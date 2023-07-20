import streamlit as st
import json

def download_json(json_data, filename):
    # Convert the JSON data to a string
    json_str = json.dumps(json_data, indent=4)

    # Create a button to download the JSON file
    with open(filename, 'w') as f:
        f.write(json_str)

    st.download_button(
        label="Click to Download JSON",
        data=json_str,
        file_name=filename,
        mime='application/json'
    )

def main():
    st.title("Download JSON File")

    # Sample JSON data (you can replace this with your own data)
    json_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com"
    }

    download_json(json_data, 'data.json')

if __name__ == "__main__":
    main()
