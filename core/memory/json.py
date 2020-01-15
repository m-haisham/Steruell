import json
from pathlib import Path


class JsonMemory:
    """
    Simple Json key pair database
    """

    def __init__(self, location):
        """
        :param location: storage location
        """

        if type(location) != Path:
            self.location = Path(location)
        else:
            self.location = location

        self.location.parent.mkdir(parents=True, exist_ok=True)

        self.data = {}

        self.load()

    def load(self):
        """
        load from storage to memory

        :return: None
        """
        try:
            with self.location.open('r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.save()

    def save(self):
        """
        save current memory to storage

        :return: None
        """
        with self.location.open('w') as f:
            json.dump(self.data, f)

    def get(self, key):
        """
        :param key: key used as identifier
        :return: data corresponding to identifer(key)

        :returns: None if key not found
        """
        try:
            value = self.data[key]
        except KeyError:
            value = None

        return value

    def delete(self, key):
        """
        removes the key from memory

        :param key: key to be removed
        :return: None
        """
        try:
            del self.data[key]
        except KeyError:
            pass

    def put(self, key, value):
        """
        adds key-value pair to memory

        :param key: key used as identifier
        :param value: data to store
        :return: None
        """
        self.data[key] = value