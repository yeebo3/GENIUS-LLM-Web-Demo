import pandas as pd

class KEGGProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        """
        Load KEGG data and convert it to a textual description format.
        """
        try:
            # Load KEGG data
            df = pd.read_csv(self.input_path)
            print(f"Processing KEGGProcessor...")

            # Convert to textual description format
            with open(self.output_path, 'w', encoding='utf-8') as file:
                for _, row in df.iterrows():
                    gene_id = row['GeneID']
                    pathway = row['KEGG']
                    description = row['KEGG_Description']
                    file.write(
                        f"Gene: '{gene_id}'\n"
                        f"Pathway: '{pathway}'\n"
                        f"Description: '{description}'\n"
                        "---\n"
                    )
            print(f"Finished processing KEGGProcessor")
        except Exception as e:
            print(f"Error processing KEGG data: {e}")
