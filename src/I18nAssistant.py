import re

from langchain_core.prompts import ChatPromptTemplate

from src.prompts.context import SYSTEM_PROMPT

from src.exceptions.ParsingError import ParsingError

class I18nAssistant:
    def __init__(self, llm, language, i18n_function, i18n_package):
        self.llm = llm
        self.language = language
        self.i18n_package = i18n_package
        self.i18n_function = i18n_function

    def generate_localized_code(self, file, locale_namespace):
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("user", "{code}")]
        )

        prompt = prompt_template.invoke({
            'code': file.read(),
            'language': self.language,
            'i18n_package': self.i18n_package,
            'i18n_function': self.i18n_function,
            'locale_namespace': locale_namespace
        })

        response = self.llm.invoke(prompt)

        localized_code = self.get_code(response.content)
        new_yaml_locale = self.get_yaml(response.content)

        return [localized_code, new_yaml_locale]
    
    def get_code(self, response):
        try:
            regex = re.compile(f"(?<=^```{self.language}\n).*(?=```\n)", flags=re.S|re.M)

            return regex.search(response)[0]
        except Exception:
            raise ParsingError(f'Error parsing code from: {response}')

    def get_yaml(self, response):
        try:
            regex = re.compile("(?<=```yaml\n).*(?=```$)", flags=re.S|re.M)

            return regex.search(response)[0]
        except Exception:
            raise ParsingError(f'Error parsing yaml from {response}')
