# model/llm_model.py

import yaml
from openai import OpenAI
from .base_model import BaseModel

# Read the configuration file
with open(r'..\config\data_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

class LLMModel(BaseModel):
    def __init__(self):
        self.api_key = config['model']['api_key']
        self.base_url = config['model']['url']
        self.model_name = config['model']['model']
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    
    def call_api(self, prompt):
        """Call OpenAI API to generate prediction results"""
        full_content = ""  # Used to concatenate the final result

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": "You are a helpful assistant specialized in gene prediction."},
                          {"role": "user", "content": prompt}],
                stream=False
            )

            full_content = response.choices[0].message.content
            while response.choices[0].finish_reason == "length":
                # If the result is truncated, continue the request for generation
                prompt = full_content  # Use the current generated content as the new prompt to continue generating
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "system", "content": "You are a helpful assistant specialized in gene prediction."},
                              {"role": "user", "content": prompt}],
                    stream=False
                )
                full_content += response.choices[0].message.content

            return full_content
        except Exception as e:
            return f"Error calling API: {e}"
