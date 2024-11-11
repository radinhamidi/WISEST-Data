import json

def txt_to_json(input_file_path, output_file_path):
    passages = []
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            passage = {}
            passage['id'] = i
            passage['contents'] = lines[i]
            passages.append(passage)

    with open(output_file_path, 'w') as file:
        json.dump(passages, file, indent=4, ensure_ascii=False)