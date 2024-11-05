import json

def import_json(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        json_content = ''.join(line for line in lines if not line.strip().startswith('//'))
        return json.loads(json_content)
    
def export_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
