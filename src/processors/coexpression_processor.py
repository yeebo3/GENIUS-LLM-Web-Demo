# processors/coexpression_processor.py
import os
import pandas as pd
from collections import defaultdict
from typing import List
from .base_processor import BaseDataProcessor

class CoexpressionProcessor(BaseDataProcessor):
    def read_data(self) -> pd.DataFrame:
        all_data = []
        for filename in os.listdir(self.input_path):
            if (filename.startswith("cultivar_c1_") or 
                filename.startswith("cultivar_c2_")) and filename.endswith(".txt"):
                file_path = os.path.join(self.input_path, filename)
                df = pd.read_csv(file_path, sep='\s+', header=0)
                all_data.append(df)
        return pd.concat(all_data, ignore_index=True)

    def process_data(self, df: pd.DataFrame) -> List[str]:
        gene_pair_set = set()
        gene_relations = defaultdict(list)
        
        for _, row in df.iterrows():
            try:
                weight = float(row['weight'])
                if weight > 0.9:
                    gene_pair = tuple(sorted([row['row'], row['col']]))
                    if gene_pair not in gene_pair_set:
                        gene_pair_set.add(gene_pair)
                        gene_relations[gene_pair[0]].append((gene_pair[1], weight))
                        gene_relations[gene_pair[1]].append((gene_pair[0], weight))
            except ValueError:
                continue

        result_text = []
        for gene, relations in gene_relations.items():
            if relations:
                relations_text = [
                    f"with gene '{col}' having a co-expression weight of '{weight:.6f}'"
                    for col, weight in relations
                ]
                result_text.append(f"Gene '{gene}' is co-expressed {', '.join(relations_text)}.")

        return result_text