import cloudscraper
import prompt_generate

def get_gene_input():
    """Get Gene ID"""
    return input("Please enter the gene ID for prediction: ")

def call_openai_api(prompt):
    # For optimal results, it is recommended to use an API key that can access the following model.
    url = ""  # The API endpoint URL
    api_key = ""  # Your OpenAI API key

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-2024-11-20",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant specialized in gene prediction."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 15000
    }

    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # 检查截断情况并处理续写
        if data["choices"][0].get("finish_reason") == "length":
            followup_prompt = [{"role": "assistant", "content": content}]
            payload["messages"].extend(followup_prompt)
            followup_response = scraper.post(url, headers=headers, json=payload)
            followup_response.raise_for_status()
            followup_data = followup_response.json()
            content += followup_data["choices"][0]["message"]["content"]

        return content
    except Exception as e:
        return f"Error calling API: {e}"

if __name__ == "__main__":
    gene_id = get_gene_input()
    try:
        prompt = prompt_generate.generate_structured_prompt_with_natural_language(gene_id)
    except Exception as e:
        print(f"Error generating prompt: {e}")
        exit(1)
    
    result = call_openai_api(prompt)

    print("\n=== Prediction Result ===\n", result)
