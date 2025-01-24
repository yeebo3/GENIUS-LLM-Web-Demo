# model/model_factory.py

from .llm_model import LLMModel

class ModelFactory:
    @staticmethod
    def create_model(model_type='llm'):
        """Create different model instances based on the configuration file or type"""
        if model_type == 'llm':
            return LLMModel()
        else:
            raise ValueError("Unsupported model type")
