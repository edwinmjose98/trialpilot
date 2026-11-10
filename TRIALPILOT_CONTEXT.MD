# TrialPilot Project Context

## Project
- TrialPilot — web app to help clinical trial coordinators avoid protocol deviations
- Edwin: technical co-founder (builder). Medical co-founder: oncology CRC at OSF/UICOMP (Illinois)
- Stack: FastAPI + PostgreSQL backend, Next.js + React frontend
- Backend path: /Users/edwinmjose/Documents/crc_clinical_aid_protocol_docs/trialpilot
- Frontend path: /Users/edwinmjose/Documents/crc_clinical_aid_protocol_docs/trialpilot-frontend (separate Next.js repo, pushed to GitHub)
- Test protocol PDF: /Users/edwinmjose/Documents/crc_clinical_aid_protocol_docs/Prot_000 (2).pdf
  (this IS the TJ301 protocol, CTJ301UC201 Ver 1.1 — 97 pages, ulcerative colitis trial, not oncology, marked CONFIDENTIAL; stored as protocol id 1)
- Spec docs in the parent folder: TrialPilot_Knowledge_Document.docx (product spec), "answers to claude questions from CRC (1).xlsx" (co-founder's answers — use Sheet2)

## Completed
- 8 PostgreSQL tables: users, protocols, patients, visit_definitions, procedure_definitions, visit_schedules, checklist_items, alerts
- API endpoints: Protocol CRUD, Patient CRUD, VisitDefinition POST, Alerts GET/PUT
- Services: auto visit schedule generation, alert detection (VISIT_OVERDUE, WINDOW_CLOSING)
- Frontend pages working: login, dashboard, patients, protocols, alerts
- JWT auth flow end-to-end, fetchWithAuth utility at src/app/utils/api.js
- GPT-4o PDF parser working — extracts 11 visits, 111 procedures from TJ301 protocol PDF
- pgvector installed and enabled in PostgreSQL 16 (built from source)
- protocol_chunks table: id, protocol_id, chunk_index, content, embedding vector(1536), page_number
  (page_number added 2026-11-10; table ownership moved from edwinmjose to trialpilot_user so the app can access it)
- pip installed: pgvector, openai in backend venv (pgvector is not in requirements.txt yet)
- app/services/rag_service.py — 5 of 6 functions written and tested (2026-11-10):
  - extract_chunks: per-page chunking, returns [{"page_number", "content"}] → 101 chunks for TJ301
  - embed_text: text-embedding-3-small → 1536 floats
  - embed_protocol: deletes old chunks for the protocol, inserts new rows, single commit at end. TJ301 embedded: 101 rows, pages 1–97
  - retrieve_chunks: cosine distance (<=>) search, returns chunk_index, page_number, content, distance
  - answer_question: top 10 chunks labelled [Page N] → GPT-4o (temperature 0, JSON mode) → {answer, found, cited_pages, retrieved_pages}
    cited_pages is filtered to pages actually retrieved. Tested: "What haemoglobin level would exclude a patient?" → "<9 g/dL (p. 35)", correct

## Architecture Decision
RAG pipeline replaces old parse-pdf approach.
Flow: /embed (chunk+store in pgvector) → /parse (retrieve relevant chunks + GPT-4o → save visits/procedures to DB) → /ask (free-form Q&A)
RAG endpoints go in separate app/api/v1/endpoints/rag.py

Decisions made while building rag_service.py:
- Chunk per page (not whole text) so every chunk carries a page number for citations
- chunk_size 500 words for now; tune only after testing with real questions
- chunk_index kept alongside page_number: pages can have several chunks, and it allows fetching neighbouring chunks
- Page citations come from GPT-4o's JSON (cited_pages), not from the retrieved list
- No model training/fine-tuning: knowledge stays in protocol_chunks so answers are citable and per-protocol.
  A local open-source model (embeddings + LLM) is the fallback if the protocol cannot be sent to OpenAI
- Raw SQL must be wrapped in sqlalchemy text() (SQLAlchemy 2.x)

- RAG endpoints working (2026-11-10), in app/api/v1/rag.py (routers live directly in app/api/v1/, no endpoints/ folder):
  - POST /api/v1/protocols/{protocol_id}/embed — PDF upload → embed_protocol → {"message", "chunks_created"}. Re-embedding TJ301 gave 101 rows, no duplicates
  - POST /api/v1/protocols/{protocol_id}/ask — body {"question"} (AskRequest in app/schemas/rag.py) → answer_question
  - extract_chunks/embed_protocol now take pdf_bytes (uploaded file contents), not a file path
- Auth switched from OAuth2PasswordBearer to HTTPBearer in app/core/security.py so Swagger's Authorize accepts a pasted token
  (login stays JSON {email, password}; frontend unaffected; bad token still returns 401)
- Swagger testing: /docs → POST /auth/login → copy access_token → Authorize → paste. Local test account: test@trialpilot.com / test123 (dev only)

## WHERE WE LEFT OFF — NEXT TASK
- rag_service.py: functions 1–4 and 6 done, plus /embed and /ask endpoints
- Next: parse_protocol(protocol_id, db) — retrieve relevant chunks, GPT-4o extracts structured visits/procedures, save to DB (overlaps with existing protocol_parser.py), then /parse endpoint
- Old commented-out drafts at the bottom of rag_service.py can be deleted
- Embedding runs synchronously (~1–2 min, 101 OpenAI calls); consider batching inputs or a background job later

Improvements to try after testing (one at a time, measure each):
- Strip the repeated ~176-char page header ("Date: 16 May 2017 Ver.1.1 ... CONFIDENTIAL") from every chunk
- Overlap between chunks; prepend section headings; fetch neighbouring chunks by chunk_index
- Skip/merge tiny chunks (10 chunks under 100 words); table-aware extraction for the Schedule of Events
- De-duplicate retrieved_pages (a page with 2 chunks appears twice)
- Build ~10 test questions with known answers + pages from THIS protocol (UC trial)

Open questions:
- Confirm the sponsor's confidentiality terms allow sending the protocol to OpenAI (already sent by both the parser and embed_protocol)
- Medical co-founder follow-ups: SAE answer (Q34) missing, retention 12 vs ~20 years, "adrenaline" = adrenal?, hepatitis A exclusion typo?
- Spec gaps in schema: arms/cohorts, eligibility criteria, deviations, audit log not built yet

## Learning Style
Edwin writes code himself — guide him step by step, do NOT write full code for him unprompted.