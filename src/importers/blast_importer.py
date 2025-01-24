# importers/blast_importer.py
import re
from typing import List
from .base_importer import BaseMongoImporter

class BlastImporter(BaseMongoImporter):
    def parse_data(self, file_path: str) -> List[dict]:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        blast_matches = re.findall(
            r"Gene '([^']+)' has a sequence similarity of '([\d.]+)' with gene '([^']+)', "
            r"alignment length is '(\d+)', mismatches is '(\d+)', gaps is '(\d+)', "
            r"query start position is '(\d+)', query end position is '(\d+)', "
            r"target start position is '(\d+)', target end position is '(\d+)', "
            r"e-value is '([^']+)', alignment score is '([\d.]+)'.",
            content
        )
        
        return [
            {
                "gene_id": match[0],
                "similarity_matches": {
                    "target_gene": match[2],
                    "similarity": float(match[1]),
                    "alignment_length": int(match[3]),
                    "mismatches": int(match[4]),
                    "gaps": int(match[5]),
                    "query_start": int(match[6]),
                    "query_end": int(match[7]),
                    "target_start": int(match[8]),
                    "target_end": int(match[9]),
                    "e_value": match[10],
                    "score": float(match[11])
                }
            }
            for match in blast_matches
        ]
    
    def import_data(self, data: List[dict], collection_name: str) -> None:
        collection = self.db[collection_name]
        for item in data:
            collection.insert_one(item)
            