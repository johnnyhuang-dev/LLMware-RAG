# Exercises and Troubleshooting

Use these exercises after you run `python src/rag_tutorial.py` at least once.

## How To Use This File

- Do one exercise at a time.
- Predict what will happen before running code.
- Run, observe output, then explain the difference between your prediction and reality.

That reflection loop is how you become independent.

## Exercise 1: Query Sensitivity

Goal: see how retrieval changes with wording.

1. In `src/rag_tutorial.py`, change:
   - `"base salary"` -> `"salary"`
   - then -> `"compensation"`
   - then -> `"holiday allowance"` (or another likely missing phrase)
2. Run script after each change.
3. Compare:
   - result count,
   - source files,
   - text relevance.

Questions:
- Which query gives the most useful context?
- Which query returns noisy chunks?

## Exercise 2: Result Count Tradeoff

Goal: understand precision vs. recall in retrieval.

1. Change `result_count` from `5` to `2`.
2. Run and inspect quality.
3. Change to `10` and run again.

Questions:
- At what point do extra results stop being useful?
- Does bigger context always improve prompts?

## Exercise 3: Prompt Strictness

Goal: control hallucination risk with instructions.

1. Find the prompt text in step 7.
2. Remove this sentence:
   - `Answer using only the provided context.`
3. Compare expected behavior with and without that line.

Questions:
- Why is guardrail wording important in RAG prompts?
- What failure mode are we preventing?

## Exercise 4: Your Own Documents

Goal: transfer the pattern to real data.

1. Add one or two small `.txt` or `.md` files into `data/`.
2. Replace `agreements_folder` with `Path("data")`.
3. Change query to match your custom document content.
4. Run script and inspect fields.

Questions:
- Did chunk text match your expectations?
- Which query terms worked best?

## Exercise 5: Explain Every Symbol

Goal: make sure nothing is "magic".

For each line in `main()`:
- Explain the purpose in one sentence.
- Explain one possible failure case.
- Explain how you would detect the failure from terminal output.

If you cannot explain a line, pause and investigate before adding features.

## Troubleshooting Guide

### Problem: `ModuleNotFoundError: No module named 'llmware'`

Fix:
1. Activate virtual environment.
2. Re-run `pip install -r requirements.txt`.
3. Confirm with `python -c "import llmware; print('ok')"`.

### Problem: No results from query

Likely causes:
- query phrase not present,
- ingestion path incorrect,
- ingestion did not complete.

Checks:
- print `agreements_folder`,
- print library card values (`documents`, `blocks`),
- retry broader query terms.

### Problem: Ingestion seems slow

For learning:
- keep corpus small,
- run with one directory,
- use text files first before PDFs.

### Problem: Script crashes when sample files missing

The script already checks folder existence and raises a clear error.
If this occurs:
1. Re-run script to trigger sample file setup.
2. Verify Python process has filesystem permission.

## Mini Challenge (Optional)

Refactor this project into three modules:
- `src/config.py` (llmware setup)
- `src/ingest.py` (library creation + file ingestion)
- `src/retrieve.py` (query + prompt assembly)

Then write a small `src/main.py` that orchestrates all three.

If you can complete this while keeping behavior unchanged, your understanding is solid.
