# prompt_generate/prompt_factory.py

from .gene_prompt import GenePrompt

class PromptFactory:
    @staticmethod
    def create_prompt(prompt_type='gene'):
        """Generate different types of prompts based on the configuration or type"""
        if prompt_type == 'gene':
            return GenePrompt()
        else:
            raise ValueError("Unsupported prompt type")
