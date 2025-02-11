import streamlit as st
from openai import OpenAI
from os import environ
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

st.title("📝 File Q&A with OpenAI")

# TODO: Chunk the file content into smaller parts if it is too large
# TODO: Implement actual retrieval mechanism
uploaded_files = st.file_uploader("Upload an article", type=("txt","pdf"), accept_multiple_files=True)

question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_files,
)

def extract_text_smart(pdf_file, file_name):
    text_output = ""
    
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                text_output += f"Document:{file_name}\n{page_text}\n\n"
            else:
                # Convert the PDF page to an image
                images = convert_from_path(pdf_file, first_page=i+1, last_page=i+1)
                for img in images:
                    ocr_text = pytesseract.image_to_string(img)
                    text_output += f"Document:{file_name}\n{ocr_text}\n\n"
    
    return text_output


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_files:
    file_content = ""
    
    for uploaded_file in uploaded_files:
        # Read the content of the uploaded file, for each type
        if uploaded_file.type in ["text/plain", "text/markdown"]:
            file_content += f"Document:{uploaded_file.name}\n{uploaded_file.read().decode('utf-8')}"
            file_content += "\n\n"
        elif uploaded_file.type == "application/pdf":
            file_content += extract_text_smart(uploaded_file, uploaded_file.name)
            file_content += "\n\n"
            
    print(file_content)
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{file_content}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)


    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})

