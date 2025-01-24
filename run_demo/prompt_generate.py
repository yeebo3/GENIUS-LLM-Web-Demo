from pymongo import MongoClient

# connect your  MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cotton_gene_database']

#  BLAST
def get_blast_data(gene_id):
    blast_collection = db['gene_blast_similarity']
    blast_results = blast_collection.find({"gene_id": gene_id})
    
    if blast_collection.count_documents({"gene_id": gene_id}) == 0:
        return f"No BLAST data found for gene {gene_id}.", []
    
    description_list = []
    similar_genes = []
    
    for result in blast_results:
        target_gene = result['similarity_matches']['target_gene']
        similarity = result['similarity_matches']['similarity']
        description = f"Gene '{gene_id}' has a similarity of {similarity:.3f} with gene '{target_gene}'."  # 转换为文本描述
        description_list.append(description)
        similar_genes.append(target_gene)
    
    return "\n".join(description_list), similar_genes

# coexpression
def get_coexpression_data(gene_id):
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

# expression
def get_expression_data(gene_id):
    expression_collection = db['gene_expression']
    expression_result = expression_collection.find_one({"gene_id": gene_id})
    
    if not expression_result:
        return f"No expression data found for gene {gene_id}."
    
    tissue_expression = expression_result.get("tissue_expression", {})
    description_list = []
    for tissue, expression_value in tissue_expression.items():
        description = f"Gene '{gene_id}' has an expression level of {expression_value:.6f} in '{tissue}'."  # 转换为文本描述
        description_list.append(description)
    
    return "\n".join(description_list)

# homologous
def get_homologous_gene_data(gene_id):
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

# twas
def get_twas_data(gene_id):
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
    # GO
def get_go_data(gene_id):
    go_data = db.go_data.find({"gene_id": gene_id})
    descriptions = []
    for go in go_data:
        descriptions.append(f"GO term '{go['go_term']}' ({go['ontology']}): {go['description']}")
    if descriptions:
        return "The gene is associated with the following Gene Ontology (GO) terms: " + "; ".join(descriptions)
    return "No GO data available for the target gene."

# KEGG
def get_kegg_data(gene_id):
    kegg_data = db.kegg_data.find({"gene_id": gene_id})
    descriptions = []
    for kegg in kegg_data:
        descriptions.append(f"KEGG pathway '{kegg['kegg_pathway']}': {kegg['kegg_description']}")
    if descriptions:
        return "The gene is involved in the following KEGG pathways: " + "; ".join(descriptions)
    return "No KEGG data available for the target gene."
#  hIGH WEIGHT GENES
def get_related_genes_data(gene_data):
    related_genes_data = {}

    for similar_blast_gene in gene_data['similar_blast_genes']:
        related_genes_data[similar_blast_gene] = {
            "blast_data": get_blast_data(similar_blast_gene)[0],
            "coexpression_data": get_coexpression_data(similar_blast_gene)[0],
            "expression_data": get_expression_data(similar_blast_gene),
            "homologous_data": get_homologous_gene_data(similar_blast_gene),
            "twas_data": get_twas_data(similar_blast_gene),
            "go_data": get_go_data(similar_blast_gene),
            "kegg_data": get_kegg_data(similar_blast_gene)
        }

    for high_weight_gene in gene_data['high_weight_genes']:
        related_genes_data[high_weight_gene] = {
            "blast_data": get_blast_data(high_weight_gene)[0],
            "coexpression_data": get_coexpression_data(high_weight_gene)[0],
            "expression_data": get_expression_data(high_weight_gene),
            "homologous_data": get_homologous_gene_data(high_weight_gene),
            "twas_data": get_twas_data(high_weight_gene),
            "go_data": get_go_data(high_weight_gene),
            "kegg_data": get_kegg_data(high_weight_gene)
        }

    return related_genes_data


