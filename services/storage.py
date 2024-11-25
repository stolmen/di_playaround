import json


class StorageService:
    def store_data(self, data):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError


class JsonFileStorageService(StorageService):
    """store data as a JSON file"""

    def __init__(self, filename):
        self.filename = filename

    def store_data(self, data):
        with open(self.filename, "w") as f:
            f.write(json.dumps(data, indent=4))

    def get_data(
        self,
    ):
        with open(self.filename, "r") as f:
            data = f.read()
            if not data:
                raise ValueError("huh, no data?")
        return json.loads(data)
