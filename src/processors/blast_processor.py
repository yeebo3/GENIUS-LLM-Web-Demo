# src/data/processors/blast_processor.py
import pandas as pd
from typing import List
from .base_processor import BaseDataProcessor

class BlastProcessor(BaseDataProcessor):
    def read_data(self) -> pd.DataFrame:
        column_names = [
            "query", "subject", "similarity", "alignment_length",
            "mismatches", "gap_openings", "q_start", "q_end",
            "s_start", "s_end", "e_value", "bit_score"
        ]
        return pd.read_csv(
            self.input_path,
            sep='\s+',
            header=None,
            names=column_names
        )
    
    def process_data(self, df: pd.DataFrame) -> List[str]:
        df_filtered = df[df['similarity'] != 100.000]
        result_text = []
        
        for gene, group in df_filtered.groupby('query'):
            descriptions = []
            for _, row in group.iterrows():
                description = (
            f"Gene '{row['query']}' has a sequence similarity of '{row['similarity']:.3f}' "
            f"with gene '{row['subject']}', alignment length is '{row['alignment_length']}', "
            f"mismatches is '{row['mismatches']}', gaps is '{row['gap_openings']}', "
            f"query start position is '{row['q_start']}', query end position is '{row['q_end']}', "
            f"target start position is '{row['s_start']}', target end position is '{row['s_end']}', "
            f"e-value is '{row['e_value']}', alignment score is '{row['bit_score']}'."
                )
                descriptions.append(description)
            result_text.append("\n".join(descriptions))
            
        return result_text