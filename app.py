import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime

from readme_agent import extract_code_from_files, generate_readme
from github_utils import (
    create_new_repo, clone_repo, push_files_to_repo
)

load_dotenv()

st.set_page_config(page_title="AI README Generator", layout="centered")

st.title("📘 AI-Powered README Generator")
st.markdown("Upload your code and let GPT generate a professional `README.md`. It will auto-push everything to GitHub.")

uploaded_files = st.file_uploader("Upload .py or .ipynb files", type=['py', 'ipynb'], accept_multiple_files=True)
repo_url = st.text_input("Enter your GitHub repository URL (or leave blank to create a new one)")

create_repo_flag = st.checkbox("Create new repo if not provided", value=True)

if st.button("Generate and Push README"):
    if not uploaded_files:
        st.warning("Please upload at least one code file.")
    else:
        with st.spinner("Processing..."):
            try:
                github_token = os.getenv("GITHUB_TOKEN")
                openai_key = os.getenv("OPENAI_API_KEY")

                # Step 1: Extract code and generate README
                code = extract_code_from_files(uploaded_files)
                readme_text = generate_readme(code, repo_url or "To be created", api_key=openai_key)
                st.success("✅ README generated.")

                # Step 2: Create or clone repo
                if not repo_url or create_repo_flag:
                    # Generate a name from timestamp
                    repo_name = f"auto-readme-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                    new_repo_url = create_new_repo(github_token, repo_name, private=False)
                    repo_url = new_repo_url
                    st.info(f"🆕 Created GitHub repo: {repo_name}")
                else:
                    st.info("Using provided repo...")

                repo_path = clone_repo(repo_url, github_token)

                # Step 3: Push README + uploaded files
                push_files_to_repo(repo_path, uploaded_files, readme_text)
                st.success("✅ Code & README pushed to GitHub.")
                st.markdown(f"[🔗 View Repository]({repo_url.replace(f'{github_token}@', '')})")

                # Download
                st.download_button("📥 Download README.md", data=readme_text, file_name="README.md")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
