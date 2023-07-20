import json
import io

def download_json(col, json_data, filename):
    # Convert the JSON data to a string
    json_str = json.dumps(json_data, indent=4)

    # Create a button to download the JSON file
    # with open(filename, 'w') as f:
    #     f.write(json_str)
    # buffered = io.BytesIO()
    # buffered.write(json_data.encode('utf-8'))
    
    col.download_button(
        label="Click to Download JSON",
        data=json_str,
        file_name=filename,
        mime='application/json'
    )