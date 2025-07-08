# scripts/gene_predict.py

import yaml
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根目录

from src.model.model_factory import ModelFactory
from src.prompt.prompt_factory import PromptFactory

# 配置日志
log_dir = '../chat/logs'
log_file = os.path.join(log_dir, 'predict.log')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载配置
with open('../config/data_config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)


def run_prediction(gene_id: str) -> str:
    try:
        prompt_generator = PromptFactory.create_prompt(prompt_type='gene')
        prompt = prompt_generator.generate_prompt(gene_id)
        logger.info(f"Prompt generated for gene {gene_id}")
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        raise

    try:
        model = ModelFactory.create_model(model_type='llm')
        result = model.call_api(prompt)
        logger.info("Prediction result obtained.")
    except Exception as e:
        logger.error(f"Error calling the model API: {e}")
        raise

    logger.info(f"Final prediction result: {result}")
    return result


# 保留命令行方式调用（可选）
def get_gene_input():
    return sys.argv[1] if len(sys.argv) > 1 else input("Enter gene ID: ")

if __name__ == "__main__":
    gene_id = get_gene_input()
    print(run_prediction(gene_id))
