import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.base import BaseLLM
from htmlTemplates import css, bot_template, user_template
from groq import Groq
import asyncio
import os

# Load environment variables
load_dotenv()  # Ensure you load environment variables
groq_api_key = os.environ.get("GROQ_API_TOKEN")

# Wrapper class to make Groq compatible with LangChain
class GroqWrapper(BaseLLM):
    def __init__(self, api_key):
        super().__init__()  # Call the initializer of BaseLLM
        if api_key is None:
            raise ValueError("API key must be provided")
        self.client = Groq(api_key=api_key)  # Use the passed API key directly
        self.api_key = api_key  # Store the API key for debugging

    def _generate(self, prompts, stop=None):
        responses = []
        for prompt in prompts:
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {"role": "user", "content": [{"type": "text", "text": prompt}]},
                        {"role": "assistant", "content": ""},
                    ],
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=stop,
                )
                responses.append(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error during completion: {e}")
                responses.append("Error occurred while generating response.")
        return responses

    @property
    def _llm_type(self):
        return "groq"

    def __str__(self):
        return f"GroqWrapper(api_key={self.api_key})"

async def get_pdf_text(pdf_docs):
    try:
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error processing PDF files: {e}")
        return ""

async def get_text_chunks(text):
    try:
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        st.error(f"Error splitting text: {e}")
        return []

async def get_vectorstore(text_chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {e}")
        return None

async def get_conversation_chain(vectorstore):
    try:
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        
        # Wrap Groq in GroqWrapper using the API key
        llm = GroqWrapper(groq_api_key)  # Ensure the API key is passed correctly
        st.write(f"Initialized {llm}")  # For debugging purposes

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {e}")
        return None

async def handle_userinput(user_question):
    try:
        if st.session_state.conversation:  # Ensure conversation is initialized
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']

            for i, message in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error handling user input: {e}")

async def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question and st.session_state.conversation:
        await handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process") and pdf_docs:
            with st.spinner("Processing"):
                raw_text = await get_pdf_text(pdf_docs)
                text_chunks = await get_text_chunks(raw_text)
                if text_chunks:  # Ensure text chunks are not empty
                    vectorstore = await get_vectorstore(text_chunks)
                    if vectorstore:
                        st.session_state.conversation = await get_conversation_chain(vectorstore)
                    else:
                        st.error("Failed to create a vector store. Please check your PDFs.")
                else:
                    st.error("No text chunks found. Please check your PDFs.")

if __name__ == '__main__':
    asyncio.run(main())
