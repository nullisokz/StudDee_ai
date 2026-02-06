import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 2. De specifika kedjorna (dessa bor numera under under-moduler)
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# 3. Integrationer (dessa har egna paket)
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature= 0.3
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory= "./chroma_db",
    embedding_function = embeddings
)

system_prompt = """
                Du är en assistent som ska hitta fakta utifrån den kontext du får.
                Du ska ge en sammanfattning om de viktigaste delarna.
                Om svaret inte finns i texten så svara "Jag kan inte hitta någon information i innehållet
                \n\n
                {context}
                """
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

combine_docs_chain = create_stuff_documents_chain(llm, prompt)

rag_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)



chat_history = []

print("Gemini ready! type 'exit' to quit.")

while True:
    user_input = input("Fråga: ")

    if user_input.lower() == 'exit':
        print("Adjö!")
        break

    result = rag_chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    answer = result["answer"]

    print(f'\n Gemini: {answer}\n')
    print("-" * 40)

    #print("-" * 20, "ANVÄNDA CHUNKS","-" * 20)

    #for i, doc in enumerate(result["context"]):
    #    source_text = doc.page_content.replace('\n', ' ')[:200]
    #    print(f'[{i+1}] {source_text}...')
    #    print("-" * 40)

    chat_history.append(("human", user_input))
    chat_history.append(("ai", answer))

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]