def generate_structured_prompt_with_natural_language(gene_id):
    prompt = f"""
### **Task Overview**:
You are tasked with predicting the biological function of the target gene '{gene_id}' by analyzing multiple datasets. 
Provide a detailed prediction of the gene's function, associated biological processes, and relevant traits.

### **Data for Target Gene '{gene_id}'**:
"""

    blast_data, similar_blast_genes = get_blast_data(gene_id)
    prompt += f"""
#### **BLAST Similarity Data**:
{blast_data}

This section presents the sequence similarity between the target gene and other genes. The higher the similarity, the more likely it is that the genes share evolutionary history and possibly similar functions.

- **Purpose**: Identify genes with sequence similarity to the target gene. High similarity suggests shared evolutionary history or potential functional similarities. 
- **Task**: Analyze this data to infer possible shared functions between the target gene and similar genes.
"""

    coexpression_data, high_weight_genes = get_coexpression_data(gene_id)
    prompt += f"""
#### **Co-expression Data**:
{coexpression_data}

This data shows the genes that are co-expressed with the target gene. Co-expression often indicates that these genes work together in the same biological pathways or processes.

- **Purpose**: Identify genes that are co-expressed with the target gene. Genes with similar expression patterns may participate in similar biological pathways or processes.
- **Task**: Use co-expression data to hypothesize the involvement of the target gene in specific biological pathways.
"""

    expression_data = get_expression_data(gene_id)
    prompt += f"""
#### **Gene Expression Data Across Different Tissues**:
{expression_data}

This data provides the expression levels of the target gene in different plant tissues. Understanding where the gene is expressed can offer clues about its biological role.

- **Purpose**: Understand where and when the target gene is expressed in different plant tissues. Tissue-specific expression can provide insights into the gene's role in specific biological functions or developmental stages.
- **Task**: Correlate expression patterns with tissue-specific functions to refine your functional prediction.
"""

    homologous_data = get_homologous_gene_data(gene_id)
    prompt += f"""
#### **Homologous Gene Data**:
{homologous_data}

This data provides information about homologous genes in Arabidopsis thaliana. Homologous genes often retain similar functions across species, so this can provide valuable insights into the target gene's function.

- **Purpose**: Use information from homologous genes in **Arabidopsis thaliana** (a model plant) to infer potential functions. Homologous genes often retain similar functions across species.
- **Task**: Leverage the functional annotation of homologous genes to predict the potential function of the target gene in cotton.
"""

    twas_data = get_twas_data(gene_id)
    prompt += f"""
#### **TWAS Data**:
{twas_data}

This data shows associations between the gene and traits based on transcriptome-wide association studies (TWAS). It helps link gene expression to specific traits, such as fiber development stages.

- **Purpose**: Identify statistical associations between the target gene and specific traits. This data links gene expression to traits, such as fiber development stages.
- **Task**: If available, use TWAS data to strengthen or validate the predicted gene-trait associations.
"""


    go_data = get_go_data(gene_id)
    prompt += f"""
#### **Gene Ontology (GO) Data**:
{go_data}

This section describes the GO terms associated with the target gene, including biological processes, molecular functions, and cellular components. GO terms provide structured and comprehensive descriptions of gene functions.

- **Purpose**: Use GO annotations to understand the functional roles of the target gene in biological processes, molecular activities, and its cellular localization.
- **Task**: Analyze GO terms to refine your prediction of the gene's biological roles, molecular mechanisms, and interactions within cellular contexts.
"""

    kegg_data = get_kegg_data(gene_id)
    prompt += f"""
#### **KEGG Pathway Data**:
{kegg_data}

This section presents the KEGG pathways in which the target gene is involved. KEGG pathways represent metabolic networks, biochemical pathways, and cellular processes that help interpret the gene's role in broader biological contexts.

- **Purpose**: Explore how the target gene contributes to metabolic or biochemical pathways. Pathway involvement can indicate the gene's specific role in cellular and physiological functions.
- **Task**: Use KEGG pathway data to hypothesize the gene's involvement in specific metabolic or regulatory pathways, and relate these roles to its biological significance.
"""

    prompt += """
---

### **Data for Related Genes**:
Below are related genes identified based on BLAST similarity or co-expression data. These genes may provide further insights into the function of the target gene.

"""
    related_genes_data = get_related_genes_data({"similar_blast_genes": similar_blast_genes, "high_weight_genes": high_weight_genes})
    for related_gene, related_data in related_genes_data.items():
        prompt += f"\n\n### Data for Related Gene '{related_gene}':\n"
        prompt += f"- **BLAST Similarity Data**: {related_data['blast_data']}\n"
        prompt += f"- **Co-expression Data**: {related_data['coexpression_data']}\n"
        prompt += f"- **Gene Expression Data**: {related_data['expression_data']}\n"
        prompt += f"- **Homologous Gene Data**: {related_data['homologous_data']}\n"
        prompt += f"- **TWAS Data**: {related_data['twas_data']}\n"
        prompt += f"- **GO Data**: {related_data['go_data']}\n"
        prompt += f"- **KEGG Data**: {related_data['kegg_data']}\n"



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

