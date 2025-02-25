import streamlit as st
from os import environ
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

DEBUG = False
# Streamlit UI Setup
st.title("📝 File Q&A with OpenAI (RAG-powered)")

# File Uploader
uploaded_files = st.file_uploader(
    "Upload one or more articles (.txt, .pdf)", 
    type=("txt", "pdf"), 
    accept_multiple_files=True
)



question = st.chat_input("Ask something about the uploaded files", disabled=not uploaded_files)

def debug_print(msg):
    if DEBUG == True:
        print(msg)
        
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
            page_content=f"{file_text}",
            metadata={"source": uploaded_file.name}
        )
        documents.append(document)
    
    return documents

# Initialize OpenAI API Key
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")

# Session state setup
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = StreamlitChatMessageHistory(key="chat_messages")

# Process uploaded files and create vector store
if uploaded_files:
    documents = process_files(uploaded_files)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunked_docs = text_splitter.split_documents(documents)
    print("chunked_docs: ", len(chunked_docs))
    
    # Create FAISS Vector Store
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="openai.text-embedding-3-large")
    vector_store = FAISS.from_documents(chunked_docs, embeddings)

    st.session_state.vector_store = vector_store

    st.success(f"✅ Processed {len(uploaded_files)} file(s). You can now ask questions!")

# Display previous chat history
for msg in st.session_state.chat_messages.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Handling User Question
if question and st.session_state.vector_store:
    # retriever = st.session_state.vector_store.as_retriever()
    retriever = st.session_state.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    template = """
    You are an AI assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. Please also remember the information that the user told you.
    
    Context: {context} 
    
    Previous Conversation: {history}
    
    Question: {question} 
    
    Answer:
    """
    
    prompt = PromptTemplate.from_template(template)
    
    final_prompt = {"context": RunnablePassthrough(), "question": RunnablePassthrough(), "history": RunnablePassthrough()} | prompt
    # Retrieve relevant documents
    retrieved_docs = list(retriever.invoke(question))
    print("retrieved_docs: ", retrieved_docs)
    # formatted_docs = format_docs_with_sources(retrieved_docs)

    client = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="openai.gpt-4o", temperature=0.2)
    
    def format_docs(docs):
        # Append the source to make it source-aware
        return "\n\n".join(f"source:{doc.metadata.get('source')}\n{doc.page_content}" for doc in docs)
    # debug_print(f"prompt: {final_prompt}")
    debug_print(f"formatted_docs: {format_docs(retrieved_docs)}")
    
    
    #Build the RAG chain
    rag_chain = (
        final_prompt
        | client
        | StrOutputParser()
    )

    # Display & Save User Message
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.chat_messages.add_user_message(question)
    
    debug_print(f"history: {st.session_state.chat_messages}")
    # AI Response
    with st.chat_message("assistant"):
        response = rag_chain.invoke({
            "question": question,
            "context": format_docs(retrieved_docs),
            "history": str(st.session_state.chat_messages)
        })
        st.markdown(response)

    # Save AI Response
    st.session_state.chat_messages.add_ai_message(response)
