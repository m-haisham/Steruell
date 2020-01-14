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
        except (FileNotFoundError, json.decoder.JSONDecodeError):
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