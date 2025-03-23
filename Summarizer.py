import os
import re
import time
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
import textwrap
import PyPDF2 
import warnings
warnings.filterwarnings("ignore")

class OllamaBookSummarizer:
    def __init__(self, model_name="mistral:7b", host=None):
        """Initialize the summarizer with a local Ollama model."""
        print(f"Initializing with model: {model_name}")
        
        if host is None:
            host = os.environ.get("OLLAMA_HOST", "localhost")
        
        if not host.startswith("http"):
            host = f"http://{host}:11434"
        
        # Initialize Ollama
        self.llm = Ollama(
            model=model_name,
            base_url=host,
            temperature=0.1,
            num_ctx=5000, 
            verbose=True
        )
        
        self.target_compression = 0.3
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=300,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        self.map_prompt_template = """
        You are a highly skilled book summarizer. Your goal is to create a concise summary that captures the 
        key information from the following book.
        without loosing the titles , headings and other info , do not loose any context or the overall flow of the book , Focus on preserving the most important facts, concepts, and details.
        Maintain the original meaning and context while reducing the length. Aim for a summary that is about 30% 
        of the original length.

        Text to summarize:
        {text}

        CONCISE SUMMARY:
        """
        
        self.combine_prompt_template = """
        You are a highly skilled book and text editor. Your task is to combine the following summaries into a single or many if needed for long books or texts, coherent 
        summary that flows naturally. Eliminate redundancies and ensure the final summary is well-structured and 
        easy to read. Focus on maintaining a logical flow of ideas. The final summary should be approximately 30% 
        of the original document's length.

        SUMMARIES TO COMBINE:
        {text}

        COMBINED SUMMARY:
        """
        
        self.map_prompt = PromptTemplate(template=self.map_prompt_template, input_variables=["text"])
        self.combine_prompt = PromptTemplate(template=self.combine_prompt_template, input_variables=["text"])
    
    def read_file(self, file_path):
        """Read content from a file based on its extension."""
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == '.pdf':
            return self._read_pdf(file_path)
        else:
            # Default to text file
            return self._read_text(file_path)
    
    def _read_text(self, file_path):
        """Read text content from a file."""
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()
    
    def _read_pdf(self, file_path):
        """Extract text from a PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() + "\n"
        return text
    
    def preprocess_text(self, text):
        """Clean and preprocess text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Replace line breaks with spaces
        text = re.sub(r'\n+', ' ', text)
        return text
    
    def split_into_chunks(self, text):
        """Split text into chunks for processing."""
        print("Splitting text into chunks...")
        processed_text = self.preprocess_text(text)
        docs = [Document(page_content=processed_text)]
        chunks = self.text_splitter.split_documents(docs)
        print(f"Text split into {len(chunks)} chunks")
        return chunks
    
    def summarize_book(self, book_text, compression_rate=None):
        """Summarize an entire book."""
        if compression_rate is None:
            compression_rate = self.target_compression
        
        # Split the text into chunks
        chunks = self.split_into_chunks(book_text)
        if len(chunks) == 1:
            print("Single chunk detected. Summarizing directly...")
            return self.summarize_single_chunk(chunks[0].page_content, compression_rate)
        
        # Create the summarization chain
        chain = load_summarize_chain(
            self.llm,
            chain_type="map_reduce",
            map_prompt=self.map_prompt,
            combine_prompt=self.combine_prompt,
            verbose=True
        )
        
        print("Starting summarization process...")
        start_time = time.time()
        
        # Run the chain
        result = chain.invoke(chunks)
        
        end_time = time.time()
        print(f"Summarization completed in {end_time - start_time:.2f} seconds")
        
        return result['output_text']
    
    def summarize_single_chunk(self, text, compression_rate):
        """Summarize a single chunk of text."""
        prompt = f"""
        Summarize the following text of the book to approximately {int(compression_rate * 100)}% of its original length.
        add info if needed or remove it if not, but it has to be {int(compression_rate * 100)}% of its original size 
        Do not try to narrate the document or the book but keep the format and flow of it as it is ,
        not matter what do not loose or override the format
        try to remove the unnecessary filler talks and filler parts , only summarize the main facts, narrations, infomartions, stories etc without loosing the details of it  
        Preserve the key information, main points, and essential details. Maintain the original meaning and context.
        keep in mind that each paragraph is connected to the next and the previous paragraph so keep the flow and do not add your own voice to it
        
        TEXT:
        {text}
        
        SUMMARY:
        """
        
        return self.llm.invoke(prompt)
    
    def format_summary(self, summary, width=80):
        """Format the summary text for better readability."""
        paragraphs = summary.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                wrapped = textwrap.fill(paragraph, width=width)
                formatted_paragraphs.append(wrapped)
                
        return '\n\n'.join(formatted_paragraphs)
    
    def save_summary(self, summary, output_path):
        """Save the summary to a file."""
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary saved to {output_path}")

#Testing
if __name__ == "__main__":
    # File paths
    input_file_path = "doc.pdf"  
    output_file_path = "summary.txt" 
    compression_rate = 0.6  
    model_name = "mistral:7b"
    
    summarizer = OllamaBookSummarizer(model_name=model_name)
    
    print(f"Reading book from {input_file_path}...")
    book_text = summarizer.read_file(input_file_path)
    print(f"Book length: {len(book_text.split())} words")
    
    print(f"Summarizing with target compression rate of {compression_rate * 100}%...")
    summary = summarizer.summarize_book(book_text, compression_rate)
    
    formatted_summary = summarizer.format_summary(summary)
    summarizer.save_summary(formatted_summary, output_file_path)
    
    print(f"Summary length: {len(formatted_summary.split())} words")
    print(f"Actual compression rate: {len(formatted_summary.split()) / len(book_text.split()):.2%}")
    print(f"Summary saved to: {output_file_path}")