#### **4. Integration with External Knowledge**:
- Perform supplementary online searches and retrieve evidence from:
  - **PubMed literature citations**,
  - **Protein-protein interaction networks** (e.g., STRING),
  - **Plant-specific databases** (e.g., PlantTFDB).
- It is mandatory to retrieve and include specific data points from online databases or literature in the output.
- Examples of required data include:
  1. STRING protein-protein interaction data, including interaction confidence scores and involved proteins.
  2. PlantTFDB transcription factor annotations, highlighting regulatory roles.

- For each retrieved data point:
  - Explicitly cite the source (e.g., "STRING Interaction: interacting with stress-related proteins, confidence score: 0.82").
  - Indicate whether the data supports or challenges local predictions.
- Retrieve at least three specific data points related to the target gene from online resources and explicitly describe how each one contributes to the prediction.
- For example:
  - "STRING Interaction: interacting with stress-related proteins (confidence score: 0.82), retrieved from STRING, supports the hypothesis that the gene plays a role in abiotic stress response."
  - "PlantTFDB Annotation: transcription factor involved in drought response, retrieved from PlantTFDB, aligns with high expression levels in drought-related tissues."

#### **5. Upregulation/Downregulation Analysis**:
- Use gene expression data to analyze whether gene '{gene_id}' is upregulated or downregulated under specific conditions.
- Correlate observed trends with potential biological roles, e.g.:
  - **Upregulation**: Active involvement in processes like stress response or development.
  - **Downregulation**: Reduced activity or suppression in certain pathways or conditions.
- Cross-reference local findings with external annotations (e.g., GO terms, KEGG pathways).
  
#### **6. Step-by-Step Reasoning**:
- Provide a structured explanation showing how each dataset contributes to your prediction. Use logical connectors like "Firstly," "Furthermore," and "Lastly" for clarity.

---

### **Task Overview**:
You are tasked with predicting the biological function of the target gene '{gene_id}' by analyzing multiple datasets. Use the following datasets in order of priority to infer the gene's function, associated biological processes, and relevant traits. To strengthen the prediction, integrate evidence from **all available data sources** where possible, even if high-priority data already suggests a strong hypothesis.


### **Data for Target Gene '{gene_id}'**:
- For each supporting evidence type (e.g., BLAST, co-expression, expression data),all need supplement with external data:
#### Data Sources (Ordered by Priority):
1. **TWAS Data** (High Confidence):
   - **Purpose**: Directly associate the gene with specific traits via statistical associations. High Z-scores indicate stronger associations.
   - **Usage**: TWAS associations take precedence and form the initial basis of predictions. However, use other datasets to validate and enhance confidence in TWAS-based associations.
   - Use external KEGG pathways or STRING interactions to explain observed trait associations.
   - Example: "KEGG: Pathway 'Secondary Metabolite Biosynthesis' suggests the gene is involved in cotton's fiber strength."

2. **Homologous Gene Data** (Medium-High Confidence):
   - **Purpose**: Use homologous gene functions in model organisms to support functional predictions.
   - **Usage**: Homologous gene data can strengthen TWAS predictions or provide standalone insights in absence of TWAS. When TWAS and homologous data are aligned, continue to examine additional datasets to add support and detail.

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

