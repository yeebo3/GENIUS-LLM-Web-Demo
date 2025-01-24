import os
import logging
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.config_loader import load_config
from src.importers.importer_factory import MongoImporterFactory  # Path modified
from pymongo import MongoClient

def setup_logging(log_path: str):
    """Set up logging configuration"""
    os.makedirs(log_path, exist_ok=True)
    logging.basicConfig(
        filename=f"{log_path}/import_data.log",
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    # Load configuration
    config = load_config("config/data_config.yaml")
    
    # Setup logging
    setup_logging(config['common']['log_path'])
    
    # Initialize MongoDB client
    try:
        client = MongoClient(config['mongodb']['uri'])
        db = client[config['mongodb']['database']]
        
        # Import each data type
        importer_factory = MongoImporterFactory()
        
        for data_type, import_config in config['data_imports'].items():
            print(f"Starting import for {data_type}...")
            logging.info(f"Starting import for {data_type}...")
            try:
                importer = importer_factory.get_importer(
                    data_type,
                    db_uri=config['mongodb']['uri'],
                    db_name=config['mongodb']['database']
                )
                importer.run(
                    file_path=import_config['input_path'],
                    collection_name=import_config['collection']
                )
                logging.info(f"Successfully imported {data_type} data")
                print(f"Finished import for {data_type}.")
            except Exception as e:
                logging.error(f"Error importing {data_type} data: {str(e)}")
                print(f"Error importing {data_type} data: {str(e)}")
                
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {str(e)}")
        print(f"Error connecting to MongoDB: {str(e)}")
        
    finally:
        client.close()

if __name__ == "__main__":
    main()
