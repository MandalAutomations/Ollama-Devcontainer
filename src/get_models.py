import requests
from bs4 import BeautifulSoup

def get_models():
    url = "https://ollama.com/library"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    model_cards = soup.select("a[href^='/library/']")
    models_data = []
    for card in model_cards:
        div = card.find('div', {'class': 'flex flex-col', 'x-test-model-title': ''})
        title = div.get('title')
        updated = card.find('span', attrs={'x-test-updated': ''})
        updated = updated.get_text(strip=True) if updated else "N/A"
        
        spans_div = card.find('div', class_='flex flex-wrap space-x-2')
        parameter_sizes = []
        tags = []
        
        if spans_div:
            spans = spans_div.find_all('span')
            for span in spans:
                if 'bg-indigo-50' in span.get('class', []):
                    tags.append(span.get_text().strip()) 
                elif 'bg-[#ddf4ff]' in span.get('class', []):
                    parameter_sizes.append(span.get_text().strip())

        models_data.append({
            'name': title,
            'parameter_sizes': parameter_sizes,
            'tags': tags,
            'last_updated': updated
        })

    return models_data

def create_markdown():
    table_format = "| Model Name | Category | Parameter Sizes | Last Updated |\n|------------------|-------------|-------------|----------------|\n"
    models = get_models()
    for model in models:
        name = model['name']
        sizes = ", ".join(model['parameter_sizes']) if model['parameter_sizes'] else "N/A"
        categories = ", ".join(model['tags']) if model['tags'] else "N/A"
        last_updated = model['last_updated']
        table_format += f"| {name} | {categories} | {sizes} | {last_updated} |\n"

    with open("AVAILABLE_MODELS.md", "w") as f:
        f.write("# Available Ollama Models\n\n")
        f.write("This document lists the available models from Ollama along with their categories and parameter sizes.\n\n")
        f.write(table_format)

if __name__ == "__main__":
    create_markdown()