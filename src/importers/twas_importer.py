# importers/twas_importer.py
import re
from typing import List
from .base_importer import BaseMongoImporter

class TwasImporter(BaseMongoImporter):
    def parse_data(self, file_path: str) -> List[dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        twas_matches = re.findall(
            r"Gene '([^']+)' at stage '([^']+)' is associated with trait "
            r"'([^']+)' with a TWAS Z-score of '([-\d.]+)'",
            content,
            re.DOTALL
        )

        gene_traits = {}
        for gene_id, stage, phenotype, zscore in twas_matches:
            if gene_id not in gene_traits:
                gene_traits[gene_id] = []
            
            gene_traits[gene_id].append({
                "stage": stage,
                "phenotype": phenotype,
                "twas_zscore": float(zscore)
            })

        return [
            {
                "gene_id": gene_id,
                "traits": traits
            }
            for gene_id, traits in gene_traits.items()
        ]

    def import_data(self, data: List[dict], collection_name: str) -> None:
        collection = self.db[collection_name]
        for item in data:
            collection.insert_one(item)
            