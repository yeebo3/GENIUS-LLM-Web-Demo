# processors/homolog_processor.py
import pandas as pd
from typing import List
from .base_processor import BaseDataProcessor

class HomologProcessor(BaseDataProcessor):
    def read_data(self) -> pd.DataFrame:
        return pd.read_excel(self.input_path)

    def process_data(self, df: pd.DataFrame) -> List[str]:
        def generate_gene_description(row):
            gene_id = row['GeneID'] if pd.notna(row['GeneID']) else 'NA'
            homology = row['Homology of AtGi'] if pd.notna(row['Homology of AtGi']) else 'NA'
            symbol = row['Symbol'] if pd.notna(row['Symbol']) else 'NA'
            full_name = row['Full_name'] if pd.notna(row['Full_name']) else 'NA'
            chr_loc = row['Chr.'] if pd.notna(row['Chr.']) else 'NA'
            start = row['Start'] if pd.notna(row['Start']) else 'NA'
            end = row['End'] if pd.notna(row['End']) else 'NA'
            function_desc = row['Function description'] if pd.notna(row['Function description']) else 'NA'
            
            return f"""Gene: '{gene_id}'
Homologous gene in Arabidopsis thaliana: '{homology}' (Symbol: '{symbol}')
Location: Chromosome '{chr_loc}', from position '{start}' to '{end}'
Full name: '{full_name}'
Function: '{function_desc}'\n"""

        all_descriptions = []
        for gene_id, group in df.groupby('GeneID'):
            gene_descriptions = []
            for idx, row in group.iterrows():
                gene_description = generate_gene_description(row)
                gene_descriptions.append(gene_description)
            all_descriptions.append("\n".join(gene_descriptions))
            
        return all_descriptions