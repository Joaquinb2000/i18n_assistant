import yaml

def update_file_code(code, file_path):
    with open(file_path, 'w') as file:
        file.write(code)

def update_locale_file(yaml_str, file_path):
    with open(file_path, 'r') as file:
        locale = yaml.safe_load(file)

    new_locale = yaml.safe_load(yaml_str)

    locale.update(new_locale)

    with open(file_path, 'w') as file:
        yaml.dump(locale, file)