- **Path 1** (Direct TWAS Association): If TWAS data shows a strong association, form a primary hypothesis. Validate with expression data to identify tissue-specific activity, focusing on whether the gene is upregulated or downregulated in relevant tissues or conditions. Use homolog data to refine these predictions.

- **Path 2** (Homolog-Based Inference): Align homologous gene functions with TWAS or expression data for robust predictions. Pay attention to whether homologous genes display regulatory roles (e.g., upregulation or downregulation) in similar pathways.

- **Path 3** (Expression Validation): Use expression patterns to validate trait predictions from TWAS or homolog data. Explicitly analyze tissue-specific upregulation or downregulation trends and correlate these with traits such as stress response or developmental processes.

- **Path 4** (Sequence Similarity via BLAST): Use BLAST to reinforce indirect associations. For genes with high sequence similarity, consider whether similar expression trends (upregulation/downregulation) occur under comparable conditions.

- **Path 5** (Indirect Association via Co-expression): Use co-expression as supplementary support, especially when other data types suggest a function. Investigate if co-expressed genes share similar upregulation or downregulation patterns under specific conditions.

- **Path 6** (Integration of External Knowledge): Use web-based research to validate findings from local datasets. Integrate knowledge from Gene Ontology, KEGG pathways, and relevant publications to confirm predicted functions or to uncover novel roles for gene '{gene_id}'.

- **Path 7** (GO and KEGG-Based Inference): 
   - **GO Data**: Use provided Gene Ontology annotations to directly identify biological processes, molecular functions, or cellular components related to the gene. Highlight functional annotations that align with other data sources (e.g., TWAS, homologs).
   - **KEGG Data**: Analyze metabolic or regulatory pathways involving the gene. Use KEGG pathways to identify the gene's role in stress responses, development, or biochemical networks.

### **Conflict Resolution**:
If different paths yield conflicting predictions, apply these strategies:

1. **Priority Weighting**:
   - Give precedence to higher-confidence sources in the following order: 
     - TWAS > Homolog > GO and KEGG > Expression > Upregulation/Downregulation Analysis > BLAST > Co-expression.
   - Prioritize data that has strong statistical or experimental support (e.g., TWAS Z-scores, peer-reviewed functional studies, well-curated GO terms, or KEGG pathways).

2. **Consensus Building**:
   - Seek support from multiple data sources. Even if high-priority data is available, supporting evidence from lower-priority sources can increase robustness.
   - Integrate data that aligns across datasets (e.g., TWAS, homologs, GO terms, and KEGG pathways) and explicitly state areas of agreement.

3. **Biological Plausibility**:
   - Choose predictions that align best with known biological roles. For example:
     - If KEGG pathways suggest involvement in a specific metabolic process, prioritize this evidence over weaker co-expression trends.
     - Ensure that predicted upregulation/downregulation patterns match known physiological mechanisms or developmental stages.

4. **External Validation**:
   - Use external knowledge sources (e.g., STRING, PlantTFDB) to resolve ambiguities and validate the most plausible prediction. Avoid relying on external GO or KEGG sources, as local data provides sufficient annotations.
   - If external data supports local evidence, explicitly state this alignment to strengthen the prediction.

5. **Exclusion of Inconsistencies**:
   - If certain datasets consistently conflict with high-confidence sources and lack biological plausibility:
     - Exclude them from final predictions.
     - Document the rationale for exclusion (e.g., species-specific differences, experimental limitations).

6. **Contradictions Between Local and External Data**:
   - If external data contradicts local evidence, follow these steps:
     1. Evaluate the reliability and relevance of both sources.
     2. Prioritize data aligning with known biological principles or higher confidence (e.g., peer-reviewed literature over co-expression data).
     3. Clearly document contradictions and suggest potential reasons for discrepancies, such as:
        - Species-specific differences in gene function.
        - Variability in experimental conditions or sample types.

---

### Additional Instructions:
- Analyze the provided data to predict if the gene is upregulated or downregulated for specific traits or functions.
- Provide a detailed step-by-step explanation of your prediction process.
- Use gene expression levels across tissues to identify whether the target gene is likely upregulated or downregulated under specific biological or environmental conditions.
- Incorporate GO and KEGG data to identify biological processes, molecular functions, cellular components, and pathways related to the gene. Highlight how these annotations support predictions derived from other datasets (e.g., TWAS, homologs, expression).
- Correlate findings from GO and KEGG with gene expression trends to strengthen hypotheses about the gene's role in traits or functions.

