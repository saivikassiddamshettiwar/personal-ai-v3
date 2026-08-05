import chromadb

import ollama

import uuid


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="personal_documents"
)


def create_embedding(text):

    response = ollama.embeddings(

        model="nomic-embed-text",

        prompt=text

    )

    return response["embedding"]


def split_text(

    text,

    chunk_size=1000,

    overlap=200

):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():

            chunks.append(
                chunk
            )

        start += (
            chunk_size
            - overlap
        )

    return chunks


def add_document(

    text,

    file_name

):

    if not text or not text.strip():

        return

    chunks = split_text(
        text
    )

    for chunk in chunks:

        embedding = create_embedding(
            chunk
        )

        collection.add(

            ids=[
                str(
                    uuid.uuid4()
                )
            ],

            embeddings=[
                embedding
            ],

            documents=[
                chunk
            ],

            metadatas=[
                {
                    "file_name": file_name
                }
            ]

        )


def search_documents(

    query,

    number_of_results=5

):

    if collection.count() == 0:

        return []

    query_embedding = create_embedding(
        query
    )

    total_documents = collection.count()

    number_of_results = min(

        number_of_results,

        total_documents

    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=number_of_results

    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents