import pandas as pd

class GOProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        """
        Main processing method, loads GO data and converts it to a textual description format.
        """
        print(f"Processing GOProcessor...")
        try:
            # Load GO data
            df = pd.read_csv(self.input_path)
            
            # Convert to textual description format
            with open(self.output_path, 'w', encoding='utf-8') as file:
                for _, row in df.iterrows():
                    gene_id = row['GeneID']
                    go_term = row['GO']
                    ontology = row['Ontology']
                    description = row['Description']
                    file.write(
                        f"Gene: '{gene_id}'\n"
                        f"GO Term: '{go_term}'\n"
                        f"Ontology: '{ontology}'\n"
                        f"Description: '{description}'\n"
                        "---\n"
                    )
            print(f"Finished processing GOProcessor")
            
        except Exception as e:
            print(f"Error processing GO data: {e}")
