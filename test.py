import streamlit as st
from os import environ
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# Initialize OpenAI API Key
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")

# Streamlit UI Setup
st.title("📝 File Q&A with OpenAI (RAG-powered)")


msgs = StreamlitChatMessageHistory(key="chat_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")
    
uploaded_files = st.file_uploader(
    "Upload one or more articles (.txt, .pdf)", 
    type=("txt", "pdf"), 
    accept_multiple_files=True
)
    
model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="openai.gpt-4o")

# Function to Extract Text from PDF (OCR Fallback)
def extract_text_smart(pdf_file):
    text_output = ""
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                text_output += f"{page_text}\n\n"
            else:
                images = convert_from_bytes(pdf_file.getvalue(), first_page=i+1, last_page=i+1)
                for img in images:
                    ocr_text = pytesseract.image_to_string(img)
                    text_output += f"{ocr_text}\n\n"
    
    return text_output

# Function to Process Uploaded Files
def process_files(files):
    documents = []
    
    for uploaded_file in files:
        file_text = ""
        
        if uploaded_file.type in ["text/plain", "text/markdown"]:
            file_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            file_text = extract_text_smart(uploaded_file)

        document = Document(
            page_content=f"Document Name:{uploaded_file.name}\n{file_text}",
            metadata={"source": uploaded_file.name}
        )
        documents.append(document)
    
    return documents

def format_docs_with_sources(docs):
    """Format retrieved docs to include their source metadata."""
    return "\n\n".join(
        f"**Source: {doc.metadata['source']}**\n{doc.page_content}" for doc in docs
    )

# Session state setup
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Store messages as `HumanMessage` and `AIMessage`

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

if uploaded_files:
    documents = process_files(uploaded_files)

    # print(len(uploaded_files))
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=250)
    chunked_docs = text_splitter.split_documents(documents)

    # Create FAISS Vector Store
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="openai.text-embedding-3-large")
    vector_store = FAISS.from_documents(chunked_docs, embeddings)

    st.session_state.vector_store = vector_store

    st.success(f"✅ Processed {len(uploaded_files)} file(s). You can now ask questions!")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | model

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
)

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input("Ask something about the uploaded files"):
    st.chat_message("human").write(prompt)
    # As usual, new messages are added to StreamlitChatMessageHistory when the Chain is called.
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.invoke({"question": prompt}, config)
    st.chat_message("ai").write(response.content)
    
