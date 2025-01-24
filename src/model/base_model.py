# model/base_model.py

from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def call_api(self, prompt):
        """Call the model API"""
        pass
