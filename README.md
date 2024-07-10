# Document Analysis

This project allows you to upload documents in PDF, DOCX, or TXT formats and analyzes them using OpenAI's GPT-4 model. The analysis includes identifying the main theme, objectives, evaluations, suggestions, criticisms, and improvements for the document.

## Features

- **Document Upload:** Upload documents in PDF, DOCX, or TXT formats.
- **Document Analysis:** Analyze the document to identify the main theme, objectives, evaluations, suggestions, criticisms, and improvements.
- **Output:** Generate a YAML file with the analysis results and display them in a web interface.
- **Document Type Identification:** Automatically identify the type of document (e.g., report, article, contract).

## Setup

### Prerequisites

- python = ">=3.10,<=3.13" or higher
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/document_analysis.git
    cd document_analysis
    ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    poetry lock 
    poetry install
    ```

3. **Create a `.env` file in the project root and add your OpenAI API key:**

    ```plaintext
    OPENAI_API_KEY=""
    OPENAI_MODEL_NAME="gpt-3.5-turbo"
    SERPER_API_KEY='8'
    ```

### Running the Application

1. **Start the Flask application:**

    ```bash
    poetry run python src/document_analysis/app.py
    ```

2. **Open your browser and navigate to `http://127.0.0.1:5000/`.**

3. **Upload a document (PDF, DOCX, or TXT) through the web interface.**

4. **View the analysis results on the results page and in the `output_results` folder.**

## Project Structure

