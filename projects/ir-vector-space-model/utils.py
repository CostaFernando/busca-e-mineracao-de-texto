import configparser
import csv
import unicodedata

def read_config_file(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  
  config_dict = dict(config.items("DEFAULT"))

  return config_dict

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