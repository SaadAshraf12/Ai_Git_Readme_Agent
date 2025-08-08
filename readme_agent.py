from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import nbformat

def extract_code_from_files(uploaded_files):
    all_code = ""
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        if filename.endswith(".ipynb"):
            nb = nbformat.read(uploaded_file, as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    all_code += cell.source + "\n"
        elif filename.endswith(".py"):
            code = uploaded_file.read().decode("utf-8")
            all_code += f"# File: {filename}\n{code}\n\n"
    return all_code

def generate_readme(code, repo_link, api_key):
    llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0.5)

    prompt = ChatPromptTemplate.from_template("""
    You are an experienced AI engineer. Based on the following code and repository link, write a professional README.md file with:
    - Project name
    - Description
    - Features
    - Installation
    - Usage
    - Requirements
    - Example if possible

    GitHub Repo: {repo_link}
    Code:
    {code}
    """)

    messages = prompt.format_messages(code=code, repo_link=repo_link)
    readme = llm(messages)
    return readme.content
