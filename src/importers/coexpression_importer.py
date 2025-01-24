# importers/coexpression_importer.py
import re
from typing import List, Dict
from .base_importer import BaseMongoImporter

class CoexpressionImporter(BaseMongoImporter):
    def parse_data(self, file_path: str) -> List[dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        coexpression_matches = re.findall(
            r"Gene '([^']+)' is co-expressed with gene '([^']+)' "
            r"having a co-expression weight of '([\d.]+)'[,\.]",
            content
        )

        gene_coexpressions = {}
        for gene_id, target_gene, weight in coexpression_matches:
            if gene_id not in gene_coexpressions:
                gene_coexpressions[gene_id] = []
            gene_coexpressions[gene_id].append({
                "gene_id": target_gene,
                "weight": float(weight)
            })

        return [
            {
                "gene_id": gene_id,
                "coexpressed_genes": coexpressions
            }
            for gene_id, coexpressions in gene_coexpressions.items()
        ]

    def import_data(self, data: List[dict], collection_name: str) -> None:
        collection = self.db[collection_name]
        for item in data:
            collection.update_one(
                {"gene_id": item["gene_id"]},
                {"$set": item},
                upsert=True
            )
           