
## Table of Contents
- [Configuration](#configuration)
- [Logs](#logs)
- [Scripts](#scripts)
- [Source](#source)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)

## Configuration
`data_config.yaml` In this yaml file, customize your own API, data paths, and database addresses and other configurations.
## Scripts Overview
The project is divided into four main parts:

### 1. User-Facing Script
- **01process_data.py**
- **02import_data.py**
- **03predict.py**: 
        - Users need to modify two parts before running this py in `data_config.yaml`

### 2. Model Module
- **__init__.py**: Empty file for package initialization.
- **base_model.py**: Calls the model API to generate prediction results.
- **llm_model.py**: Handles interactions with the OpenAI API or others for compatibility. Modify this if using a different model.
- **model_factory.py**: Creates different model instances based on the configuration.

### 3. Prompt Module
- **__init__.py**: Empty file for package initialization.
- **base_prompt.py**: Generates prompts for gene prediction.
- **gene_prompt.py**: Extracts gene data from MongoDB and integrates it into comprehensive prompts.
- **prompt_factory.py**: Creates different types of prompt generators.

### 4. Data process
We provide cotton data as examples.

## File Structure

```
├── config
│   └── data_config.yaml
├── logs
│   ├── import_data.log
│   ├── predict.log
│   └── process_data.log
├── README.md
├── scripts
│   ├── 01process_data.py
│   ├── 02import_data.py
│   └── 03predict.py
└── src
                ├── data
                │   ├── fetchers
                │   ├── yourdata_process
                │   └── yourdata_process_output
                ├── fetchers
                ├── importers
                ├── model
                ├── processors
                ├── prompt
                └── utils
```

## File Descriptions
- **README.md**: This file.
- **data_config.yaml**: Configuration file.
- **01process_data.py**: Processes data.
- **02import_data.py**: Imports data to MongoDB.
- **03predict.py**: Calls the language model to predict genes.
- **logs/**: Stores log files.
- **data/**: Contains raw and processed data.
- **fetchers/**: Fetches 7 types of data.
- **importers/**: Imports data.
- **model/**: Interfaces with the large model API.
- **processors/**: Converts data into text.
- **prompt/**: Manages prompt engineering.

## Usage
To run the project, follow these steps:

1. **Install Required Packages:**（*not list all*）
                ```bash
                pip install pyyaml==6.0.1 openai==0.28.0 pymongo==4.8.0
                ```

2. **Import Data:**
                Place your data into `src/data/yourdata_process`.
                create your mongoDB database and collection.

3. **Configure:**
                Modify `data_config.yaml` to fit your requirements.

4. **Run Scripts Sequentially:**
                python scripts/01process_data.py
                python scripts/02import_data.py
                python scripts/03predict.py
