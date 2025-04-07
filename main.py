import os
import readline
from pathlib import Path

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from src.I18nAssistant import I18nAssistant
from src.utils import update_file_code, update_locale_file

load_dotenv()

home = Path.home()

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.5)
I18nAssistant = I18nAssistant(llm, 'vue', '$t', 'vue')

LOCALE_FILE_PATH = os.getenv('LOCALE_FILE_PATH')
BASE_TARGET_PATH = os.getenv('BASE_TARGET_PATH')
SKIP_PATHS = []
invalid_paths = []

def main(file_path):
    relative_path = os.path.join(home, file_path)

    for skippable_path in SKIP_PATHS:
        if skippable_path in relative_path: return

    try:
        if(os.path.isdir(relative_path)):
            for path in os.listdir(relative_path):
                main(os.path.join(file_path, path))
        else:
            print(f"Localizing {file_path}...")

            with open(relative_path) as file:
                file_name = os.path.basename(relative_path)
                locale_namespace = file_name.split('.')[0]
                code, yaml = I18nAssistant.generate_localized_code(file, locale_namespace)

            update_file_code(code, relative_path)
            update_locale_file(yaml, LOCALE_FILE_PATH)
            print(f"Sucessfully localized {file_path}!")

    except FileNotFoundError:
        print(f"File path: '{relative_path}' doesn't exist")
        invalid_paths.push(relative_path)

    except Exception as e:
        print(f"Error processing: '{relative_path}'.")
        print(f"Error was: {str(e)}")

        retry = input("Retry? (y/n): ")
        if retry == 'y': 
            main(relative_path)
    
if __name__ == '__main__':
    while True:
        file_path = input("Input file path please: ")

        if BASE_TARGET_PATH:
            file_path = os.path.join(BASE_TARGET_PATH, file_path)

        main(file_path)

        if len(invalid_paths) > 0:
            print(f"Failed translating {"\n".join(invalid_paths)}")

        