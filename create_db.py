from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectordb_file_path = "faiss_index"

# Creates a vector database from a CSV file and saves it locally
def create_vector_db():
    loader = CSVLoader(file_path='customersupport_faqs.csv', source_column="prompt")
    data = loader.load()

    vectordb = FAISS.from_documents(documents=data,
                                    embedding=embed)

    vectordb.save_local(vectordb_file_path)

if __name__ == "__main__":
    create_vector_db()


