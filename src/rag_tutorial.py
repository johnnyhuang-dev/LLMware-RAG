"""
Beginner-friendly RAG tutorial script using llmware.
"""

from pathlib import Path
from llmware.configs import LLMWareConfig
from llmware.setup import Setup
from llmware.library import Library
from llmware.prompts import Prompt
from llmware.retrieval import Query

# Local generative model from the llmware catalog.
# First run downloads weights, so it needs network once.
LLM_MODEL_NAME = "llmware/bling-1b-0.1"


def main() -> None:
    # 1. Configure llmware
    LLMWareConfig().set_active_db("sqlite")
    LLMWareConfig().set_config("debug_mode", 1)

    # 2. Download sample files
    sample_files_path = Setup().load_sample_files(over_write=False)

    # 3. Define the folder to ingest
    agreements_folder = Path(sample_files_path) / "Agreements"
    
    # 4. Create or load the library
    library_name = "beginner_rag_library"

    # 5. Check if the library already exists
    if Library().check_if_library_exists(library_name):
        library = Library().load_library(library_name)
        print(f"Loaded existing library: {library_name}")
    else:
        library = Library().create_new_library(library_name)
        print(f"Created new library: {library_name}")
    
    if not agreements_folder.exists():
        raise FileNotFoundError(
            f"Expected folder not found: {agreements_folder}. "
            "Check sample file download and try again."
        )
    
    # 6. Ingest the files
    ingestion_result = library.add_files(str(agreements_folder))
    print("Ingestion finished")
    print(f"Ingestion return type: {type(ingestion_result).__name__}")

    # 7. Get the library card (records summary of library) for debugging add_files
    card = library.get_library_card()
    print(f"documents: {card.get('documents', 'N/A')}")
    print(f"blocks: {card.get('blocks', 'N/A')}")
    print(f"pages: {card.get('pages', 'N/A')}")

    # 8. Create a query
    query_text = "base salary"
    result_count = 5

    q = Query(library)
    results = q.text_query(query_text, result_count=result_count)
    print(f"Query: {query_text}")
    print(f"Requested: {result_count} results")
    print(f"Returned: {len(results)} results")

    # 9. Check if there are results
    if not results:
        print("Try a broader query")
        return
    
    # 10. Print the results
    for i, result in enumerate(results, start=1):
        print(f"\nResult #{i}:")
        print(f"file_source: {result.get('file_source', 'N/A')}")
        print(f"page_num: {result.get('page_num', 'N/A')}")
        print(f"doc_ID: {result.get('doc_ID', 'N/A')}")
        print(f"block_ID: {result.get('block_ID', 'N/A')}")
        print(f"matches: {result.get('matches', 'N/A')}")
        print(f"text:")
        print(result.get('text', '').strip())

    # 11. Build a prompt
    top_k_for_context = 3
    context_blocks = [item.get("text", "").strip() for item in results[0:top_k_for_context]]
    context = "\n\n".join(context_blocks)

    user_question = "What is the policy around base salary in these documents?"

    prompt = (
        "You are a careful assistant.\n"
        "Answer using only the provided context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{user_question}\n\n"
        "If the context does not contain the answer, say 'I don't have enough context to answer.'"
    )

    print("\nConstructed prompt:")
    print("-" * 40)
    print(prompt)
    print("-" * 40)

    # 12. Generate an answer using 
    print("\nLoading model and running inference...")
    prompter = Prompt(llm_name=LLM_MODEL_NAME, library=library)
    prompter.set_inference_parameters(temperature=0.3, llm_max_output_len=500)
    response = prompter.prompt_main(prompt)
    print("\nLLM response:")
    print("-" * 40)
    print(response.get("llm_response", response))
    print("-" * 40)


if __name__ == "__main__":
    main()
