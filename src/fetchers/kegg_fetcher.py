# src/fetchers/kegg_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class KEGGFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            kegg_collection = self.db['gene_kegg']
            kegg_result = kegg_collection.find_one({"gene_id": gene_id})
            
            if not kegg_result:
                self.logger.info(f"No KEGG data found for gene {gene_id}")
                return f"No KEGG data found for gene {gene_id}.", []
            
            pathways = kegg_result.get("pathways", [])
            description_list = [
                f"Pathway: {pathway['name']} - {pathway['description']}"
                for pathway in pathways
            ]
            return "\n".join(description_list), []
        except Exception as e:
            self.logger.error(f"Error fetching KEGG data for gene {gene_id}: {str(e)}")
            raise