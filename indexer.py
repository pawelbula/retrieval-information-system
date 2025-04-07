import gzip
import json
import re
import os
from collections import defaultdict
from Stemmer import Stemmer
from nltk.corpus import stopwords
import psutil
import time

class DocumentParser:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def parse_documents(self):
        for root, _, files in os.walk(self.data_dir):
            for filename in files:
                if filename.endswith('.jsonl.gz'):
                    file_path = os.path.join(root, filename)
                    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                        for line in file:
                            data = json.loads(line)
                            pmid = data.get('pmid', '')  # id
                            title = data.get('title', '')  # title
                            abstract = data.get('abstractText', '')  # abstract
                            yield pmid, title + ' ' + abstract
# TODO exception handling

class AdvancedTokenizer:
    def __init__(self, pattern=r'\w+\b', min_chars=3, lowercase=True, stopword_file=None, stemming=False):
        self.pattern = pattern
        self.min_chars = min_chars
        self.lowercase = lowercase
        self.stopword_file = stopword_file
        self.stemming = stemming
        self.stemmer = Stemmer('english')
        self.stopwords = set()

        if self.stopword_file:
            with open(self.stopword_file, 'r', encoding='utf-8') as file:
                self.stopwords.update(word.strip().lower() for word in file if len(word.strip()) >= self.min_chars)

    def tokenize(self, content):
        terms = self.filter_stopw_and_stemming(self.create_tokens(content))
        
        tf_pos = {}
        for i, token in enumerate(terms):
            if token in tf_pos:
                tf_pos[token] = (tf_pos[token][0] + 1, tf_pos[token][1] + f",{i}")
            else:
                tf_pos[token] = (1, str(i))
        return tf_pos

    def create_tokens(self, content):
        return [token.lower().strip('-_') for token in re.findall(self.pattern, content) if len(token.strip('-_')) >= self.min_chars]
        # return [token.lower().strip('-_') for token in re.split(r"[^\w-]+", content) if len(token.strip('-_')) >= self.min_chars]

    def filter_stopw_and_stemming(self, tokens):
        filtered_tokens = []
        if self.stemming:
            for token in tokens:
                stemmed_token = self.stemmer.stemWord(token)
                if self.stopword_file:
                    if stemmed_token not in self.stopwords:
                        filtered_tokens.append(stemmed_token)
                else:
                    filtered_tokens.append(stemmed_token)
        else:
            for token in tokens:
                if self.stopword_file:
                    if token not in self.stopwords:
                        filtered_tokens.append(token)
                else:
                    filtered_tokens.append(token)
                    
                    return filtered_tokens
                            
    def process_documents(self, parser):
        for pmid, content in parser.parse_documents():
            tokens = self.tokenize(content)
            index.add_document(pmid, tokens)
        
        print("tokenizing doc ID:", pmid)
        print("Tokens in doc:", tokens)           
                    


class SPIMI_Index:
    def __init__(self, output_directory, memory_threshold=90, frequency_check=10):
        self.index = defaultdict(lambda: defaultdict(int)) # structure for index (term -> {doc_id -> term_frequency})
        self.output_directory = output_directory
        self.memory_threshold = memory_threshold
        self.frequency_check = frequency_check
        self.current_doc_id = ''
        self.current_term_frequency = 0
        self.current_tokens = []
        self.last_memory_check = 0

    def add_document(self, doc_id, tokens):
        for token in tokens:
            if doc_id != self.current_doc_id:
                if self.current_doc_id:
                    self.index_tokens(self.current_doc_id, self.current_tokens)
                self.current_doc_id = doc_id
                self.current_tokens = []
                self.current_term_frequency = 0
            self.current_tokens.append(token)
            self.current_term_frequency += 1
            
            if self.frequency_check > 0 and self.current_term_frequency >= self.frequency_check:
                self.check_memory_usage()

    def index_tokens(self, doc_id, tokens):
        for token in tokens:
            self.index[token][doc_id] = self.current_term_frequency

    def check_memory_usage(self):
        current_time = time.time()
        if current_time - self.last_memory_check > 1:
            memory_percent = psutil.virtual_memory().percent
            if memory_percent >= self.memory_threshold:
                self.save_index_to_disk()
                self.last_memory_check = current_time

    def save_index_to_disk(self):
        for term, doc_frequencies in self.index.items():
            with open(os.path.join(self.output_directory, f'{term}.txt'), 'a') as file:
                for doc_id, term_frequency in doc_frequencies.items():
                    file.write(f'{doc_id}:{term_frequency};')
                    
                    
# Next work TODO:
#stemming, stopping, positions (first OFF, before merge?)

#inverted index - is arleady that (after index with freq): term:doc_id,times_it_occured

#dictionary (file)
#after merging -> create dictionary storing every term and where it exist (which line or which file after after)

#count time

#tokenizer config & rest of parameters (last thing?)

if __name__ == '__main':
    data_directory = 'collections'
    parser = DocumentParser(data_directory)
    
    # initialize SPMI indexer
    # TODO mkdir for output

    output_directory = 'index'
    memory_threshold = 90
    frequency_check = 10
    index = SPIMI_Index(output_directory, memory_threshold, frequency_check)
    
    # Below function is about replace to class:
    
    # Iteration by docs indexing and tokenizing:
    # for pmid, content in parser.parse_documents():
    #     tokens = AdvancedTokenizer().tokenize(content)
    #     index.add_document(pmid, tokens)
    
    tokenizer = AdvancedTokenizer()
    tokenizer.process_documents(parser)
    
    index.save_index_to_disk()
