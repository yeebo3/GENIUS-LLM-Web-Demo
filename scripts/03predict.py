import yaml
import logging
import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from src.model.model_factory import ModelFactory  # Create model from model_factory
from src.prompt.prompt_factory import PromptFactory  # Create prompt generator from prompt_factory

# Read the configuration file
with open(r'C:\Users\zyb20\Downloads\GENIUS-LLM\config\data_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Set up logging
log_dir = 'logs'
log_file = os.path.join(log_dir, 'predict.log')

# Ensure the log directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Output logs to a file
        logging.StreamHandler()  # Also output to the console
    ]
)

logger = logging.getLogger(__name__)

def get_gene_input(gene_id):
    """Get the gene ID input from the user"""
    print("Please enter the gene ID for prediction: ")
    return gene_id

if __name__ == "__main__":
    # Step 1: Get the gene ID input from the user
    gene_id = get_gene_input("AT1G03000")

    # Step 2: Create a prompt generator instance
    try:
        prompt_generator = PromptFactory.create_prompt(prompt_type='gene')  # Create the prompt generator
        prompt = prompt_generator.generate_prompt(gene_id)  # Generate the prompt
        logger.info(f"Prompt generated for gene {gene_id}")
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        exit(1)
    
    # Step 3: Create a model instance
    try:
        model = ModelFactory.create_model(model_type='llm')  # Create the model instance
        result = model.call_api(prompt)  # Call the model API for prediction
        logger.info("Prediction result obtained.")
    except Exception as e:
        logger.error(f"Error calling the model API: {e}")
        exit(1)

    # Step 4: Output the final prediction result to the user
    logger.info(f"Final prediction result: {result}")
    print("\n=== Prediction Result ===\n", result)
