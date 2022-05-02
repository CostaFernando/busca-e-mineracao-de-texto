# IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

<img width="680" alt="image" src="https://user-images.githubusercontent.com/17749414/166241418-d8f47e53-4db4-443b-835e-d125197658bb.png">

**Módulos**:
* Processador de Consultas (query_processor.py): Processa as queries originais do arquivo cfquery.xml em dois arquivos csv.
* Gerador Lista Invertida (inverted_index_generator.py): Gera um índice invertido em csv a partir de leitura full text de um conjunto de documentos cf[id].xml.