---

### **Expected Output Format**:
- For each section (e.g., predicted function, traits, evidence), include:
  1. Specific insights derived from provided datasets.
  2. Explanation of how the data supports or challenges the prediction.
  3. Integration of GO and KEGG annotations with other datasets to build a robust hypothesis.

The output should include the following sections:

1. **Predicted Function and Traits**:
   - Provide a clear and concise statement of the predicted function(s) and associated trait(s) for gene '{gene_id}'.
   - Highlight the roles suggested by GO and KEGG data, explicitly linking them to the predicted traits or functions.

2. **Explanation of Reasoning**:
   - Offer a comprehensive narrative that cohesively integrates the evidence from various data sources, explaining each source's specific contribution to the prediction.
   - Explicitly discuss upregulation or downregulation trends and their relevance to the gene's predicted function.
   - Emphasize how GO and KEGG annotations complement findings from TWAS, homologous genes, and expression data.
   - Use structured connectors such as “Firstly,” “Additionally,” and “Lastly” to delineate the logical steps in the reasoning process.

3. **Upregulation/Downregulation Predictions**:
   - Clearly state whether gene '{gene_id}' is upregulated or downregulated in specific tissues or conditions, and explain the biological implications.
   - Analyze whether gene '{gene_id}' is likely to be upregulated or downregulated under specific conditions or tissues based on:
     1. Gene expression data provided in the local datasets.
     2. GO annotations for biological processes or stress responses related to differential expression.
     3. KEGG pathway roles that may highlight regulatory or metabolic functions.
   - For each trend, provide:
     - A clear statement of whether the gene is upregulated or downregulated.
     - Supporting evidence from the provided GO and KEGG annotations.
     - Implications of the upregulation or downregulation in the context of the gene's function and traits.
   - Use GO terms to identify stress responses, regulatory roles, or developmental processes that align with the observed expression trends.
   - Analyze KEGG pathways for their relevance to tissue-specific activity, metabolic networks, or broader physiological functions.

4. **Integration of GO and KEGG Data**:
   - Summarize how GO and KEGG annotations support or refine the predictions for gene '{gene_id}'.
   - Highlight GO terms that explicitly describe the gene's role in specific biological processes or molecular functions.
   - Use KEGG pathways to explain the gene's involvement in metabolic or regulatory pathways and their connection to observed traits.

5. **External Validation**:
   - Supplement predictions with insights from external knowledge sources, excluding GO and KEGG data. These sources may include:
     1. Protein-protein interaction networks (e.g., STRING) for identifying interaction partners.
     2. Plant-specific databases (e.g., PlantTFDB) for transcription factor roles or regulatory functions.
   - Example:
     - "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.82), retrieved from STRING, supports the hypothesis of involvement in abiotic stress response."
     - "PlantTFDB Annotation: Transcription factor involved in drought response, retrieved from PlantTFDB, aligns with high expression levels in drought-related tissues."

---

### **Data Sources**:
1. **Gene Ontology (GO)**:
   - Use provided annotations to identify biological processes, molecular functions, and cellular components associated with the target gene.
   - Example: "GO Annotation: GO:0009414 (response to water deprivation), provided in the dataset, highlights involvement in stress responses."

2. **KEGG Pathways**:
   - Use provided pathways to identify metabolic or regulatory roles associated with the target gene.
   - Example: "KEGG Pathway: 'Plant Hormone Signal Transduction,' provided in the dataset, suggests involvement in auxin-mediated signaling pathways."

3. **Protein-Protein Interaction Networks**:
   - Use STRING or similar databases to identify interactions involving the target gene.
   - Example: "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.82), retrieved from STRING, supports the hypothesis of involvement in abiotic stress response."

