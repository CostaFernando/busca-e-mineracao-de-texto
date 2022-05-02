from utils import read_config_file, process_string, create_csv_file
import xml.etree.ElementTree as ET

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

def get_queries_from_cfquery_file(cfquery_file):
  tree = ET.parse(cfquery_file)
  cfquery_root = tree.getroot()

  queries = []
  for query in cfquery_root.iter('QUERY'):
    query_number = query.find("QueryNumber").text
    query_text = process_string(query.find("QueryText").text)
    queries.append([query_number, query_text])

  return queries

def get_expected_results_from_cfquery_file(cfquery_file):
  tree = ET.parse(cfquery_file)
  cfquery_root = tree.getroot()

  expected_results = []
  for query in cfquery_root.iter('QUERY'):
    query_number = query.find("QueryNumber").text

    records = query.find("Records")
    for item in records:
      doc_number = item.text
      doc_votes = compute_doc_votes(item.attrib["score"])
      expected_results.append([query_number, doc_number, doc_votes])

  return expected_results

def compute_doc_votes(score):
  votes_sum = 0
  for vote in score:
    votes_sum += int(vote)
  
  return votes_sum