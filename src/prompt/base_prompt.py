# prompt_generate/base_prompt.py
from abc import ABC, abstractmethod

class BasePrompt(ABC):
    @abstractmethod
    def generate_prompt(self, gene_id):
        """Generate a prompt for gene prediction"""
        pass
