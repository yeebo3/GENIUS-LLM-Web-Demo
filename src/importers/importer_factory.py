# importers/importer_factory.py
from typing import Dict, Type
from .base_importer import BaseMongoImporter
from .blast_importer import BlastImporter
from .coexpression_importer import CoexpressionImporter
from .expression_importer import ExpressionImporter
from .homolog_importer import HomologImporter
from .twas_importer import TwasImporter
from .kegg_importer import KEGGImporter
from .go_importer import GOImporter

class MongoImporterFactory:
    """Factory class for creating MongoDB data importers"""
    
    _importers: Dict[str, Type[BaseMongoImporter]] = {
        'blast': BlastImporter,
        'coexpression': CoexpressionImporter,
        'expression': ExpressionImporter,
        'homolog': HomologImporter,
        'twas': TwasImporter,
        'kegg': KEGGImporter,
        'go': GOImporter,
    }
    
    @classmethod
    def get_importer(cls, 
                    importer_type: str,
                    db_uri: str,
                    db_name: str) -> BaseMongoImporter:
        """Get appropriate importer instance based on type"""
        if importer_type not in cls._importers:
            raise ValueError(f"Unknown importer type: {importer_type}")
        
        importer_class = cls._importers[importer_type]
        return importer_class(db_uri, db_name)