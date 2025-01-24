# src/data/fetchers/base_fetcher.py
from abc import ABC, abstractmethod
from typing import Tuple, List, Any

class BaseDataFetcher(ABC):
    def __init__(self, db_client):
        self.db = db_client
        
    @abstractmethod
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        """Fetch data from database and return description and related genes"""
        pass