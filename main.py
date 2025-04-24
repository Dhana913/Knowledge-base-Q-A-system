import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAI


st.title("✨The Radiant Rhino Q&A✨")
question = st.text_input("Question: ")


load_dotenv()

llm = OpenAI(temperature=0.1)

embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectordb_file_path = "faiss_index"


vectordb = FAISS.load_local(vectordb_file_path, embed,
                                allow_dangerous_deserialization=True)
retriever = vectordb.as_retriever(score_threshold=0.7)

prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

prompt = PromptTemplate(
template=prompt_template, input_variables=["context", "question"]
    )
chain_type_kwargs = {"prompt": prompt}

# Creates a RetrievalQA chain for question answering using a LLM and the vector database which has the data from the .csv file
chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs=chain_type_kwargs)

if question:
   response = chain.invoke(question)
   st.header("Answer")
   if "result" in response:
       st.write(response["result"])
   else:
       st.write("Could not find answer.")

