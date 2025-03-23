import streamlit as st
import os
from Summarizer import OllamaBookSummarizer

# Set page title and description
st.title('AI-Powered Book & Document Summarizer – Smart, Fast, and Accurate!')
st.write("Tired of reading lengthy books and documents? Our AI-driven summarizer condenses complex texts into concise, insightful summaries while preserving key details. Whether it's research papers, business reports, or entire books, get the essence in seconds with our cutting-edge AI. Save time, stay informed, and never miss important insights!")

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# File upload widget
file = st.file_uploader("Upload Your Documents!", type=["txt", "pdf", "docx"])

# Initialize variables
summary = None
compression_rate = st.slider("Compression Rate", min_value=0.1, max_value=0.9, value=0.6, step=0.1,
                            help="Lower values produce shorter summaries")

model_options = ["mistral:7b", "llama2:7b", "llama3:8b", "phi3:14b"]
model_name = st.selectbox("Select Model", model_options)

# Process file when uploaded
if file is not None:
    save_path = os.path.join("uploads", file.name)
    
    # Save uploaded file
    with open(save_path, "wb") as f:
        f.write(file.getbuffer())
    st.success(f"File saved successfully: {save_path}")
    
    # Set output path
    output_file_path = os.path.join("outputs", f"summary_{file.name}")
    
    # Create summarizer instance
    summarizer = OllamaBookSummarizer(model_name=model_name)
    
    # Process with feedback
    with st.spinner("Reading document..."):
        book_text = summarizer.read_file(save_path)
        st.info(f"Document length: {len(book_text.split())} words")
    
    if st.button("Generate Summary"):
        with st.spinner(f"Summarizing with target compression rate of {compression_rate * 100}%..."):
            try:
                summary = summarizer.summarize_book(book_text, compression_rate)
                formatted_summary = summarizer.format_summary(summary)
                summarizer.save_summary(formatted_summary, output_file_path)
                
                st.success(f"Summary created! Length: {len(formatted_summary.split())} words")
                st.info(f"Actual compression rate: {len(formatted_summary.split()) / len(book_text.split()):.2%}")
                
                # Display summary
                st.subheader("Summary")
                # st.markdown(formatted_summary)
                
                # Download button
                with open(output_file_path, "r") as f:
                    st.download_button(
                        label="Download Summary",
                        data=f.read(),
                        file_name=f"summary_{file.name}",
                        mime="text/plain"
                    )

                # cleaning up the files 
                os.remove(output_file_path)
                os.remove(save_path)
            except Exception as e:
                st.error(f"An error occurred during summarization: {str(e)}")
else:
    st.info("Please upload a document to summarize")