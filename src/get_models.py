# import requests
# from bs4 import BeautifulSoup
# import os
# import sys
# from src.llama import llama

# def get_models():
#     url = "https://ollama.com/library"
#     response = requests.get(url)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, 'html.parser')
#     model_cards = soup.select("a[href^='/library/']")
#     models_data = []

#     print(model_cards[0])
#     # for card in model_cards:
#     #     name = card.text.strip()
#     #     href = card.get("href")

#     #     print(name)
#     #     models_data.append({
#     #         "Model Name": name,
#     #         "Parameter Sizes": "?",      # Needs additional scraping if available
#     #         "Category": "?",             # Could use name to guess or check model page
#     #         "Last Updated": "?"          # Not shown on main page, possibly in subpages
#     #     })

#     return models_data


# # def create_markdown():
# #     OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
# #     MODEL = "gemma3:1b" # Find available models here https://ollama.com/library
    
# #     llama_instance = llama(OLLAMA_HOST, MODEL)
# #     llama_instance.check_and_pull_model()

# #     table_format = "| Model Name | Parameter Sizes | Category | Last Updated |\n|------------|-------------|-------------|-------------|\n"
# #     models = get_models()

# #     prompt = f"Generate a markdown table in this format {table_format} from the following text: {models}"

# #     response = llama_instance.generate_response(prompt)
# #     print(response)

# # if __name__ == "__main__":
# #     create_markdown()

# get_models()

from playwright.sync_api import sync_playwright

# playwright install
# playwright install-deps

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://ollama.com/library")
    page.screenshot(path="website_screenshot.png", full_page=True)
    browser.close()