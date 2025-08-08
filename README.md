# AI README Generator

## Description
The AI README Generator is a Streamlit web application that allows users to upload their Python (.py) or Jupyter Notebook (.ipynb) files and enter their GitHub repository link. The application then uses an AI-powered model to generate a professional `README.md` file based on the provided code and repository link. The generated README file is automatically pushed to the user's GitHub repository.

## Features
- Upload Python (.py) or Jupyter Notebook (.ipynb) files
- Enter GitHub repository link
- Generate professional README.md file using AI model
- Automatically push generated README to GitHub repository

## Installation
To run the AI README Generator, follow these steps:
1. Clone the repository from [GitHub](https://github.com/SaadAshraf12/Ai_Git_Readme_Agent)
2. Install the required packages by running `pip install -r requirements.txt`
3. Set up environment variables for `OPENAI_API_KEY` and `GITHUB_TOKEN`
4. Run the Streamlit app by executing `streamlit run app.py` in the terminal

## Usage
1. Upload your Python (.py) or Jupyter Notebook (.ipynb) files using the file uploader
2. Enter your GitHub Repository URL with write access
3. Click on the "Generate and Push README" button
4. Wait for the README generation and push process to complete
5. Download the generated README.md file

## Requirements
- Python 3.6+
- Streamlit
- OpenAI API Key
- GitHub Token

## Example
```python
# File: app.py
import streamlit as st
from dotenv import load_dotenv
import os

from readme_agent import extract_code_from_files, generate_readme
from github_utils import clone_repo, push_readme_to_repo

load_dotenv()

st.set_page_config(page_title="AI README Generator", layout="centered")

st.title("📘 AI-Powered README Generator")
st.markdown("Upload your code and enter your GitHub repo link. This app will generate a professional `README.md` and push it to your repo.")

# 1. Upload files
uploaded_files = st.file_uploader("Upload .py or .ipynb files", type=['py', 'ipynb'], accept_multiple_files=True)

# 2. GitHub repo
repo_url = st.text_input("Enter your GitHub Repository URL (must have write access)")

# 3. Button
if st.button("Generate and Push README"):
    if not uploaded_files or not repo_url:
        st.warning("Please upload files and enter your GitHub repo link.")
    else:
        with st.spinner("Processing..."):
            try:
                # Step 1: Extract Code
                code = extract_code_from_files(uploaded_files)
                st.success("✅ Code extracted successfully.")

                # Step 2: Generate README using GPT
                readme_text = generate_readme(
                    code,
                    repo_url,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                st.success("✅ README generated.")

                # Step 3: Clone and Push
                repo_path = clone_repo(repo_url, os.getenv("GITHUB_TOKEN"))
                push_readme_to_repo(repo_path, readme_text)
                st.success("✅ README pushed to GitHub.")

                st.download_button("📥 Download README.md", data=readme_text, file_name="README.md")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
```

For more details, visit the [GitHub Repo](https://github.com/SaadAshraf12/Ai_Git_Readme_Agent).