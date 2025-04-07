# The Information Retrieval System (Assignment project 2023)
 
This repository contains the CLI definition for implementing a fully functional IR system, with indexing, searching and evaluation capabilities.

## Table-of-Contents

* [Overview](#overview)
  * [Indexer Mode](#indexer-mode)
  * [Searcher Mode](#searcher-mode)
  * [Evaluator Mode](#evaluator-mode)
* [Usage](#usage)
* [Installation](#installation)
* [Info](#info)

## Overview
Command-line information retrieval system with three main components:

### Indexer Mode
Builds inverted index from document collections with configurable settings:
```bash
python main.py indexer <collection.jsonl> <index_folder> [options]
```
Key features:
- SPIMI algorithm support
- Configurable RAM usage
- Term position storage
- BM25/TF-IDF scoring

### Searcher Mode
Query processing in two modes:
```bash
# Interactive mode
python main.py searcher interactive <index_folder> [--top_k N]

# Batch mode
python main.py searcher batch <index_folder> <queries_file> <output_file>
```
Features:
- BM25 and TF-IDF ranking
- Configurable top-k results
- Interactive and batch processing

### Evaluator Mode
Performance assessment using standard IR metrics:
```bash
python main.py evaluator <gold_standard> <results_file>
```
Metrics: F1, nDCG, MAP

## Usage

Basic indexing example:
```bash
python main.py indexer collections/pubmed_tiny.jsonl pubmed_index \
  --tokenizer.minL 3 \
  --tokenizer.stopwords stopw.txt \
  --tokenizer.stemmer potterNLTK
```

## Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Info

- Index format must follow standard specification
- Tokenizer configuration is stored with index
- CLI can be extended using argparse argument groups

For detailed help on any mode:
```bash
python main.py <mode> --help
```
