# Projeto RPCW 2025 — Ficha

## Descrição do Trabalho

Este projeto consiste na modelação e povoamento de uma ontologia sobre conceitos, disciplinas, mestres, obras e aprendizes, com base no enunciado fornecido no ficheiro [`rpcw2025-normal.pdf`](rpcw2025-normal.pdf). Foram criados ficheiros de dados em formato JSON e Turtle (TTL), bem como um conjunto de queries SPARQL para exploração e manipulação da ontologia.

## O que foi feito

- **Modelação da Ontologia**: Definição das classes principais (Conceito, Disciplina, Mestre, Obra, Aprendiz, Aplicação, etc.) e suas relações.
- **Povoamento**: Criação de ficheiros `.ttl` com instâncias reais, baseadas nos ficheiros `.json` fornecidos.
- **Queries SPARQL**: Implementação de queries para responder às perguntas do enunciado, incluindo queries de seleção, agregação, e inserção de novos triplos (ex: relações `estudaCom` e `dáBasesPara`).
- **Documentação**: Este ficheiro (`PR.md`) explica o processo e como replicar os cenários.

## Como replicar os cenários

1. **Pré-requisitos**:
   - Ter instalado um triplestore compatível com SPARQL 1.1 (ex: Apache Jena Fuseki, GraphDB, etc.).
   - Importar os ficheiros `.ttl` da pasta para o triplestore.

2. **Povoamento dos dados**:

Usamos a ontologia base `sepientia_base.ttl` como base para o povoamento

#### Povoar Conceitos
Usa a `sepientia_base.ttl` como base o o json conceitos.json

python povoCoceitos.py 


#### Povoar Disciplinas 
Usa a `sapientia_povoada_conceitos.ttl` como base o o json disciplinas.json

python povDisiciplinas.py 


#### Povoar Mestres 
Usa a `sapientia_povoada_disciplinas.ttl` como base o o json mestres.json

python povMestres.py 

#### Povoar Obras 
Usa a `sapientia_povoada_mestres.ttl` como base o o json obras.json

python povObras.py 

#### Povoar Aprendizes 
Usa a `sapientia_povoada_obras.ttl` como base o o json pg55980.json e dá o resultado final `sapientia_ind.ttl`

python povAprendizes.py 


3. **Execução das queries**:
   - Abrir o endpoint SPARQL do triplestore.
   - Copiar as queries do ficheiro [`sparql.txt`](sparql.txt) e executar.
   - As queries estão numeradas e comentadas para corresponder às perguntas do enunciado do PDF.

4. **Queries de inserção**:
   - As queries `INSERT` (ex: para as relações `estudaCom` e `dáBasesPara`) podem ser executadas diretamente para adicionar novos triplos à ontologia.





