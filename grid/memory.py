import json

from pathlib import Path


class JsonMemory:
    """
    Simple Json key pair database
    """

    def __init__(self, location):

        if type(location) != Path:
            self.location = Path(location)
        else:
            self.location = location

        self.location.parent.mkdir(parents=True, exist_ok=True)

        self.data = {}

        self.load()

    def load(self):
        try:
            with self.location.open('r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.save()

    def save(self):
        with self.location.open('w') as f:
            json.dump(self.data, f)

    def get(self, key):
        try:
            value = self.data[key]
        except KeyError:
            value = None

        return value

    def put(self, key, value):
        self.data[key] = value


class AppDatabase(JsonMemory):
    instance = None

    GRID_KEY = 'grid'

    def __init__(self):
        super(AppDatabase, self).__init__(Path('data.db'))

    def save_grid(self, grid):
        self.put(AppDatabase.GRID_KEY, grid)

    def load_grid(self):
        try:
            return self.get(AppDatabase.GRID_KEY)
        except KeyError:
            return None

    @staticmethod
    def database():
        """
        :return: database instance
        :rtype: AppDatabase
        """
        if AppDatabase.instance is None:
            AppDatabase.instance = AppDatabase()

        return AppDatabase.instance
