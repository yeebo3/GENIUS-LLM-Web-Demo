# src/fetchers/go_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class GOFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            go_collection = self.db['gene_go']
            go_result = go_collection.find_one({"gene_id": gene_id})
            
            if not go_result:
                self.logger.info(f"No GO data found for gene {gene_id}")
                return f"No GO data found for gene {gene_id}.", []
            
            go_annotations = go_result.get("annotations", [])
            description_list = [
                f"{annotation['term']} ({annotation['description']})"
                for annotation in go_annotations
            ]
            return "\n".join(description_list), []
        except Exception as e:
            self.logger.error(f"Error fetching GO data for gene {gene_id}: {str(e)}")
            raise


