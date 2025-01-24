# importers/homolog_importer.py
import re
from typing import List
from .base_importer import BaseMongoImporter

class HomologImporter(BaseMongoImporter):
    def parse_data(self, file_path: str) -> List[dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        homolog_matches = re.findall(
            r"Gene: '([^']+)'\n"
            r"Homologous gene in Arabidopsis thaliana: '([^']+)' \(Symbol: '([^']+)'\)\n"
            r"Location: Chromosome '([^']+)', from position '([^']+)' to '([^']+)'\n"
            r"Full name: '([^']+)'\n"
            r"Function: '([^']+)'",
            content
        )

        return [
            {
                "gene_id": match[0],
                "homologous_gene": match[1],
                "arabidopsis_symbol": match[2],
                "chromosome": match[3],
                "location_start": int(match[4]) if match[4].isdigit() else None,
                "location_end": int(match[5]) if match[5].isdigit() else None,
                "full_name": match[6],
                "function_description": match[7]
            }
            for match in homolog_matches
        ]

    def import_data(self, data: List[dict], collection_name: str) -> None:
        collection = self.db[collection_name]
        for item in data:
            collection.insert_one(item)
           