4. **Plant-Specific Databases**:
   - Search for transcription factor roles or other regulatory functions in PlantTFDB or similar resources.
   - Example: "PlantTFDB Annotation: Transcription factor involved in fiber development, retrieved from PlantTFDB."

---

#### **Task Steps**:
To validate and integrate all evidence, including KEGG and GO data, follow these steps in order:

1. **Identify Relevant Data Sources**:
   - Use local datasets to extract annotations, pathways, and interactions related to the target gene or its homologs.
   - Sources include:
     - **GO Annotations**: Provided biological processes, molecular functions, and cellular components.
     - **KEGG Pathways**: Provided pathways representing metabolic or regulatory roles.
     - Protein-protein interactions (e.g., STRING).
     - Transcription factor functions (e.g., PlantTFDB).

2. **Retrieve Specific Data Points**:
   - Extract and record relevant data, such as:
     - GO annotations from the provided dataset.
     - KEGG pathway memberships from the provided dataset.
     - Protein-protein interactions from STRING.
     - Transcription factor roles or regulatory functions from PlantTFDB.

3. **Organize Evidence with Clear References**:
   - Ensure each data point is accompanied by a description and a reference to its source. Example formats include:
     - "GO Annotation: GO:0009414 (response to water deprivation), provided in the dataset."
     - "KEGG Pathway: 'Plant Hormone Signal Transduction,' provided in the dataset."
     - "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.82), retrieved from STRING."
     - "PlantTFDB Annotation: Transcription factor involved in drought response, retrieved from PlantTFDB."

4. **Integrate Local Data (Including GO and KEGG)**:
   - Combine GO and KEGG data with other local evidence (e.g., TWAS, expression, homologs) to reinforce predictions.
   - Explicitly state whether the data supports or contradicts the hypothesis:
     - If GO annotations highlight biological processes aligned with expression data or TWAS findings, use this alignment to strengthen predictions.
     - If KEGG pathways suggest metabolic roles that contradict homolog functions, evaluate pathway relevance and propose possible explanations.

5. **Resolve Conflicts Between Evidence**:
   - If data from different sources (e.g., GO vs. expression) presents conflicting predictions:
     - Evaluate the reliability and biological plausibility of each source.
     - Prioritize data that aligns with known biological mechanisms or robust statistical evidence.
     - Document discrepancies and suggest potential reasons, such as species-specific differences or data limitations.

6. **Prioritize Biological Plausibility**:
   - Assign higher priority to data that aligns with:
     - Known biological mechanisms (e.g., stress response pathways in KEGG or regulatory roles in GO).
     - Statistical robustness (e.g., TWAS Z-scores or high-confidence protein-protein interactions).
     - Peer-reviewed annotations in GO, KEGG, or literature.

---

#### **Expected Results**:
Summarize the insights derived from all datasets, including GO and KEGG annotations, and explain how they integrate with other evidence. Example outputs include:

- **GO Annotations**:
  - "GO Annotation: GO:0009414 (response to water deprivation), provided in the dataset, highlights the gene's involvement in abiotic stress responses."
  - "GO Annotation: GO:0045893 (positive regulation of transcription), provided in the dataset, aligns with upregulation trends in key tissues."

- **KEGG Pathways**:
  - "KEGG Pathway: 'Plant Hormone Signal Transduction,' provided in the dataset, suggests the gene plays a role in auxin-mediated signaling during fiber development."
  - "KEGG Pathway: 'Secondary Metabolite Biosynthesis,' provided in the dataset, highlights involvement in metabolic processes critical for stress adaptation."

- **STRING Interactions**:
  - "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.82), retrieved from STRING, supports the hypothesis of involvement in stress response pathways."

- **PlantTFDB Annotations**:
  - "PlantTFDB Annotation: Transcription factor involved in drought response, retrieved from PlantTFDB, aligns with high expression levels in drought-related tissues."

Clearly indicate the alignment or conflict between KEGG/GO annotations and other evidence (e.g., expression, TWAS) to provide a robust final prediction.

---

