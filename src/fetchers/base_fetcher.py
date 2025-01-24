# src/fetchers/base_fetcher.py
from abc import ABC, abstractmethod
from typing import Tuple, List, Any
import logging

class BaseDataFetcher(ABC):
    """Base class for data fetchers"""
    
    def __init__(self, db_client):
        self.db = db_client
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def fetch_data(self, gene_id: str) -> Tuple[str, List[str]]:
        """
        Fetch data from database
        
        Args:
            gene_id (str): Gene identifier
            
        Returns:
            Tuple[str, List[str]]: (description, list of related genes)
        """
        pass