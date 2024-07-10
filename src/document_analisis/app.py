from flask import Flask, request, render_template
import os
import yaml
import asyncio
from document_analisis.main import analyze_document

app = Flask(__name__)

# Ensure input and output directories exist
input_folder = 'input_docs'
output_folder = 'output_results'
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'document' not in request.files:
        return 'No file part'
    file = request.files['document']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(input_folder, file.filename)
        file.save(file_path)
        
        # Use asyncio.run to call the analyze_document function and wait for its result
        result = asyncio.run(analyze_document(file_path))
        
        output_file = os.path.join(output_folder, file.filename + '.yaml')
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(result, f, allow_unicode=True, default_flow_style=False)
        
        # Pass the result and the theme to the template
        theme = result.get("THEME", "No theme identified")
        return render_template('result.html', result=yaml.dump(result, allow_unicode=True, default_flow_style=False), theme=theme)

if __name__ == '__main__':
    app.run(debug=True)
