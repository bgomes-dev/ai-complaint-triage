# AI Complaint Triage & Routing Assistant

An LLM-based prototype for automatically classifying banking complaints according to a predefined banking complaint taxonomy.

The project explores how a Large Language Model (LLM) can be used to support the initial triage of customer complaints by identifying the relevant **Product** and **Matter**, while using confidence-based business rules to determine whether a case can be automatically approved or should be reviewed by a human.

---

## Project Overview

Financial institutions receive large volumes of customer complaints that need to be classified and routed according to predefined categories.

The objective of this project is to investigate whether an LLM can perform this classification accurately enough to support an initial triage process.

The prototype follows this workflow:

```text
Customer Complaint
        ↓
       LLM
        ↓
Product + Matter + Confidence
        ↓
Output Validation
        ↓
Confidence Threshold
        ↓
Approved / Needs Review
        ↓
Evaluation against Human Ground Truth
        ↓
Error Analysis
```

The project focuses on **classification, evaluation and human-in-the-loop decision support**, rather than fully automating complaint handling.

---

## Research Question

> **Can an LLM accurately classify banking complaints according to a predefined Product → Matter taxonomy, and can confidence-based routing be used to identify cases that require human review?**

---

## Dataset

The project uses a synthetic sample of **50 banking complaints** created to cover different areas of the official complaint taxonomy.

Each complaint contains:

* Complaint ID
* Complaint text

The project also contains a human-created ground truth used as an independent reference for evaluating the LLM predictions.

The taxonomy is stored separately and acts as the source of truth for the valid Products and Matters that the model can select.

---

## Methodology

### 1. Taxonomy-based classification

The LLM receives the official complaint taxonomy as context.

The taxonomy follows a hierarchical structure:

```text
Product
    ↓
Matter
```

The model must select:

* one valid Product;
* one Matter belonging to that Product;
* a confidence value between 0 and 1.

The model is explicitly instructed not to invent or modify taxonomy categories.

---

### 2. Structured output

The expected LLM output is:

```json
{
  "complaint_id": "001",
  "product": "Direct debits",
  "matter": "SEPA direct debits",
  "confidence": 0.92
}
```

The output is then validated in Python to ensure that:

* all required fields are present;
* confidence is numeric;
* confidence is between 0 and 1;
* the Product exists in the official taxonomy;
* the Matter belongs to the selected Product.

---

### 3. Confidence-based routing

A business threshold of **0.80** is applied after classification.

```text
Confidence >= 0.80
        ↓
    Approved

Confidence < 0.80
        ↓
  Needs Review
```

The confidence value is treated as a model self-assessment rather than a statistically calibrated probability.

The business rule is therefore kept separate from the LLM itself.

---

## Evaluation

The LLM predictions are compared against an independently created human ground truth.

Three main metrics are calculated:

* **Product Accuracy** — whether the correct Product was identified.
* **Matter Accuracy** — whether the correct Matter was identified.
* **Overall Accuracy** — whether both Product and Matter were correctly identified.

The evaluation also identifies individual classification errors so that the model's failures can be analysed rather than relying only on aggregate accuracy.

### Current results

The current experiment produced:

| Metric                    |  Result |
| ------------------------- | ------: |
| Product Accuracy          |     94% |
| Matter Accuracy           |     94% |
| Overall Accuracy          |     94% |
| Correct Classifications   | 47 / 50 |
| Incorrect Classifications |  3 / 50 |

These results are based on the current 50-complaint sample and should not be interpreted as evidence of production-level model performance.

---

## Error Analysis

An important part of the project is understanding **where the model fails**.

For every complaint, the evaluation stores:

* Original complaint text
* Expected Product
* Expected Matter
* Predicted Product
* Predicted Matter
* Model confidence
* Classification result
* Routing status

This makes it possible to investigate individual errors and understand whether mistakes are related to ambiguous complaint descriptions, similar taxonomy categories, or model uncertainty.

---

## Dashboard

The evaluation results are exported to:

```text
results/evaluation_results.json
```

A standalone HTML dashboard reads this JSON file and presents the results interactively.

The dashboard includes:

* Overall performance KPIs
* Product, Matter and Overall Accuracy
* Approved vs Needs Review cases
* Complaint-level classification results
* Filtering by routing status and classification result
* Classification error analysis
* Human ground truth vs LLM predictions
* Model confidence
* Complaints requiring human review

The dashboard is located in:

```text
dashboard/dashboard.html
```

The dashboard is intentionally separated from the notebook so that the analysis pipeline produces a reusable results file, while the HTML is responsible only for presenting those results.

---

## Project Structure

```text
ai-complaint-triage/
│
├── data/
│   ├── taxonomy.json
│   ├── complaints_sample.jsonl
│   └── ground_truth.jsonl
│
├── notebooks/
│   └── 01_llm_classification.ipynb
│
├── results/
│   └── evaluation_results.json
│
├── dashboard/
│   └── dashboard.html
│
├── README.md
└── requirements.txt
```

### `data/`

Contains the input data used by the experiment.

* `taxonomy.json` — official Product → Matter taxonomy.
* `complaints_sample.jsonl` — sample of banking complaints used for classification.
* `ground_truth.jsonl` — human reference classifications used for evaluation.

### `notebooks/`

Contains the main experimentation notebook.

`01_llm_classification.ipynb` handles:

* data loading;
* taxonomy preparation;
* prompt construction;
* LLM API requests;
* structured output parsing;
* validation;
* confidence-based routing;
* evaluation;
* results export.

### `results/`

Contains the structured output produced by the notebook.

`evaluation_results.json` acts as the data source for the dashboard.

### `dashboard/`

Contains the standalone HTML dashboard used to visualise and explore the evaluation results.

---

## Technologies

* Python
* Jupyter Notebook
* Pandas
* JSON / JSONL
* REST API
* Large Language Models
* HTML
* CSS
* JavaScript

---

## Key Concepts Demonstrated

This project was designed to explore several practical concepts involved in building LLM-based data applications:

* LLM API integration
* Prompt engineering
* Context and taxonomy-based classification
* Structured outputs
* Output validation
* Confidence-based business rules
* Ground-truth evaluation
* Classification metrics
* Error analysis
* Human-in-the-loop workflows
* Separation between model logic, business logic and presentation

---

## Limitations

This is a proof-of-concept rather than a production system.

The main limitations include:

* The evaluation dataset contains only 50 complaints.
* The complaints are synthetic examples rather than real customer data.
* The evaluation sample is relatively small.
* Model confidence is not statistically calibrated.
* The results may vary depending on the selected LLM.
* No production deployment or automated human-review workflow is implemented.

The purpose of the project is to demonstrate the methodology and technical approach, not to claim that the model is ready for production use.

---

## Future Improvements

Potential next steps include:

* Expanding the evaluation dataset.
* Including more difficult and ambiguous complaints.
* Performing deeper error analysis.
* Comparing multiple LLMs.
* Testing different prompts and classification strategies.
* Evaluating confidence calibration.
* Introducing a human-review workflow for `Needs Review` cases.
* Monitoring model performance over time.
* Testing the approach on real anonymised complaint data.

---

## Author

This project was developed as a practical exploration of applying Large Language Models to data classification and decision-support problems in a financial-services context.
