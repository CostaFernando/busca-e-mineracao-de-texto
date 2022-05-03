from query_processor import process_query_file
from inverted_index_generator import generate_inverted_index
from indexer import index_documents
from search_engine import execute_queries_on_index

process_query_file("../config/pc.cfg")
generate_inverted_index("../config/gli.cfg")
index_documents("../config/index.cfg")
execute_queries_on_index("../config/busca.cfg")