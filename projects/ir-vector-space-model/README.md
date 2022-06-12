# IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

<img width="680" alt="image" src="https://user-images.githubusercontent.com/17749414/166241418-d8f47e53-4db4-443b-835e-d125197658bb.png">

### Módulos

Os módulos estão na pasta /src.

- Processador de Consultas (query_processor.py): Processa as queries originais do arquivo cfquery.xml em dois arquivos csv.
- Gerador Lista Invertida (inverted_index_generator.py): Gera um índice invertido em csv a partir de leitura full text de um conjunto de documentos cf[id].xml.
- Indexador (indexer.py): Gera uma matrix termo-documento com pesos TF-IDF em csv a partir de um arquivo csv de índice invertido.
- Buscador (search_engine.py): Gera um arquivo csv contendo os resultados rankeados de cada uma das buscas presentes no arquivo de buscas.
- Avaliador (search_engine_evaluation.ipynb): Avalia o mecanismo de busca com base em 9 métricas.

Na pasta /avalia, encontram-se métricas de desempenho do sistema de busca.
