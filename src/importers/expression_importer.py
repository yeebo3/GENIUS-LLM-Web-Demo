import re
from typing import List
from pymongo import MongoClient


class ExpressionImporter:
    def __init__(self, db_uri: str, db_name: str):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def parse_data(self, file_path: str) -> List[dict]:
        """
        Parse the data file line by line, extracting gene and corresponding tissue expression levels.
        """
        data = []

        # Regular expression: match Gene ID and expression levels in all tissues
        expression_pattern = re.compile(
            r"Gene '([^']+)'.*? has expression level of '([\d.]+)' in tissue '([^']+)'(?:,|\.|$)"
        )

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                matches = expression_pattern.findall(line)
                if matches:
                    gene_id = matches[0][0]
                    tissue_expressions = {
                        tissue: float(expression)
                        for _, expression, tissue in matches
                    }
                    data.append({
                        "gene_id": gene_id,
                        "tissue_expression": tissue_expressions
                    })

        return data

    def import_data(self, data: List[dict], collection_name: str) -> None:
        """
        Import the parsed expression data into the MongoDB collection one by one.
        """
        collection = self.db[collection_name]

        # Insert data one by one
        for item in data:
            collection.insert_one(item)
           

    def run(self, file_path: str, collection_name: str):
        """
        Main entry point: Parse data from the file and import it into the specified MongoDB collection.
        """
        print(f"Starting to process file: {file_path}")
        data = self.parse_data(file_path)  # Call the parsing method
        print(f"Parsed {len(data)} records from {file_path}")
        self.import_data(data, collection_name)  # Call the import method
        print(f"Successfully imported data into collection: {collection_name}")
