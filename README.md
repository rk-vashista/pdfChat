# 🌟 Chat with Multiple PDFs 🌟

Welcome to the **Chat with Multiple PDFs** project! This is a Streamlit-based application where you can upload multiple PDF documents and ask questions about their content, powered by **Groq AI** and **LangChain**. The application processes PDFs, splits the text into chunks, and stores them in a vector store for efficient retrieval, enabling conversational interactions with the document contents.

---

## 📖 Features

- Upload multiple PDF files and interact with them through a chat interface.
- Ask questions and get responses powered by **Groq AI** and **LangChain**.
- Conversational memory to keep track of the chat history.
- Uses **HuggingFace embeddings** and **FAISS vectorstore** for efficient text retrieval.
  
---

## 🛠️ Installation

Follow these steps to get the application up and running.

### Prerequisites
Make sure you have **Python 3.8+** and **pip** installed.

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/chat-with-multiple-pdfs.git
    cd chat-with-multiple-pdfs
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the environment variables:

    - Create a `.env` file in the root directory and add your **Groq API Key**:
    
    ```bash
    GROQ_API_TOKEN=your-groq-api-key-here
    ```

---

## 🚀 Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Once the application starts, open it in your browser. You will see an input field to upload your PDFs.

3. Upload the PDFs and ask questions about their content via the text input.

4. Responses from the AI will be displayed in a conversational format on the interface.

---

## 🔧 Tech Stack

- **Streamlit**: Interactive UI for the app.
- **LangChain**: Manages language models, text splitting, and conversation memory.
- **Groq AI**: Powers the LLM-based responses.
- **HuggingFace Embeddings**: For converting text chunks into vector representations.
- **FAISS**: Vector store for fast text retrieval.
- **PyPDF2**: Extracts text from PDF documents.

---

## 🎨 Customization

- **UI Templates**: You can find the custom HTML templates in `htmlTemplates.py`. Feel free to modify the `user_template` and `bot_template` to match your desired aesthetics.
- **Model**: The LLM used in this project is **Groq’s Llama 3.2 11B Vision Preview**. You can change this model by modifying the `GroqWrapper` class in `app.py`.

---

## 🧪 Example

1. Upload two or more PDF documents.
2. Ask a question like: _"What is the main point discussed in the first document?"_
3. The system will extract the relevant information from the documents and return a meaningful response.

---

## 💡 Future Enhancements

- Adding support for more file formats (like Word, Text, etc.).
- Implementing caching for faster repeated queries.
- Enhancing UI with themes and styles.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

## 🌟 Credits

- Developed using **Streamlit**, **LangChain**, and **Groq AI**.
- Special thanks to **HuggingFace** for the powerful embeddings models and **FAISS** for text retrieval.

---

Give it a ⭐ if you found this project helpful!
