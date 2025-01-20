import yaml

def loadYaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return data
    except Exception as e:
        print(f"Error reading yaml {file_path}: {e}")