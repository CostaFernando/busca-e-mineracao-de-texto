import configparser
import xml.etree.ElementTree as ET
import csv
import unicodedata

def process_query_file(config_file):
  config_dict = read_config_file(config_file)
  cfquery_file = config_dict["leia"]
  
  header = ["QueryNumber", "QueryText"]
  queries = get_queries_from_cfquery_file(cfquery_file)
  queries_file = config_dict["consultas"]
  create_csv_file(queries_file, header, queries)

  header = ["QueryNumber", "DocNumber", "DocVotes"]
  expected_results = get_expected_results_from_cfquery_file(cfquery_file)
  expected_results_file = config_dict["esperados"]
  create_csv_file(expected_results_file, header, expected_results)
    

def read_config_file(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  
  config_dict = dict(config.items("DEFAULT"))

  return config_dict

def get_queries_from_cfquery_file(cfquery_file):
  tree = ET.parse(cfquery_file)
  cfquery_root = tree.getroot()

  queries = []
  for query in cfquery_root.iter('QUERY'):
    query_number = query[0].text
    query_text = process_string(query[1].text)
    queries.append([query_number, query_text])

  return queries

def get_expected_results_from_cfquery_file(cfquery_file):
  tree = ET.parse(cfquery_file)
  cfquery_root = tree.getroot()

  expected_results = []
  for query in cfquery_root.iter('QUERY'):
    query_number = query[0].text

    records = query[3]
    for item in records:
      doc_number = item.text
      doc_votes = compute_doc_votes(item.attrib["score"])
      expected_results.append([query_number, doc_number, doc_votes])

  return expected_results

def process_string(string_to_process):
  processed_string = string_to_process.replace(";", "")
  processed_string = unicodedata.normalize("NFD", processed_string).encode("ascii", "ignore").decode("utf-8")
  processed_string = processed_string.upper()

  return processed_string

def create_csv_file(file_to_write, header, data):
  with open(file_to_write, 'w', encoding='UTF8') as f:
    writer = csv.writer(f, delimiter=';')

    writer.writerow(header)
    writer.writerows(data)

def compute_doc_votes(score):
  votes_sum = 0
  for vote in score:
    votes_sum += int(vote)
  
  return votes_sum


process_query_file("pc.cfg")