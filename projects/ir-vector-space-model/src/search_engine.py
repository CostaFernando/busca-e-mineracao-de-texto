from utils import read_config_file
import pandas as pd
import numpy as np
import re
from numpy import linalg as LA
from nltk.stem import *

def execute_queries_on_index(config_file):
  print("Reading config files...")
  config_dict = read_config_file(config_file)
  term_document_matrix_file = config_dict["modelo"]
  queries_file = config_dict["consultas"]
  queries_results_file = config_dict["resultados"]
  use_stemmer = bool(int(config_dict["use_stemmer"]))

  print("Reading model and queries files...")
  term_document_matrix_df = pd.read_csv(term_document_matrix_file, sep=';', index_col=0, na_filter = False)
  print(f"terms-documents matrix has the following dimensions: ({len(term_document_matrix_df)},{len(term_document_matrix_df.columns)}).")
  queries_df = pd.read_csv(queries_file, sep=';', index_col=0)
  print(f"There are {len(queries_df)} queries.")

  print("Computing queries docs scores...")
  queries_scored_results_data= get_queries_scored_results_data(term_document_matrix_df, queries_df, use_stemmer)
  
  print("Saving queries results...")
  queries_scored_results_df = pd.DataFrame(data=queries_scored_results_data, columns=["QueryNumber", "Results"])
  queries_scored_results_df.to_csv(queries_results_file, sep=";", index=False)

  print("Done!")

def get_queries_scored_results_data(term_document_matrix_df, queries_df, use_stemmer=False):
  ps = PorterStemmer()
  terms_on_index = term_document_matrix_df.index

  def get_queries_vectors(query_text):
    number_of_words = len(terms_on_index)
    query_vector = np.zeros(number_of_words)

    for word in re.findall(r'\w+', query_text):
      if len(word) < 2:
        continue

      if use_stemmer:
        word = ps.stem(word)
        
      word_index = np.flatnonzero(terms_on_index == word)
      query_vector[word_index] = 1

    query_vector = query_vector / LA.norm(query_vector)

    return query_vector

  queries_vectors = queries_df["QueryText"].apply(get_queries_vectors)

  queries_scored_results_data = []
  term_document_matrix = term_document_matrix_df.values
  queries_vectors = queries_vectors.tolist()
  # vectors are normalized, so dot product is the same as cosine similarity
  queries_documents_similarities = np.dot(queries_vectors, term_document_matrix)

  for i, query_documents_similarities in enumerate(queries_documents_similarities):
    query_number = queries_df.index.values[i]
    query_results = []

    for j, query_document_similarity in enumerate(query_documents_similarities):
      if query_document_similarity > 0:
        document_number = term_document_matrix_df.columns[j]
        query_results.append((document_number, query_document_similarity))

    query_results = sorted(query_results, key=lambda tup: tup[1], reverse=True)
    for j, query_result in enumerate(query_results):
      queries_scored_results_data.append([query_number, [j, *query_result]])

  return queries_scored_results_data