import pandas as pd
import numpy as np
from utils import read_config_file
from numpy import linalg as LA

def index_documents(config_file):
  print("Reading config files...")
  config_dict = read_config_file(config_file)
  inverted_index_file = config_dict["leia"]
  term_document_matrix_file = config_dict["escreva"]

  print("Reading inverted index file...")
  inverted_index_df = pd.read_csv(inverted_index_file, sep=';')

  records_num = get_records_num_set(inverted_index_df)
  words = inverted_index_df["Word"].tolist()
  print(f"Inverted index dimensions: ({len(words)},{len(records_num)}).")

  print("Computing terms-documents matrix from inverted index...")
  term_document_matrix = compute_term_document_matrix(inverted_index_df, records_num)

  print("Creating terms-documents matrix file...")
  term_document_df = pd.DataFrame(data=term_document_matrix, index=words, columns=records_num)
  term_document_df.to_csv(term_document_matrix_file, sep=";")

  print("Done!")

def get_records_num_set(inverted_index_df):
  inverted_index_df["RecordNum"] = inverted_index_df["RecordNum"].str.replace("'", "")
  inverted_index_df["RecordNum"] = inverted_index_df["RecordNum"].str.replace(" ", "")
  records_num = set([record_num for word in inverted_index_df["RecordNum"].str[1:-1].str.split(",").tolist() for record_num in word])

  return records_num

def compute_term_document_matrix(inverted_index_df, records_num):
  terms_frequencies = []

  for record_num in records_num:
    terms_frequencies.append(inverted_index_df["RecordNum"].str.count(record_num))

  # Tf-Idf implementation based on ScikitLearn: https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
  terms_frequencies = np.array(terms_frequencies).T

  number_of_documents = terms_frequencies.shape[-1]
  terms_occurence_on_documents = np.sum(np.where(terms_frequencies > 0, 1, 0), axis=1)
  terms_idf = (np.log((1 + number_of_documents)/(1 + terms_occurence_on_documents)) + 1).reshape((terms_occurence_on_documents.shape[0], 1))

  term_document_matrix = terms_frequencies * terms_idf
  term_document_matrix = term_document_matrix / LA.norm(term_document_matrix, axis=0)

  return term_document_matrix