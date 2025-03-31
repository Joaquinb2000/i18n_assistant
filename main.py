import os
import readline
from pathlib import Path

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from src.I18nAssistant import I18nAssistant
from src.utils import update_file_code, update_locale_file

load_dotenv()

home = Path.home()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")
I18nAssistant = I18nAssistant(llm, 'vue', '$t', 'vue')

LOCALE_FILE_PATH = os.getenv('LOCALE_FILE_PATH')

def main(file_path):
    relative_path = os.path.join(home, file_path)

    with open(relative_path) as file:
        code, yaml = I18nAssistant.generate_localized_code(file, file.name)

    update_file_code(code, relative_path)
    update_locale_file(yaml, LOCALE_FILE_PATH)
    
if __name__ == '__main__':
    while True:
        file_path = input("Input file path please: ")
        main(file_path)
        print(f"Sucessfully localized {file_path}!")

        