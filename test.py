from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize the splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=10,      # Target number of characters per chunk
    chunk_overlap=1,    # Number of characters to repeat from the previous chunk
    length_function=len,
    separators=[ " ", "", "\n\n", "\n"] # Hierarchical separators
)

# Split your text
text = "Your long document text here..."
chunks = text_splitter.split_text(text)

print(chunks)