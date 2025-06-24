# src/fetchers/homolog_fetcher.py
from typing import Tuple, List
from .base_fetcher import BaseDataFetcher
from typing import List, Dict, Any

class HomologFetcher(BaseDataFetcher):
    def fetch_data(self, gene_id: str) ->  Tuple[str, List[str]]:
        """
        Fetch homologous gene data from MongoDB.

        Args:
            gene_id: Target gene ID.

        Returns:
            A list containing a dictionary with homologous gene data. 
            Returns an empty list if no data is found.
        """
        try:
            # Get MongoDB collection
            homologous_genes_collection = self.db['homologous_genes']
            
            # Query the document for the gene_id
            homologous_result = homologous_genes_collection.find_one({"gene_id": gene_id})
            
            # If no result is found
            if not homologous_result:
                self.logger.info(f"No homologous gene data found for gene {gene_id}")
                return []

            # Construct the returned dictionary
            result_data = {
                "gene_id": gene_id,
                "homologous_gene": homologous_result.get("homologous_gene"),
                "arabidopsis_symbol": homologous_result.get("arabidopsis_symbol", "-"),
                "chromosome": homologous_result.get("chromosome", "-"),
                "location_start": homologous_result.get("location_start"),
                "location_end": homologous_result.get("location_end"),
                "full_name": homologous_result.get("full_name", "-"),
                "function_description": homologous_result.get("function_description", "-"),
            }

            # Construct the description message
            description = (
                f"Gene '{gene_id}' has a homologous gene in Arabidopsis thaliana, "
                f"'{result_data['homologous_gene']}' "
                f"with symbol '{result_data['arabidopsis_symbol']}'.\n"
                f"Chromosome location: {result_data['chromosome']} "
                f"from {result_data['location_start']} "
                f"to {result_data['location_end']}.\n"
                f"Full name: {result_data['full_name']}.\n"
                f"Function: {result_data['function_description']}."
            )

            # Log success
            self.logger.info(f"Successfully fetched homolog data for gene {gene_id}")
            
            # Return the result
            return [{"data": result_data, "description": description}]

        except Exception as e:
            self.logger.error(f"Error fetching homolog data for gene {gene_id}: {str(e)}")
            raise
