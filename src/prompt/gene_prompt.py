# prompt_generate/gene_prompt.py

from .base_prompt import BasePrompt
from pymongo import MongoClient
import yaml

# Read the configuration file
with open(r'C:\Users\zyb20\Downloads\GENIUS-LLM\config\data_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Read MongoDB configuration from the config file
mongodb_uri = config['mongodb']['uri']
database_name = config['mongodb']['database']
client = MongoClient(mongodb_uri)
db = client[database_name]

class GenePrompt(BasePrompt):
    def generate_prompt(self, gene_id):
        prompt = f"""
### **Task Overview**:
You are tasked with predicting the biological function of the target gene '{gene_id}' by analyzing multiple datasets. 
Provide a detailed prediction of the gene's function, associated biological processes, and relevant traits.

### **Data for Target Gene '{gene_id}'**:
"""

        # Get and process BLAST data
        blast_data, similar_blast_genes = self.get_blast_data(gene_id)
        prompt += f"""
#### **BLAST Similarity Data**:
{blast_data}
"""
        
        # Get and process co-expression data
        coexpression_data, high_weight_genes = self.get_coexpression_data(gene_id)
        prompt += f"""
#### **Co-expression Data**:
{coexpression_data if coexpression_data else "No co-expression data available for the target gene."}
"""

        # Get and process expression data
        expression_data = self.get_expression_data(gene_id)
        prompt += f"""
#### **Gene Expression Data Across Different Tissues**:
{expression_data}
"""

        # Get and process homologous gene data
        homologous_data = self.get_homologous_gene_data(gene_id)
        prompt += f"""
#### **Homologous Gene Data**:
{homologous_data}
"""

        # Get and process TWAS data
        twas_data = self.get_twas_data(gene_id)
        prompt += f"""
#### **TWAS Data**:
{twas_data if twas_data else "No TWAS data available for the target gene."}
"""

        # Get and process GO data
        go_data = self.get_go_data(gene_id)
        prompt += f"""
#### **Gene Ontology (GO) Data**:
{go_data if go_data else "No GO data available for the target gene."}
"""

        # Get and process KEGG data
        kegg_data = self.get_kegg_data(gene_id)
        prompt += f"""
#### **KEGG Pathway Data**:
{kegg_data if kegg_data else "No KEGG data available for the target gene."}
"""

        # Final task and output format
        prompt += """
---

### **Final Analysis**:
Based on the data for the target gene and related genes, predict the biological function of gene '{gene_id}' and its possible involvement in specific traits. Your explanation should include:

#### **1. Predicted Function**:
- Provide a concise and clear statement summarizing the predicted biological function of gene '{gene_id}'.

#### **2. Supporting Evidence**:
- Present a structured explanation of the reasoning behind your prediction. Include data and insights from:
  - **BLAST Similarity Data**: Analyze evolutionary relationships or functional similarities.
  - **Co-expression Data**: Highlight involvement in shared pathways.
  - **Gene Expression Patterns**: Determine tissue-specific roles and biological significance.
  - **Homologous Gene Functions**: Leverage conserved functionalities across species.
  - **TWAS Data**: Link gene expression to specific traits or phenotypes.
- Clearly highlight upregulation/downregulation trends across tissues, explaining their relevance to the gene's biological roles.

#### **3. Potential Traits**:
- List and describe any traits that may be influenced by gene '{gene_id}', integrating evidence from the above datasets.


#### **4. Upregulation/Downregulation Analysis**:
- Use gene expression data to analyze whether gene '{gene_id}' is upregulated or downregulated under specific conditions.
- Correlate observed trends with potential biological roles, e.g.:
  - **Upregulation**: Active involvement in processes like stress response or development.
  - **Downregulation**: Reduced activity or suppression in certain pathways or conditions.
- Cross-reference local findings with external annotations (e.g., GO terms, KEGG pathways).
  
#### **5. Step-by-Step Reasoning**:
- Provide a structured explanation showing how each dataset contributes to your prediction. Use logical connectors like "Firstly," "Furthermore," and "Lastly" for clarity.

---

### **Task Overview**:
You are tasked with predicting the biological function of the target gene '{gene_id}' by analyzing multiple datasets. Use the following datasets in order of priority to infer the gene's function, associated biological processes, and relevant traits. To strengthen the prediction, integrate evidence from **all available data sources** where possible, even if high-priority data already suggests a strong hypothesis.


### **Data for Target Gene '{gene_id}'**:
- For each supporting evidence type (e.g., BLAST, co-expression, expression data), all need to be supplemented with external data:
#### Data Sources (Ordered by Priority):
1. **TWAS Data** (High Confidence):
   - **Purpose**: Directly associate the gene with specific traits via statistical associations. High Z-scores indicate stronger associations.
   - **Usage**: TWAS associations take precedence and form the initial basis of predictions. However, use other datasets to validate and enhance confidence in TWAS-based associations.
   - Use external KEGG pathways or STRING interactions to explain observed trait associations.
   - Example: "KEGG: Pathway 'Secondary Metabolite Biosynthesis' suggests the gene is involved in cotton's fiber strength."

2. **Homologous Gene Data** (Medium-High Confidence):
   - **Purpose**: Use homologous gene functions in model organisms to support functional predictions.
   - **Usage**: Homologous gene data can strengthen TWAS predictions or provide standalone insights in the absence of TWAS. When TWAS and homologous data are aligned, continue to examine additional datasets to add support and detail.

3. **Expression Data** (Medium Confidence):
   - **Purpose**: Confirm tissue or stage-specific gene activity to validate primary predictions.
   - **Usage**: Use high or specific expression to validate TWAS and homolog predictions. Continue this validation with other data sources to form a well-supported hypothesis.
   - Validate tissue-specific expression trends using external studies or databases.

4. **BLAST Similarity Data** (Supporting Confidence):
   - **Purpose**: Identify sequence similarities with other genes to suggest functional parallels.
   - **Usage**: Utilize BLAST data to indirectly reinforce predictions from TWAS, expression, or homologous gene data. Use it as an additional layer of support, especially in stress tolerance or pathway functions.
   - Include functional annotations of homologous genes retrieved from GO, KEGG, or PubMed.
   - Example: "Gene 'Ghir_D11G004620' with 97.829% similarity is annotated in GO as 'GO:0009507 (photosynthesis).' Retrieved from Gene Ontology database."

5. **Co-expression Data** (Supporting Confidence):
   - **Purpose**: Explore functional associations through co-expression with genes of known functions.
   - **Usage**: Co-expression data serves as further validation, especially when corroborating TWAS and expression data findings. Use co-expression to suggest pathway involvement or related functions when other data sources are weak.

6. **GO Data** (High Confidence):
   - **Purpose**: Use provided GO annotations to identify biological processes, molecular functions, or cellular components associated with the gene.
   - **Usage**: GO annotations directly support functional roles of the gene based on provided data.

7. **KEGG Pathway Data** (High Confidence):
   - **Purpose**: Use provided KEGG pathways to describe metabolic or regulatory pathways involving the gene.
   - **Usage**: KEGG pathways contextualize gene function in broader biochemical networks or stress responses.

### **Inference Paths for Gene '{gene_id}'**:
Follow these paths based on available data, using each source as evidence to confirm or elaborate predictions. Integrate multiple paths when they reinforce each other, and continue gathering support from all relevant data types even after forming initial predictions.

- **Path 1** (Direct TWAS Association): If TWAS data shows a strong association, form a primary hypothesis. Validate with expression data to identify tissue-specific activity, focusing on whether the gene is upregulated or downregulated in relevant tissues or conditions. Use homolog data to refine these predictions.Note: Information from web-searched papers should not be included in the output.
...
"""

        return prompt

    # Get BLAST data
    def get_blast_data(self, gene_id):
        blast_collection = db['gene_blast_similarity']
        blast_results = blast_collection.find({"gene_id": gene_id})
        
        if blast_collection.count_documents({"gene_id": gene_id}) == 0:
            return f"No BLAST data found for gene {gene_id}.", []
        
        description_list = []
        similar_genes = []
        
        for result in blast_results:
            target_gene = result['similarity_matches']['target_gene']
            similarity = result['similarity_matches']['similarity']
            description = f"Gene '{gene_id}' has a similarity of {similarity:.3f} with gene '{target_gene}'."  # Convert to text description
            description_list.append(description)
            similar_genes.append(target_gene)
        
        return "\n".join(description_list), similar_genes

    # Get co-expression data
    def get_coexpression_data(self, gene_id):
        coexpression_collection = db['gene_coexpression']
        coexpression_result = coexpression_collection.find_one({"gene_id": gene_id})
        
        if not coexpression_result:
            return f"No coexpression data found for gene {gene_id}.", []
        
        coexpressions = coexpression_result.get("coexpressed_genes", [])
        description_list = []
        high_weight_genes = []
        
        for coexpression in coexpressions:
            related_gene = coexpression['gene_id']
            weight = coexpression['weight']
            description = f"Gene '{gene_id}' is co-expressed with gene '{related_gene}' with a co-expression weight of {weight:.6f}."
            description_list.append(description)
            high_weight_genes.append(related_gene)
        
        return "\n".join(description_list), high_weight_genes

    # Get expression data
    def get_expression_data(self, gene_id):
        expression_collection = db['gene_expression']
        expression_result = expression_collection.find_one({"gene_id": gene_id})
        
        if not expression_result:
            return f"No expression data found for gene {gene_id}."
        
        tissue_expression = expression_result.get("tissue_expression", {})
        description_list = []
        for tissue, expression_value in tissue_expression.items():
            description = f"Gene '{gene_id}' has an expression level of {expression_value:.6f} in '{tissue}'."  # Convert to text description
            description_list.append(description)
        
        return "\n".join(description_list)

    # Get homologous gene data
    def get_homologous_gene_data(self, gene_id):
        homologous_genes_collection = db['homologous_genes']
        homologous_result = homologous_genes_collection.find_one({"gene_id": gene_id})
        
        if not homologous_result:
            return f"No homologous gene data found for gene {gene_id}."
        
        homologous_gene = homologous_result.get("homologous_gene", "Unknown")
        arabidopsis_symbol = homologous_result.get("arabidopsis_symbol", "Unknown")
        chromosome = homologous_result.get("chromosome", "Unknown")
        location_start = homologous_result.get("location_start", "Unknown")
        location_end = homologous_result.get("location_end", "Unknown")
        full_name = homologous_result.get("full_name", "Unknown")
        function_description = homologous_result.get("function_description", "Unknown")
        
        description = (f"Gene '{gene_id}' has a homologous gene in Arabidopsis thaliana, "
                       f"'{homologous_gene}' with symbol '{arabidopsis_symbol}'.\n"
                       f"Chromosome location: {chromosome} from {location_start} to {location_end}.\n"
                       f"Full name: {full_name}.\n"
                       f"Function: {function_description}.")
        return description

    # Get TWAS data
    def get_twas_data(self, gene_id):
        twas_collection = db['gene_trait_twas']
        twas_result = twas_collection.find_one({"gene_id": gene_id})
        
        if not twas_result:
            return f"No TWAS data found for gene {gene_id}."
        
        traits = twas_result.get("traits", [])
        description_list = []
        for trait in traits:
            phenotype = trait['phenotype']
            stage = trait['stage']
            zscore = trait['twas_zscore']
            description_list.append(f"At '{stage}' stage, the gene is associated with '{phenotype}' with a TWAS Z-score of {zscore:.4f}.")
        
        return "\n".join(description_list)

    # Get GO data
    def get_go_data(self, gene_id):
        go_data = db.go_data.find({"gene_id": gene_id})
        descriptions = []
        for go in go_data:
            descriptions.append(f"GO term '{go['go_term']}' ({go['ontology']}): {go['description']}")
        if descriptions:
            return "The gene is associated with the following Gene Ontology (GO) terms: " + "; ".join(descriptions)
        return "No GO data available for the target gene."

    # Get KEGG data
    def get_kegg_data(self, gene_id):
        kegg_data = db.kegg_data.find({"gene_id": gene_id})
        descriptions = []
        for kegg in kegg_data:
            descriptions.append(f"KEGG pathway '{kegg['kegg_pathway']}': {kegg['kegg_description']}")
        if descriptions:
            return "The gene is involved in the following KEGG pathways: " + "; ".join(descriptions)
        return "No KEGG data available for the target gene."
