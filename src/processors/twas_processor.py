# processors/twas_processor.py
import pandas as pd
from typing import List
from .base_processor import BaseDataProcessor

class TwasProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.phenotype_mapping = {
            "FE": "Fiber elongation rate",
            "FS": "Fiber strength",
            "FU": "Fiber uniformity",
            "FL": "Fiber length"
        }

    def read_data(self) -> pd.DataFrame:
        return pd.read_excel(self.input_path, sheet_name="Sheet1")

    def process_data(self, df: pd.DataFrame) -> List[str]:
        gene_relations = {}
        
        for _, row in df.iterrows():
            phenotype_full = self.phenotype_mapping.get(
                row['Phenotype'],
                row['Phenotype']
            )
            stage = row['Stage']
            gene_id = row['GeneID']
            zscore = row['TWAS.Zscore']
            
            if gene_id not in gene_relations:
                gene_relations[gene_id] = []
                
            gene_relations[gene_id].append(
                f"at stage '{stage}' is associated with trait '{phenotype_full}' "
                f"with a TWAS Z-score of '{zscore:.4f}'"
            )
        
        result_text = [
            f"Gene '{gene}' {', '.join(relations)}."
            for gene, relations in gene_relations.items()
        ]
        
        return result_text