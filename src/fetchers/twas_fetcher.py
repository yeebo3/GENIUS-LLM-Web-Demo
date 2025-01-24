# src/fetchers/twas_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class TwasFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            twas_collection = self.db['gene_trait_twas']
            twas_result = twas_collection.find_one({"gene_id": gene_id})
            
            if not twas_result:
                self.logger.info(f"No TWAS data found for gene {gene_id}")
                return f"No TWAS data found for gene {gene_id}.", []
            
            traits = twas_result.get("traits", [])
            description_list = []
            
            for trait in traits:
                description = (
                    f"At '{trait['stage']}' stage, the gene is associated with "
                    f"'{trait['phenotype']}' with a TWAS Z-score of {trait['twas_zscore']:.4f}."
                )
                description_list.append(description)
            
            self.logger.info(f"Successfully fetched TWAS data for gene {gene_id}")
            return "\n".join(description_list), []
            
        except Exception as e:
            self.logger.error(f"Error fetching TWAS data for gene {gene_id}: {str(e)}")
            raise