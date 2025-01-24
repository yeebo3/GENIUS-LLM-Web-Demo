# src/fetchers/expression_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class ExpressionFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            expression_collection = self.db['gene_expression']
            expression_result = expression_collection.find_one({"gene_id": gene_id})
            
            if not expression_result:
                self.logger.info(f"No expression data found for gene {gene_id}")
                return f"No expression data found for gene {gene_id}.", []
            
            tissue_expression = expression_result.get("tissue_expression", {})
            description_list = []
            
            for tissue, expression_value in tissue_expression.items():
                description = (
                    f"Gene '{gene_id}' has expression level of {expression_value:.6f} "
                    f"in tissue '{tissue}'."
                )
                description_list.append(description)
            
            self.logger.info(f"Successfully fetched expression data for gene {gene_id}")
            return "\n".join(description_list), []
            
        except Exception as e:
            self.logger.error(f"Error fetching expression data for gene {gene_id}: {str(e)}")
            raise