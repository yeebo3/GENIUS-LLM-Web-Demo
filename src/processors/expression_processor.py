# processors/expression_processor.py
import pandas as pd
from typing import List
from .base_processor import BaseDataProcessor

class ExpressionProcessor(BaseDataProcessor):
    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.input_path)

    def process_data(self, df: pd.DataFrame) -> List[str]:
        result_text = []
        
        for index, row in df.iterrows():
            gene_id = row['GeneId']
            expressions = []
            
            for column in df.columns[1:]:
                expression_value = row[column]
                if expression_value != 0:
                    expressions.append(
                        f"has expression level of '{expression_value:.6f}' in tissue '{column}'"
                    )
                    
            if expressions:
                result_text.append(f"Gene '{gene_id}' {', '.join(expressions)}.")

        return result_text