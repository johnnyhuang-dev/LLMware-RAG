"""
Beginner-friendly RAG tutorial script using llmware.
"""

from pathlib import Path
from llmware.configs import LLMWareConfig
from llmware.setup import Setup
from llmware.library import Library

LLMWareConfig().set_active_db("sqlite")
LLMWareConfig().set_debug_mode(1)
sample_files_path = Setup().load_sample_files(over_write=False)
agreements_folder = Path(sample_files_path) / "Agreements"


def main() -> None:
    pass


if __name__ == "__main__":
    main()
