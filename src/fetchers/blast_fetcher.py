# src/fetchers/blast_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher

class BlastFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        try:
            blast_collection = self.db['gene_blast_similarity']
            blast_results = blast_collection.find({"gene_id": gene_id})
            
            if blast_collection.count_documents({"gene_id": gene_id}) == 0:
                self.logger.info(f"No BLAST data found for gene {gene_id}")
                return f"No BLAST data found for gene {gene_id}.", []
            
            description_list = []
            similar_genes = []
            
            for result in blast_results:
                target_gene = result['similarity_matches']['target_gene']
                similarity = result['similarity_matches']['similarity']
                description = (
                    f"Gene '{gene_id}' has a similarity of {similarity:.3f} "
                    f"with gene '{target_gene}'."
                )
                description_list.append(description)
                similar_genes.append(target_gene)
            
            self.logger.info(f"Successfully fetched BLAST data for gene {gene_id}")
            return "\n".join(description_list), similar_genes
            
        except Exception as e:
            self.logger.error(f"Error fetching BLAST data for gene {gene_id}: {str(e)}")
            raise