# src/data/processor_factory.py
from typing import Dict, Type
from .base_processor import BaseDataProcessor
from .blast_processor import BlastProcessor
from .coexpression_processor import CoexpressionProcessor
from .expression_processor import ExpressionProcessor
from .homolog_processor import HomologProcessor
from .twas_processor import TwasProcessor
from .kegg_processor import KEGGProcessor
from .go_processor import GOProcessor

class DataProcessorFactory:
    """Data processor factory class"""
    
    _processors: Dict[str, Type[BaseDataProcessor]] = {
        'blast': BlastProcessor,
        'coexpression': CoexpressionProcessor,
        'expression': ExpressionProcessor,
        'homolog': HomologProcessor,
        'twas': TwasProcessor,
        'kegg': KEGGProcessor,
        'go': GOProcessor,
    }
    
    @classmethod
    def get_processor(cls, 
                     processor_type: str,
                     input_path: str,
                     output_path: str) -> BaseDataProcessor:
        """Get a data processor instance"""
        if processor_type not in cls._processors:
            raise ValueError(f"Unknown processor type: {processor_type}")
            
        processor_class = cls._processors[processor_type]
        return processor_class(input_path, output_path)
