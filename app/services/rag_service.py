import fitz
from openai import OpenAI
from sqlalchemy.orm import Session
from app.models.protocol import Protocol
from app.core.config import settings
from typing import List
from sqlalchemy import text
from app.db.database import SessionLocal
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You answer questions about a clinical trial protocol for clinical research coordinators.
Use only the protocol excerpts provided. Each excerpt starts with its page number.
Cite the page number for every fact, like (p. 34).
If the excerpts do not contain the answer, say "Not found in the retrieved protocol sections" instead of guessing.
Quote numbers, thresholds and time windows exactly as written.
Respond in JSON with exactly these keys:
- "answer": your answer, citing pages like (p. 34)
- "cited_pages": a list of the page numbers you actually used, e.g. [11, 35]
- "found": true if the excerpts contain the answer, otherwise false
"""


def extract_chunks(pdf_path: str, chunk_size: int =500) -> List[dict]:
    # open the PDF from the file path
    # create an empty string to collect text
    # loop over each page in the document
    # get the page's text and add it to your string
    # close the document
    # for now, print the length of the text and return an empty list
    doc=fitz.open(pdf_path)
    # full_text=""
    chunks=[]
    for page in doc:
        words=page.get_text().split()
        for i in range(0, len(words), chunk_size):
            chunk_words=words[i:i+chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append({"page_number":page.number+1,"content":chunk})
        # full_text+=page.get_text()
    
    doc.close()
    # print(len(chunks))
    # print(chunks[0]["page_number"], chunks[0]["content"][:200])
    # print(chunks[-1]["page_number"])
    return chunks
    

def embed_text(text:str) -> List[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def embed_protocol(protocol_id: int, pdf_path: str, db: Session) -> int:
    chunks = extract_chunks(pdf_path=pdf_path)

    db.execute(text("DELETE FROM protocol_chunks WHERE protocol_id = :pid"),
               {"pid": protocol_id})
    
    for index, chunk in enumerate(chunks):
        embedding = embed_text(chunk["content"])

        db.execute(
            text("""
                INSERT INTO protocol_chunks
                (protocol_id, chunk_index, page_number, content, embedding)
                VALUES (:pid, :idx, :page, :content, :embedding)
                """),
                {
                    "pid": protocol_id,
                    "idx": index,
                    "page": chunk["page_number"],
                    "content": chunk["content"],
                    "embedding": str(embedding),
                },

        )
    db.commit()
    return len(chunks)


def retrieve_chunks(protocol_id: int, query: str, db: Session, limit: int = 10) -> List[dict]:
    query_embedding = embed_text(query)

    rows = db.execute(
        text("""
             SELECT chunk_index, page_number, content, embedding <=> CAST(:embedding AS vector) AS distance
             FROM protocol_chunks
             WHERE protocol_id = :pid
             ORDER BY distance
             LIMIT :limit
             """),
             {"embedding": str(query_embedding),
              "pid": protocol_id,
              "limit": limit}
    ).fetchall()

    results = []
    for row in rows:
        results.append({
            "chunk_index": row.chunk_index,
            "page_number": row.page_number,
            "content": row.content,
            "distance": row.distance
        })
    return results

def answer_question(protocol_id: int, question: str, db: Session, limit: int = 10) -> dict:
    chunks = retrieve_chunks(protocol_id, question, db, limit)
    context=""
    for chunk in chunks:
        context+=f"[Page {chunk['page_number']}]\n{chunk['content']}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        response_format={"type":"json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Protocol excerpts:\n\n{context}Question: {question}"}
        ]
    )

    retrieved_pages = []
    for chunk in chunks:
        if chunk["page_number"] not in retrieved_pages:
            retrieved_pages.append(chunk["page_number"])

    data=json.loads(response.choices[0].message.content)

    cited_pages = []
    for page in data["cited_pages"]:
        if page in retrieved_pages:
            cited_pages.append(page)

    return {
        "answer": data["answer"],
        "found": data["found"],
        "cited_pages": cited_pages,
        "retrieved_pages": retrieved_pages
    }

if __name__ == "__main__":
    db = SessionLocal()
    try:
        result = answer_question(1, "What haemoglobin level would exclude a patient?", db)
        print(result["answer"])
        print("found:", result["found"])
        print("cited:", result["cited_pages"])
        print("retrieved:", result["retrieved_pages"])
    finally:
        db.close()


    # extract_chunks("/Users/edwinmjose/Documents/crc_clinical_aid_protocol_docs/Prot_000 (2).pdf")

























# def extract_chunks(pdf_path: str, chunk_size: int = 500) -> list[str]:
#     doc = fitz.open(pdf_path)
#     full_text = ""
#     for page in doc:
#         full_text += page.get_text()
    
#     words = full_text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)
#     return chunks

# def embed_text(text: str) -> list[float]:
#     response = openai.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding

# def embed_protocol(protocol_id: int, pdf_path: str, db: Session):
#     chunks = extract_chunks(pdf_path)
    
#     db.execute("DELETE FROM protocol_chunks WHERE protocol_id = :pid", {"pid": protocol_id})
    
#     for i, chunk in enumerate(chunks):
#         embedding = embed_text(chunk)
#         db.execute(
#             """INSERT INTO protocol_chunks (protocol_id, chunk_index, content, embedding)
#                VALUES (:pid, :idx, :content, :embedding)""",
#             {"pid": protocol_id, "idx": i, "content": chunk, "embedding": str(embedding)}
#         )
#     db.commit()
#     return len(chunks)

# def answer_question(protocol_id: int, question: str, db: Session) -> str:
#     question_embedding = embed_text(question)
    
#     results = db.execute(
#         """SELECT content FROM protocol_chunks
#            WHERE protocol_id = :pid
#            ORDER BY embedding <-> :embedding
#            LIMIT 5""",
#         {"pid": protocol_id, "embedding": str(question_embedding)}
#     ).fetchall()
    
#     context = "\n\n".join([r[0] for r in results])
    
#     response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a clinical trial expert. Answer questions based only on the provided protocol document excerpts."},
#             {"role": "user", "content": f"Protocol excerpts:\n{context}\n\nQuestion: {question}"}
#         ]
#     )
#     return response.choices[0].message.content