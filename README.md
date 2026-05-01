# Beginner-Friendly llmware RAG Learning Project

This project teaches you Retrieval-Augmented Generation (RAG) with `llmware` through one simple, runnable Python script.

The goal is not just to run code.  
The goal is to understand **why every line exists** so you can build your own RAG systems later.

## 1) What You Will Learn

By the end, you should be able to:
- Explain what RAG is in plain language.
- Build a local document retrieval pipeline with `llmware`.
- Inspect query results (`text`, `file_source`, `page_num`, `doc_ID`, `block_ID`).
- Create a grounded prompt from retrieved context.
- Debug common beginner issues.

## 2) RAG in One Mental Model

RAG is a two-part system:
- **Retriever**: finds the most relevant document chunks.
- **Generator (LLM)**: writes the answer using those chunks.

Without retrieval, an LLM guesses from its training data.
With retrieval, the LLM gets fresh, specific evidence.

Flow:
1. Ingest documents.
2. Parse and chunk text.
3. Index chunks.
4. Retrieve relevant chunks for a query.
5. Build prompt with retrieved context.
6. Ask model to answer from that context.

## 3) Project Structure

- `requirements.txt` - Python dependencies
- `src/rag_tutorial.py` - main tutorial script
- `data/README.md` - where to place your own docs later
- `docs/exercises.md` - guided practice after first run

## 4) Environment Setup

### Prerequisites
- Python 3.9 to 3.12
- macOS / Linux / Windows

### Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5) Run the Tutorial Script

From project root:

```bash
python src/rag_tutorial.py
```

The script will:
- configure `llmware` with local SQLite,
- download sample documents,
- create/load a library,
- ingest files,
- run a text query,
- print structured retrieval results,
- build a RAG prompt context.

## 6) Deep Code Walkthrough

This section maps concepts to exact code in `src/rag_tutorial.py`.

### Imports
- `from pathlib import Path`  
  Uses a reliable object-oriented path API (safer than manual string paths).
- `from llmware.configs import LLMWareConfig`  
  Controls `llmware` behavior (database, debug settings).
- `from llmware.library import Library`  
  Creates and manages your knowledge base.
- `from llmware.retrieval import Query`  
  Performs retrieval over indexed library content.
- `from llmware.setup import Setup`  
  Downloads sample files used in beginner examples.

### Step 1: Configuration
- `LLMWareConfig().set_active_db("sqlite")`  
  Sets text collection storage to SQLite (local, no external server).
- `LLMWareConfig().set_config("debug_mode", 1)`  
  Enables lightweight progress visibility during parsing.

### Step 2: Sample Data
- `Setup().load_sample_files(over_write=False)`  
  Downloads or reuses built-in sample docs.
- `over_write=False` avoids deleting and re-downloading when rerun.

### Step 3: Library Lifecycle
- `library_name = "beginner_rag_library"`  
  Stable name helps with repeated runs.
- If the name already exists, `load_library(...)`.
- Otherwise, `create_new_library(...)`.

Why this branch matters: reruns should be predictable and not crash due to duplicate library creation.

### Step 4: Ingestion
- `library.add_files(str(agreements_folder))`  
  Reads supported files, parses text, chunks, and indexes in one call.

In beginner terms, `add_files` is where raw files become searchable knowledge.

### Step 5: Library Card
- `library.get_library_card()` returns metadata.
- Useful keys:
  - `documents`: count of ingested docs
  - `blocks`: count of text chunks
  - `pages`: parsed page count

If `documents` and `blocks` stay zero, ingestion likely failed or path is wrong.

### Step 6: Retrieval
- `q = Query(library)` binds retrieval to this specific library.
- `q.text_query("base salary", result_count=5)` retrieves top matches.

Result fields you inspect:
- `text`: matched chunk text
- `file_source`: source document name/path
- `page_num`: source page number
- `doc_ID`: internal document identifier
- `block_ID`: internal chunk identifier
- `matches`: relevance/matching info

### Step 7: Prompt Construction
The script joins top chunks into `context` and creates a strict prompt:
- "Answer using only the provided context."
- fallback behavior if context is insufficient.

This is the practical core of RAG: retrieved evidence goes directly into prompt context.

## 7) Thinking Framework for Future Projects

Whenever you design a RAG system, ask:
1. **Data**: What documents exist and how noisy are they?
2. **Chunking**: Are chunks too small to preserve meaning or too big to retrieve precisely?
3. **Retrieval**: Is text search enough or do you need semantic retrieval?
4. **Prompting**: Does the prompt force evidence-grounded answers?
5. **Evaluation**: Are answers correct and traceable to source chunks?

## 8) Common Beginner Pitfalls

- Query too specific -> zero results  
  Try broader keywords first.
- Wrong folder path -> nothing ingested  
  Print and verify path before `add_files`.
- Expecting "LLM magic" without retrieval quality  
  Weak retrieval usually means weak answers.
- Large corpus too early  
  Start small; inspect outputs; scale later.

## 9) What To Do Next

1. Complete `docs/exercises.md`.
2. Replace sample docs with your own in `data/`.
3. Change query terms and compare result quality.
4. Add semantic retrieval once text retrieval feels clear.

## 10) Official References Used

- [llmware Fast Start](https://llmware-ai.github.io/llmware/getting_started/fast_start)
- [llmware Introduction by Examples](https://llmware-ai.github.io/llmware/examples/getting_started)
- [llmware Query docs](https://llmware-ai.github.io/llmware/components/query)
