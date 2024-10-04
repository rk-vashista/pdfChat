import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.base import LLM
from htmlTemplates import css, bot_template, user_template
from groq import Groq
import asyncio
import os
from typing import Any, List, Mapping, Optional
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_TOKEN")

class GroqWrapper(LLM, BaseModel):
    client: Groq = Field(default_factory=lambda: Groq(api_key=groq_api_key))
    model_name: str = Field(default="llama-3.2-11b-vision-preview")
    system_prompt: str = Field(default="You are a helpful AI assistant that answers questions based on the content of uploaded PDF documents. Provide concise and accurate responses.")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=stop,
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.error(f"Error during completion: {e}")
            return "Error occurred while generating response."

    @property
    def _llm_type(self) -> str:
        return "groq"

    def get_num_tokens(self, text: str) -> int:
        # This is a simple approximation, you might want to implement a more accurate method
        return len(text.split())

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.model_name, "system_prompt": self.system_prompt}

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

async def get_conversation_chain(vectorstore, system_prompt):
    try:
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        
        if not groq_api_key:
            raise ValueError("GROQ_API_TOKEN is not set in the environment variables")

        llm = GroqWrapper(system_prompt=system_prompt)
        st.write(f"Initialized GroqWrapper with model: {llm.model_name}")

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
        if st.session_state.conversation:
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
    
    # Add system prompt input in the sidebar
    with st.sidebar:
        st.subheader("System Prompt")
        system_prompt = st.text_area(
            "Enter a system prompt to set the context for the AI:",
            "You are a helpful AI assistant that answers questions based on the content of uploaded PDF documents. Provide concise and accurate responses.",
            height=100
        )
        
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process") and pdf_docs:
            with st.spinner("Processing"):
                raw_text = await get_pdf_text(pdf_docs)
                text_chunks = await get_text_chunks(raw_text)
                if text_chunks:
                    vectorstore = await get_vectorstore(text_chunks)
                    if vectorstore:
                        st.session_state.conversation = await get_conversation_chain(vectorstore, system_prompt)
                    else:
                        st.error("Failed to create a vector store. Please check your PDFs.")
                else:
                    st.error("No text chunks found. Please check your PDFs.")

    user_question = st.text_input("Ask a question about your documents:")
    if user_question and st.session_state.conversation:
        await handle_userinput(user_question)

if __name__ == '__main__':
    asyncio.run(main())