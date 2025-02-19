Note: place your .env file in the root folder, and run with "streamlit run hw1.py" 

the .env file look like this:
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
OPENAI_BASE_URL=https://api.ai.it.cornell.edu/
TZ=America/New_York

Modification: added installation of *poppler-utils* and *tesseract-ocr* using apt
In pyproject.toml added:
langchain-community = "^0.2.15"
langchain = "^0.2.15"
langchain_core = "^0.2.15"
langchain-openai = "^0.1.23"
pydub = "^0.25.1"
pdf2image = "^1.17.0"
pdfplumber = "^0.11.5"
pytesseract = "^0.3.13"
tesseract = "^0.1.3"
faiss-cpu = "^1.10.0"