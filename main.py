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
BASE_TARGET_PATH = os.getenv('BASE_TARGET_PATH')

def main(file_path):
    relative_path = os.path.join(home, file_path)

    if(os.path.isdir(relative_path)):
        for path in os.listdir(relative_path):
            main(os.path.join(file_path, path))
    else:
        with open(relative_path) as file:
            code, yaml = I18nAssistant.generate_localized_code(file, file.name)

        update_file_code(code, relative_path)
        update_locale_file(yaml, LOCALE_FILE_PATH)
        print(f"Sucessfully localized {file_path}!")
    
if __name__ == '__main__':
    while True:
        file_path = input("Input file path please: ")

        if BASE_TARGET_PATH:
            file_path = "/".join([BASE_TARGET_PATH, file_path])

        main(file_path)

        