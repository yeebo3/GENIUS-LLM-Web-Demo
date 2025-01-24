# importers/base_importer.py
from abc import ABC, abstractmethod
from pymongo import MongoClient
from typing import Any, Dict

class BaseMongoImporter(ABC):
    """Base MongoDB data importer"""
    
    def __init__(self, db_uri: str, db_name: str):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
    
    @abstractmethod
    def parse_data(self, file_path: str) -> list:
        """Parse data file"""
        pass
    
    @abstractmethod
    def import_data(self, data: list, collection_name: str) -> None:
        """Import data into MongoDB"""
        pass
    
    def run(self, file_path: str, collection_name: str) -> None:
        """Run import process"""
        print(f"Importing data to collection: {collection_name}")
        data = self.parse_data(file_path)
        self.import_data(data, collection_name)
        print(f"Finished importing data to {collection_name}")