#### **Confidence Assessment**:
- Indicate the confidence level of the prediction based on the consistency and strength of the evidence across datasets, including:
  - **High Confidence**: When KEGG pathways, GO annotations, and other local evidence (e.g., TWAS, expression) align to support a consistent prediction.
  - **Moderate Confidence**: When some evidence aligns but additional validation (e.g., homolog data or co-expression analysis) is required.
  - **Low Confidence**: When conflicting data cannot be resolved or when key datasets (e.g., expression or TWAS) are missing or inconclusive.

## **Example Output**:
### **Predicted Function and Traits**:
Gene '{gene_id}' is predicted to be involved in **drought stress response** and **fiber development**, functioning as a **negative regulator** in stress-mediated signaling pathways. This prediction is supported by multiple lines of evidence, including homologous gene data, tissue-specific expression patterns, co-expression networks, TWAS associations, BLAST similarity, and local annotations from Gene Ontology and KEGG pathways.
---
### **Supporting Evidence**:
#### **1. Homologous Gene Data**:
Firstly, homologous gene analysis provides strong evidence for the predicted function of '{gene_id}'. In **Arabidopsis thaliana**, the homologous gene '{arabidopsis_gene}' is associated with **drought tolerance** and **abiotic stress regulation**. This evolutionary conservation strongly implies that '{gene_id}' plays a similar role in cotton. 
Furthermore, functional annotations from local GO data provide additional support:
- "GO Annotation: GO:0009414 (response to water deprivation), provided in the dataset," highlights the gene's involvement in abiotic stress pathways.
In summary, the homologous gene data strongly indicates that '{gene_id}' functions in drought stress response and regulatory mechanisms.
---
#### **2. Gene Expression Data**:
Moreover, tissue-specific expression patterns reinforce the gene's role in fiber development and drought response:
- **High expression**:
  - In 'fiber_10DPA' (2.949739) and 'ovule' (17.467478), suggesting active involvement during critical stages of fiber differentiation and reproductive development.
- **Low expression**:
  - In 'root' (4.147105), indicating potential downregulation in root-specific functions under resource allocation strategies.
These patterns are further validated by GO terms provided in the dataset:
- "GO:0045893 (positive regulation of transcription), provided in the dataset," highlights tissue-specific regulatory activity.
Therefore, the expression data, combined with GO annotations, confirms the gene's dual role in fiber development and abiotic stress tolerance.
---
#### **3. Co-expression Data**:
Furthermore, co-expression analysis provides insights into the biological pathways involving '{gene_id}':
- **Key co-expressed genes**:
  - 'Gene_A' (weight: 0.921284) and 'Gene_B' (weight: 0.940514).
- These genes are known to participate in fiber development and stress response pathways, suggesting that '{gene_id}' collaborates with them in shared biological functions.
Additionally, data from STRING database supports these findings:
- "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.92)," indicates functional integration into stress-response pathways.
In conclusion, co-expression data provides robust evidence that '{gene_id}' is actively involved in fiber development and abiotic stress pathways.
---
#### **4. TWAS Data**:
TWAS analysis directly links '{gene_id}' to traits associated with fiber development and drought stress:
- **Key Traits and Stages**:
  - At 'fiber_20DPA' stage, the gene is associated with enhanced **fiber elongation** (Z-score: 2.8517).
  - At 'stress_condition' stage, the gene is linked to **drought tolerance** (Z-score: 3.7211), highlighting its regulatory role under abiotic stress.
These TWAS findings strongly support the hypothesis that '{gene_id}' is a key regulator of fiber development and stress response mechanisms.
---
#### **5. BLAST Similarity Data**:
Additionally, sequence similarity analysis highlights evolutionary relationships and functional parallels:
- '{gene_id}' shares **97.829% sequence similarity** with 'Gene_C', suggesting conserved functions in related pathways.
- KEGG pathway annotations link this similarity to the "Plant Hormone Signal Transduction" pathway, specifically in auxin-mediated signaling processes critical for fiber tissues.
Thus, BLAST similarity data further corroborates the predicted role of '{gene_id}' in stress and developmental processes.
---
#### **6. GO and KEGG Annotations**:
Local GO and KEGG annotations further strengthen the prediction for '{gene_id}':
- **Gene Ontology (GO)**:
  - "GO:0009414 (response to water deprivation), provided in the dataset," confirms the involvement of '{gene_id}' in abiotic stress tolerance.
  - "GO:0045893 (positive regulation of transcription), provided in the dataset," aligns with the gene's upregulation in specific tissues.
