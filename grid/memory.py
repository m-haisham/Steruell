from pathlib import Path

from core.memory import JsonMemory


class AppDatabase(JsonMemory):
    instance = None

    GRID_KEY = 'grid'

    def __init__(self):
        super(AppDatabase, self).__init__(Path('data.db'))

    def save_grid(self, grid, drawable):
        self.put(AppDatabase.GRID_KEY, (grid, drawable))
        self.save()

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
