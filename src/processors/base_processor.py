# src/data/base_processor.py
from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any

class BaseDataProcessor(ABC):
    """Base class for data processing"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        
    @abstractmethod
    def read_data(self) -> pd.DataFrame:
        """Read data"""
        pass
        
    @abstractmethod
    def process_data(self, df: pd.DataFrame) -> List[str]:
        """Process the data and convert it to a textual description"""
        pass
        
    def save_data(self, text_data: List[str]) -> None:
        """Save the processed data"""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(text_data))
        
    def run(self) -> None:
        """Run the data processing workflow"""
        print(f"Processing {self.__class__.__name__}...")
        df = self.read_data()
        text_data = self.process_data(df)
        self.save_data(text_data)
        print(f"Finished processing {self.__class__.__name__}")
