import requests
from bs4 import BeautifulSoup
import os
import sys
from llama import llama

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
        # print(title)
        # print(tags)
        # print(parameter_sizes)
        # print("-----")
        models_data.append({
            'name': title,
            'parameter_sizes': parameter_sizes,
            'tags': tags
        })

    return models_data


def create_markdown():
    table_format = "| Model Name | Category | Parameter Sizes |\n|------------------|-------------|-------------|\n"
    models = get_models()
    for model in models:
        name = model['name']
        sizes = ", ".join(model['parameter_sizes']) if model['parameter_sizes'] else "N/A"
        categories = ", ".join(model['tags']) if model['tags'] else "N/A"
        table_format += f"| {name} | {categories} | {sizes} |\n"

    with open("AVAILABLE_MODELS.md", "w") as f:
        f.write("# Available Ollama Models\n\n")
        f.write("This document lists the available models from Ollama along with their categories and parameter sizes.\n\n")
        f.write(table_format)

if __name__ == "__main__":
    create_markdown()