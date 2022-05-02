from utils import read_config_file, process_string, create_csv_file
import xml.etree.ElementTree as ET
import re

def generate_inverted_index(config_file):
  config_dict = read_config_file(config_file)
  cf_files = config_dict["leia"].split(',')

  records = get_records_from_cf_files(cf_files)
  
  inverted_index = {}
  for record in records:
    for word in re.findall(r'\w+', record["text"]):
      if word in inverted_index:
        inverted_index[word].append(record["number"])
      else:
        inverted_index[word] = [record["number"]]
  
  header = ["Word", "RecordNum"]
  expected_results_file = config_dict["escreva"]
  create_csv_file(expected_results_file, header, inverted_index.items())

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