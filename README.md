# WISEST Data Processing Module

Welcome to the `WISEST Data` repository, a core component of **WISEST (WhIch Systematic Evidence Synthesis is besT)**. This repository contains the tools and processes required to transform raw systematic review (SR) data into structured datasets for automated quality assessment using Dense Passage Retrieval (DPR) and question-answering models.

## Overview

WISEST is designed to streamline quality assessments of systematic reviews (SRs) through automation. By applying natural language processing (NLP) and information retrieval techniques, WISEST addresses the need for efficient, consistent quality appraisals aligned with the AMSTAR-2 and ROBIS frameworks. This repository encompasses the entire data processing pipeline, from text extraction to dataset generation.



## Key Features
- **BM25 Matching**: Utilizes the BM25Okapi algorithm for initial scoring and retrieval of relevant passages.
- **Data Pre-processing**: Cleans and standardizes SR content, ensuring it is formatted correctly for retrieval.
- **Support for ROBIS and AMSTAR-2**: Provides structured question-answer pairs tailored to these established quality assessment frameworks.
- **Automated Data Formatting**: Generates JSON outputs suitable for training or evaluating retrieval models.

---

## Table of Contents

1. [Text Extraction Process](#text-extraction-process)
2. [Generating Passages](#generating-passages)
3. [Retrieving Relevant Passages](#retrieving-relevant-passages)
4. [Creating the DPR Dataset](#creating-dpr-dataset)
5. [Creating the Question-Answering Dataset](#creating-question-answering-dataset)
6. [Installation and Prerequisites](#installation-and-prerequisites)
7. [Usage](#usage)

---

### 1. Text Extraction Process

The first step in the pipeline involves extracting text from PDF documents of systematic reviews, applying rigorous data cleaning, and formatting the text for model training. Key steps include:

- **Using PyMuPDF for Text Extraction**: This tool extracts text in natural reading order, which is essential for multi-column SR documents.
- **Data Cleaning**: Based on the WISEST documentation:
  - Remove non-informative content (e.g., page numbers, headers/footers).
  - Capture bibliographic information from DOI.
  - Isolate the abstract and eliminate introductory content.
  - Filter out statistical tables and images.
  - Consolidate short text blocks to optimize for model input length.


### 2. Generating Passages

Once the text has been cleaned, the next step involves splitting it into manageable text passages. This ensures each text block is appropriately formatted for passage-based retrieval models.

- **Passage Structure**: Each passage consists of 512 tokens with an overlap of 50 tokens for continuity.
- **JSON Format**: Each passage is saved in a JSON format, containing a unique identifier (`id`) and the passage text (`contents`).


### 3. Retrieving Relevant Passages

With passages created, we proceed to retrieve relevant sections for each quality question in ROBIS and AMSTAR-2 using DPR and Crossencoder techniques.

- **BM25 Matching**: Initial retrieval of relevant text passages using BM25 for baseline relevance scoring.
- **Dense Passage Retrieval (DPR)**: A dense passage retrieval model aligns passage embeddings with quality questions, optimized through fine-tuning for AMSTAR-2 and ROBIS.
- **Crossencoder for Enhanced Relevance**: Crossencoder fine-tuning with a Sentence-BERT structure improves semantic similarity in retrieved passages.


### 4. Creating the DPR Dataset

The next step is generating a Dense Passage Retrieval (DPR) dataset using labeled passages from the text extraction and retrieval processes.

- **Positive and Negative Contexts**: Passages are labeled as positive or negative based on their relevance to quality questions. Positive contexts contain quotes aligned with ROBIS or AMSTAR-2, while negative contexts lack relevant answers.
- **JSON Format for DPR**: Each entry includes `question`, `answers`, `positive_ctxs`, and `negative_ctxs`.

See [WISEST Project Protocol](#) for more details on constructing the DPR dataset format.

### 5. Creating the Question-Answering Dataset

For downstream question-answering (QA) tasks, we create a dataset that aligns questions from ROBIS and AMSTAR-2 with answers extracted from the SRs.

- **Structured QA Pairs**: Each question-answer pair is formatted with `question`, `answer`, `context`, `positive_ctxs`, and `negative_ctxs`.
- **JSON Format for QA Models**: Outputs are structured to train transformer-based models, such as BERT or RoBERTa, on question-answering tasks.


---

## Installation

### Prerequisites
- **Python 3.7+**
- **Required Python packages**:
  ```bash
  pip install -r requirements.txt
  ```
- **NLTK Data**: Ensure the `punkt` tokenizer is available:
  ```python
  import nltk
  nltk.download('punkt')
  ```

### Setup
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/radinhamidi/WISEST-Data.git
cd WISEST-DPR
```

---

## How It Works

### Workflow Overview
1. **Pre-process SR Quotes**: Cleans and decodes data from input CSV files containing SRs.
2. **Match Passages**: Uses BM25 to score and match passages against provided questions.
3. **Generate Structured JSON**: Outputs a JSON file with question-answer pairs, positive context indices, and negative context indices.

### Example Usage

#### 1. Pre-process the Data
```python
df_robis, df_amstar = pre_process_quote()
```
- **Description**: Cleans and standardizes CSV data for SRs, preparing it for the retrieval process.

#### 2. Match Passages with BM25
```python
best_match_index = bm25_match(passage_list, query)
```
- **Description**: Finds the best matching passage for a given query using BM25 scoring.

#### 3. Generate Output in Retriever Format
```python
updated_passage_to_retriever_format('input_file.json', 'output_file.json')
```
- **Description**: Reads data from the input JSON file and produces an output JSON with structured retrieval data.

---

## Input/Output Details

### Input
- **CSV Files**: Containing systematic review data, with columns representing questions and corresponding answers.
- **JSON File**: A file with text passages to be scored and matched.

### Output
- **Structured JSON File**:
  - **`question`**: The question text, derived from the ROBIS or AMSTAR-2 frameworks.
  - **`answers`**: Relevant answers extracted from the corresponding SR.
  - **`positive_ctxs`**: A list of indices representing passages identified as positive matches.
  - **`negative_ctxs`**: A list of indices representing passages that are not matched as relevant (negative examples for model training).
- **Format**:
  ```json
  [
    {
      "question": "Sample question from ROBIS or AMSTAR-2",
      "answers": ["Relevant answer 1", "Relevant answer 2"],
      "positive_ctxs": [0, 2],
      "negative_ctxs": [3, 5]
    },
    ...
  ]
  ```

---

## Customization

### Paths and Data
- Adjust the file paths in the `pre_process_quote()` function and the `updated_passage_to_retriever_format()` function as needed to match your directory structure.
- Modify the questions or data formats if additional customization is required for specific use cases.

## Best Practices and Tips
- Ensure input CSVs are clean and formatted correctly for optimal pre-processing.
- Use high-quality passage data for more accurate retrieval outputs.
- The output JSON can be used for training machine learning models or as input for other evaluation tools.

---

## Contributing

Contributions to improve the module are welcome! Fork the repository, create a new branch, and submit a pull request with your changes. Ensure code adheres to PEP 8 standards for consistency.

## License

This module is part of the WISEST project and is distributed under the [CC-BY-NC License](https://creativecommons.org/licenses/by-nc/4.0/).

## References

For more details on the WISEST tool and its comprehensive functionalities, refer to:
- **WISEST Annotation Platform**: [GitHub Repository](https://github.com/radinhamidi/WISEST-Annotation-Platform.git).

---
