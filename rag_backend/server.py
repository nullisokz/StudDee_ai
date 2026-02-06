import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
app = Flask(__name__)
CORS(app)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Du är en hjälpsam assistent."
    "VIKTIGT: Skriv ALDRIG matematiska symboler med dollartecken eller LaTeX. "
    "Använd istället vanliga bokstäver, t.ex. skriv 'y' istället för '$y$'."
    "Svara baserat på: {context}"),
    ("human", "{input}"),
])

combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(vectorstore.as_retriever(search_kwargs={"k": 5}), combine_docs_chain)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get("message")
    if not user_query:
        return jsonify({"error": "Inget meddelande hittat"}), 400
    
    result = rag_chain.invoke({"input": user_query})

    return jsonify({
        "answer": result["answer"],
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)