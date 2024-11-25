from .storage import JsonFileStorageService


def test_instantiation():
    service = JsonFileStorageService(filename="hmm")
