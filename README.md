# Dense Passage Retrieval (DPR) for WISEST

Welcome to the `dpr.py` module, an integral part of the **WISEST** (WhIch Systematic Evidence Synthesis is besT) tool. This module enables automated passage retrieval for systematic review (SR) quality assessments by leveraging advanced information retrieval techniques. It plays a key role in facilitating efficient, automated responses to widely recognized frameworks such as **ROBIS** and **AMSTAR-2**.

## Overview

WISEST aims to streamline the assessment process for SRs, which are essential for evidence-based decision-making in healthcare and policy. The `dpr.py` module uses dense passage retrieval (DPR) to identify relevant text passages that align with quality appraisal questions, thus reducing manual effort and enhancing consistency.

### Key Features
- **BM25 Matching**: Utilizes the BM25Okapi algorithm for initial scoring and retrieval of relevant passages.
- **Data Pre-processing**: Cleans and standardizes SR content, ensuring it is formatted correctly for retrieval.
- **Support for ROBIS and AMSTAR-2**: Provides structured question-answer pairs tailored to these established quality assessment frameworks.
- **Automated Data Formatting**: Generates JSON outputs suitable for training or evaluating retrieval models.

## Installation

### Prerequisites
- **Python 3.7+**
- **Required Python packages**:
  ```bash
  pip install unidecode pandas rank_bm25 nltk
  ```
- **NLTK Data**: Ensure the `punkt` tokenizer is available:
  ```python
  import nltk
  nltk.download('punkt')
  ```

### Setup
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/your-repo/WISEST-DPR.git
cd WISEST-DPR
```

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

## Customization

### Paths and Data
- Adjust the file paths in the `pre_process_quote()` function and the `updated_passage_to_retriever_format()` function as needed to match your directory structure.
- Modify the questions or data formats if additional customization is required for specific use cases.

## Best Practices and Tips
- Ensure input CSVs are clean and formatted correctly for optimal pre-processing.
- Use high-quality passage data for more accurate retrieval outputs.
- The output JSON can be used for training machine learning models or as input for other evaluation tools.

## Contributing

Contributions to improve the module are welcome! Fork the repository, create a new branch, and submit a pull request with your changes. Ensure code adheres to PEP 8 standards for consistency.

## License

This module is part of the WISEST project and is distributed under the [CC-BY-NC License](https://creativecommons.org/licenses/by-nc/4.0/).

## References

For more details on the WISEST tool and its comprehensive functionalities, refer to:
- **WISEST Annotation Platform**: [GitHub Repository]([https://github.com/radinhamidi/WISEST-Annotation-Platform](https://github.com/radinhamidi/WISEST-Annotation-Platform.git))

---

