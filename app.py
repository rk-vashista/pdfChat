import streamlit as st




def main():
    st.set_page_config(page_title="PDFChat", page_icon=":books:")
    st.header("Chat from PDF :books:")
    
    with st.sidebar:
        st.subheader("Your PDF")
        st.file_uploader("Upload your PDF", type=['pdf'])    
        st.button("Process")

if __name__ == '__main__':
    main()