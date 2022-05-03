from utils import read_config_file
import pandas as pd
import numpy as np
import re

def execute_queries_on_index(config_file):
  print("Reading config files...")
  config_dict = read_config_file(config_file)
  term_document_matrix_file = config_dict["modelo"]
  queries_file = config_dict["consultas"]
  queries_results_file = config_dict["resultados"]

  print("Reading model and queries files...")
  term_document_matrix_df = pd.read_csv(term_document_matrix_file, sep=';', index_col=0)
  print(f"terms-documents matrix has the following dimensions: ({len(term_document_matrix_df)},{len(term_document_matrix_df.columns)}).")
  queries_df = pd.read_csv(queries_file, sep=';', index_col=0)
  print(f"There are {len(queries_df)} queries.")

  print("Computing queries docs scores...")
  queries_scored_results_data= get_queries_scored_results_data(term_document_matrix_df, queries_df)
  
  print("Saving queries results...")
  queries_scored_results_df = pd.DataFrame(data=queries_scored_results_data, columns=["QueryNumber", "Results"])
  queries_scored_results_df.to_csv(queries_results_file, sep=";", index=False)

  print("Done!")

def get_queries_scored_results_data(term_document_matrix_df, queries_df):
  def get_queries_scored_results(query_text):
    number_of_documents = len(term_document_matrix_df.columns)
    scored_results = np.zeros(number_of_documents)

    for word in re.findall(r'\w+', query_text):
      if word in term_document_matrix_df.index:
        scored_results += term_document_matrix_df.loc[word].values

    return scored_results

  queries_scored_results = queries_df["QueryText"].apply(get_queries_scored_results)

  queries_scored_results_data = []
  for i, query_scored_results in enumerate(queries_scored_results):
    query_number = queries_df.index.values[i]
    query_results = [(term_document_matrix_df.columns[j], scored_result) for j, scored_result in enumerate(query_scored_results)]
    query_results = sorted(query_results, key=lambda tup: tup[1], reverse=True)

    for j, query_result in enumerate(query_results):
      queries_scored_results_data.append([query_number, [j, *query_result]])

  return queries_scored_results_data

execute_queries_on_index("../config/busca.cfg")