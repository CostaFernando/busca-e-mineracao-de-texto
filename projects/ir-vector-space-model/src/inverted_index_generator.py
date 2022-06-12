from utils import read_config_file, process_string, create_csv_file
import xml.etree.ElementTree as ET
import re
from nltk.stem import *

def generate_inverted_index(config_file):
  print("Reading config files...")
  config_dict = read_config_file(config_file)
  cf_files = config_dict["leia"].split(',')
  use_stemmer = bool(int(config_dict["use_stemmer"]))
  ps = PorterStemmer()

  print("Reading cf files...")
  records = get_records_from_cf_files(cf_files)
  print(f"There are {len(records)} records.")
  
  print("Computing inverted index...")
  inverted_index = {}
  for record in records:
    for word in re.findall(r'[a-zA-Z]+', record["text"]):
      if len(word) < 2:
        continue

      if use_stemmer:
        word = ps.stem(word)

      if word in inverted_index:
        inverted_index[word].append(record["number"])
      else:
        inverted_index[word] = [record["number"]]
  print(f"Terms in inverted index: {len(inverted_index)}.")
  
  print("Creating inverted index file...")
  header = ["Word", "RecordNum"]
  expected_results_file = config_dict["escreva"]
  create_csv_file(expected_results_file, header, inverted_index.items())

  print("Done!")

def get_records_from_cf_files(cf_files):
  records = []

  for cf_file in cf_files:
    tree = ET.parse(cf_file)
    cf_root = tree.getroot()

    for record in cf_root.iter('RECORD'):
      record_number = record.find("RECORDNUM").text

      record_text = ""
      record_abstract = record.find("ABSTRACT")
      record_extract = record.find("EXTRACT")
      if record_abstract != None:
        record_text = process_string(record_abstract.text)
      elif record_extract != None:
        record_text = process_string(record_extract.text)

      records.append({"number": record_number, "text": record_text})

  return records