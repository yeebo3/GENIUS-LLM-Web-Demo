import re
from typing import List
from pymongo import MongoClient

class GOImporter:
    def __init__(self, db_uri: str, db_name: str):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def parse_data(self, file_path: str) -> List[dict]:
        """
        Parse the GO data file, extracting Gene, GO Term, Ontology, and Description.
        """
        records = []
        record_pattern = re.compile(
            r"Gene: '([^']+)'\s+GO Term: '([^']+)'\s+Ontology: '([^']+)'\s+Description: '([^']+)'"
        )

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match all records
        matches = record_pattern.findall(content)

        # Construct the record list
        for match in matches:
            records.append({
                "gene": match[0],
                "go_term": match[1],
                "ontology": match[2],
                "description": match[3]
            })

        return records

    def import_data(self, data: List[dict], collection_name: str) -> None:
        """
        Import the parsed GO data into the MongoDB collection one by one.
        """
        collection = self.db[collection_name]

        # Insert data one by one
        for record in data:
            collection.insert_one(record)
           

    def run(self, file_path: str, collection_name: str):
        """
        Main entry point: Parse data from the file and import it into the specified MongoDB collection.
        """
        print(f"Starting to process GO file: {file_path}")
        data = self.parse_data(file_path)  # Call the parsing method
        print(f"Parsed {len(data)} records from {file_path}")
        self.import_data(data, collection_name)  # Call the import method
        print(f"Successfully imported data into collection: {collection_name}")
