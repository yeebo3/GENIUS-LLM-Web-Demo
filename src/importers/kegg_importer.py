import re
from typing import List
from .base_importer import BaseMongoImporter

class KEGGImporter(BaseMongoImporter):
    def parse_data(self, file_path: str) -> List[dict]:
        """
        Parse the KEGG data file.
        """
        # Regular expression: Match fields in the KEGG data
        record_pattern = re.compile(
            r"Gene: '([^']+)'\s+Pathway: '([^']+)'\s+Description: '([^']+)'"
        )

        kegg_data = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match all KEGG records
        matches = record_pattern.findall(content)

        # Construct the KEGG data dictionary
        for match in matches:
            kegg_data.append({
                "gene_id": match[0],
                "pathway": match[1],
                "description": match[2]
            })

        return kegg_data

    def import_data(self, data: List[dict], collection_name: str) -> None:
        """
        Import the parsed KEGG data into the MongoDB collection one by one.
        """
        collection = self.db[collection_name]

        # Insert data one by one
        for item in data:
            collection.insert_one(item)
            

    def run(self, file_path: str, collection_name: str):
        """
        Main entry point: Parse data from the file and import it into the specified MongoDB collection.
        """
        print(f"Starting to process KEGG file: {file_path}")
        data = self.parse_data(file_path)  # Call the parsing method
        print(f"Parsed {len(data)} records from {file_path}")
        self.import_data(data, collection_name)  # Call the import method
        print(f"Successfully imported data into collection: {collection_name}")
