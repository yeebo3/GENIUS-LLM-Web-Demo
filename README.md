# GENIUS-LLM Web Demo

### Project Introduction

This project is modified and expanded based on the open-source project  [GENIUS-LLM](https://github.com/yimengzhiyan/GENIUS-LLM), 
realizing a complete front-end and back-end separated Web application to facilitate users' online experience of the model functions.

## 1. Script Overview

### Configuration
`data_config.yaml` - In this yaml file, customize your own API, data paths, and database addresses and other configurations.

### Scripts Overview
The project is divided into five main parts:

#### 1.1 User-Facing Script
- **01process_data.py** - Processes raw data into text format
- **02import_data.py** - Imports processed data into MongoDB
- **03predict.py** - Users need to modify two parts before running this py in `data_config.yaml`
- **gene_predict.py** - Interface with the front-end
#### 1.2 Model Module
- **__init__.py** - Empty file for package initialization
- **base_model.py** - Calls the model API to generate prediction results
- **llm_model.py** - Handles interactions with the OpenAI API or others for compatibility. Modify this if using a different model
- **model_factory.py** - Creates different model instances based on the configuration

#### 1.3 Prompt Module
- **__init__.py** - Empty file for package initialization
- **base_prompt.py** - Generates prompts for gene prediction
- **gene_prompt.py** - Extracts gene data from MongoDB and integrates it into comprehensive prompts
- **prompt_factory.py** - Creates different types of prompt generators

#### 1.4 Data Process
We provide cotton data as examples.

#### 1.5 Web
- **upload.py** - If you want to use the prediction function on the web page, you must first run this file to establish a connection with the backend.
- **welcome.html** - Welcome Screen
- **index.html** - Chat Screen

### File Structure
```
GENIUS-LLM-Web-Demo
├── chat/               
│   ├── .idea/          
│   ├── font/           
│   ├── logs/           
│   ├── pic/            
│   ├── index.html      
│   ├── welcome.html    
│   └── upload.py       
├── config/
│   └── data_config.yaml 
├── logs/               
│   ├── import_data.log  
│   ├── predict.log      
│   └── process_data.log     
├── scripts/            
│   ├── 01process_data.py 
│   ├── 02import_data.py  
│   ├── 03predict.py     
│   └── gene_predict.py
├── src/                
│   ├── data/           
│   │   ├── fetchers/      
│   │   ├── yourdata_process/  
│   │   └── yourdata_process_output/ 
│   ├── fetchers/       
│   ├── importers/      
│   ├── model/          
│   ├── processors/     
│   ├── prompt/         
│   └── utils/              
├── environment.yml                
├── README.md           
└── requirements.txt    
```

### File Descriptions
- **README.md** - This file
- **data_config.yaml** - Configuration file
- **01process_data.py** - Processes data
- **02import_data.py** - Imports data to MongoDB
- **03predict.py** - Calls the language model to predict genes
- **upload.py** - Connect to the backend
- **gene_predict.py** - Connect to the front-end
- **logs/** - Stores log files
- **data/** - Contains raw and processed data
- **fetchers/** - Fetches 7 types of data
- **importers/** - Imports data
- **model/** - Interfaces with the large model API
- **processors/** - Converts data into text
- **prompt/** - Manages prompt engineering

---

## 2. Experimental Environment

### 2.1 MongoDB
- db version v8.0.3
- Build Info:
  ```json
  {
    "version": "8.0.3",
    "gitVersion": "89d97f2744a2b9851ddfb51bdf22f687562d9b06",
    "modules": [],
    "allocator": "tcmalloc-gperf",
    "environment": {
        "distmod": "windows",
        "distarch": "x86_64",
        "target_arch": "x86_64"
    }
  }
  ```

### 2.2 MongoDB Database Tools
- Version: 100.12.0
- Download link: https://www.mongodb.com/try/download/database-tools

### 2.3 Required Packages
Packages required for the experiment can be found in: `environment.yml`
1. First activate your environment: `conda activate your_env_name`
2. Update/install the required packages in your environment: `conda env update -f environment.yml`

---

## 3. Gene Prediction

### 3.1 Preparing for Data Import
Before you begin, please make sure that:
- Your MongoDB database is correctly installed
- MongoDB Database Tools component is also installed (prerequisite for step 2)
- Your environment is correctly configured

Then, create a folder for storing the corresponding species, and put your JSON and BSON formatted data into the designated folder (`your_db_path`).

For example:
```
mkdir "C:\Users\HZAU\Desktop\GENIUS-LLM\mongo_restore_ready\cotton_gene_db"

C:\Users\HZAU\Desktop\GENIUS-LLM\mongo_restore_ready\
└── cotton_gene_db\
    ├── gene_blast_similarity.bson
    └── gene_blast_similarity.metadata.json
```

### 3.2 Import the Species Database
Open Windows terminal as administrator, navigate to the directory where the mongorestore command is located, and execute:
```
mongorestore --db your_db "your_db_path"
```

For example:
```
mongorestore --db cotton_gene_db "C:\Users\HZAU\Desktop\GENIUS-LLM\mongo_restore_ready\cotton_gene_db"
```

### 3.3 Edit the Configuration File
The config file is located at: `config/data_config.yaml`

In the configuration file, you may need to modify the following parameters:
- Change `api_key` to your own API key (must be modified)
- Change `database: "rice_gene_db"` to the database name in MongoDB for the organism you wish to predict
- The `data_paths` section should be changed to your own raw data paths (used by `01process_data.py` to process raw data into text data)
- The `data_paths` section also refers to the output file path generated by `01process_data.py` (used by `02import_data.py` to import the text data into MongoDB)
- The `common` section is for logging options and setting reliable threshold values for blast, coexpression, and TWAS

If you use the provided data, you do not need to modify the "data_paths", "data_imports", and "common" sections.

### 3.4 Input Gene ID for Prediction
Open `03predict.py` and find:
```python
# Step 1: Get the gene ID input from the user
gene_id = get_gene_input("LOC_Os01g01080")
```

Replace "LOC_Os01g01080" with your target gene ID.

### 3.5 How to Run
1. First run `01process_data.py`
2. Then run `02import_data.py`
3. Finally, run `03predict.py` 

### 3.6 How to Run the Web
1. First run `upload.py`
2. Then run `welcome.html` or `index.html`

**Note**: If you are using our provided data and have imported the downloaded data into MongoDB as described in 2.1 and 2.2, you can run `03predict.py` directly.
