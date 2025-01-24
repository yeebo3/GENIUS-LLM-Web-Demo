# scripts/process_data.py
''' The text processing of 7 types of data has been debugged. 
'''
import os
import logging
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import the src module
from src.utils.config_loader import load_config
from src.processors.processor_factory import DataProcessorFactory  # Path modified

def setup_logging(log_path: str):
    """Set up logging configuration"""
    os.makedirs(log_path, exist_ok=True)
    logging.basicConfig(
        filename=f"{log_path}/process_data.log",
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Load configuration
    config = load_config("config/data_config.yaml")
    
    # Setup logging
    setup_logging(config['common']['log_path'])
    
    # Create output directories if they don't exist
    for data_type, paths in config['data_paths'].items():
        os.makedirs(os.path.dirname(paths['output']), exist_ok=True)
    
    # Process each data type
    processor_factory = DataProcessorFactory()
    
    for data_type, paths in config['data_paths'].items():
        try:
            processor = processor_factory.get_processor(
                data_type,
                paths['input'],
                paths['output']
            )
            processor.run()
            logging.info(f"Successfully processed {data_type} data")
        except Exception as e:
            logging.error(f"Error processing {data_type} data: {str(e)}")
            print(f"Error processing {data_type} data: {str(e)}")

if __name__ == "__main__":
    main()