- **KEGG Pathways**:
  - "KEGG Pathway: 'Plant Hormone Signal Transduction,' provided in the dataset," highlights its role in auxin-mediated signaling in fiber tissues.
  - "KEGG Pathway: 'Secondary Metabolite Biosynthesis,' provided in the dataset," suggests involvement in metabolic processes critical for stress adaptation.
These annotations align seamlessly with other data, enhancing the confidence and robustness of the prediction.
---
### **Upregulation/Downregulation Analysis**:
Based on the expression data, '{gene_id}' exhibits the following regulatory trends:
1. **Upregulation**:
   - **In 'fiber_10DPA'**: High expression (2.949739) highlights active involvement in **fiber differentiation** during early developmental stages.
   - **In 'ovule'**: Exceptionally high expression (17.467478) indicates a critical regulatory role in **reproductive development**.
2. **Downregulation**:
   - **In 'root'**: Low expression (4.147105) suggests diminished activity in root-specific pathways, possibly due to **resource reallocation** during fiber development.
These trends are consistent with the gene's predicted roles and are validated by:
- "GO:0045893 (positive regulation of transcription), provided in the dataset," which supports tissue-specific activity during stress response.
- "KEGG Pathway: 'Secondary Metabolite Biosynthesis,' provided in the dataset," which aligns with the metabolic adjustments needed under stress.

#### **7. Integration with External Knowledge**:
Finally, external databases provide supplementary evidence to reinforce the local findings. These sources include:

- **Protein-Protein Interaction Networks**:
  - STRING and similar databases provide interaction data for the target gene, including confidence scores and functional relevance.
  - Example:
    - "STRING Interaction: Interacting with stress-related proteins (confidence score: 0.85), retrieved from STRING, supports involvement in abiotic stress pathways."
    - "STRING Interaction: Co-expression with known fiber development genes strengthens the hypothesis of developmental roles."

- **Plant-Specific Databases**:
  - Databases like PlantTFDB provide insights into transcription factor activity and regulatory roles of the target gene.
  - Example:
    - "PlantTFDB Annotation: Transcription factor activity associated with drought response, retrieved from PlantTFDB, aligns with high expression in drought-related tissues."
    - "PlantTFDB Annotation: Regulatory roles during fiber development confirmed through transcription factor analysis."

- **PubMed Literature**:
  - Search for publications discussing homologous genes or related pathways in cotton or other model species to validate hypotheses.
  - Example:
    - "PubMed Article: Regulatory roles of homologous genes in Arabidopsis suggest similar functions in stress responses, retrieved from PubMed."
    - "Literature Review: Studies in cotton reveal correlations between transcription factor activity and fiber quality."

---
### **Conclusion**:
In summary, integrating evidence from homologous gene data, expression patterns, co-expression networks, TWAS associations, BLAST similarity, and local annotations from KEGG and Gene Ontology, '{gene_id}' is predicted to function as a **key regulator in drought tolerance and fiber development**. Its **upregulation** in fiber and ovule tissues, combined with supporting data from local GO and KEGG annotations, confirms its critical role in cotton's agronomic traits and stress adaptation mechanisms.
### **Example Citations**:
1. "STRING Interaction: Interacting with known drought-response proteins (confidence score: 0.82), retrieved from STRING, supports the hypothesis of stress-response functions."
2. "PlantTFDB Annotation: Transcription factor involvement in fiber elongation, retrieved from PlantTFDB, aligns with high expression during developmental stages."
3. "PubMed Article: Homologous gene studies in Arabidopsis suggest regulatory roles in auxin signaling, retrieved from PubMed."

"""

    return prompt

def save_prompt_to_file(gene_id, file_path):
    prompt = generate_structured_prompt_with_natural_language(gene_id)
    with open(file_path, "w") as file:
        file.write(prompt)
    print(f"Prompt saved to {file_path}")