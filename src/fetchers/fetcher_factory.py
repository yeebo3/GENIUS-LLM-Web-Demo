# src/fetchers/fetcher_factory.py
from typing import Dict, Type
from .base_fetcher import BaseDataFetcher
from .blast_fetcher import BlastFetcher
from .coexpression_fetcher import CoexpressionFetcher
from .expression_fetcher import ExpressionFetcher
from .homolog_fetcher import HomologFetcher
from .twas_fetcher import TwasFetcher
from .go_fetcher import GOFetcher
from .kegg_fetcher import KEGGFetcher

class DataFetcherFactory:
    """Factory for creating data fetchers"""
    
    _fetchers: Dict[str, Type[BaseDataFetcher]] = {
        'blast': BlastFetcher,
        'coexpression': CoexpressionFetcher,
        'expression': ExpressionFetcher,
        'homolog': HomologFetcher,
        'twas': TwasFetcher,
        'go': GOFetcher,
        'kegg': KEGGFetcher,
    }
    
    def __init__(self, db_client):
        self.db_client = db_client
    
    def get_fetcher(self, fetcher_type: str) -> BaseDataFetcher:
        """Get appropriate fetcher instance based on type"""
        if fetcher_type not in self._fetchers:
            raise ValueError(f"Unknown fetcher type: {fetcher_type}")
            
        fetcher_class = self._fetchers[fetcher_type]
        return fetcher_class(self.db_client)