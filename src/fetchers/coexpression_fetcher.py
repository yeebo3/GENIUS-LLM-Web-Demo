# src/fetchers/coexpression_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class CoexpressionFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            coexpression_collection = self.db['gene_coexpression']
            coexpression_result = coexpression_collection.find_one({"gene_id": gene_id})
            
            if not coexpression_result:
                self.logger.info(f"No coexpression data found for gene {gene_id}")
                return f"No coexpression data found for gene {gene_id}.", []
            
            coexpressions = coexpression_result.get("coexpressed_genes", [])
            description_list = []
            high_weight_genes = []
            
            for coexpression in coexpressions:
                related_gene = coexpression['gene_id']
                weight = coexpression['weight']
                description = (
                    f"Gene '{gene_id}' is co-expressed with gene '{related_gene}' "
                    f"with a co-expression weight of {weight:.6f}."
                )
                description_list.append(description)
                high_weight_genes.append(related_gene)
            
            self.logger.info(f"Successfully fetched coexpression data for gene {gene_id}")
            return "\n".join(description_list), high_weight_genes
            
        except Exception as e:
            self.logger.error(f"Error fetching coexpression data for gene {gene_id}: {str(e)}")
            raise