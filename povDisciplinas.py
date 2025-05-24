import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF

# Carrega o grafo da ontologia base
g = Graph()
g.parse("sapientia_povoada_conceitos.ttl", format="turtle") 


EX = Namespace("http://www.semanticweb.org/historiaas/")

with open("disciplinas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for disciplina in data["disciplinas"]:
    nome_disciplina = disciplina["nome"].replace(" ", "_").replace("-", "_")
    uri_disciplina = EX[nome_disciplina + "_Disciplina"]

    # Cria a instância da disciplina
    g.add((uri_disciplina, RDF.type, EX.Disciplina))
    g.add((uri_disciplina, EX.nome, Literal(disciplina["nome"])))

    # Tipos de conhecimento da disciplina
    for tipo in disciplina.get("tiposDeConhecimento", []):
        tipo_nome = tipo.replace(" ", "_").replace("-", "_") + "_TipoDeConhecimento"
        uri_tipo = EX[tipo_nome]

        if (uri_tipo, RDF.type, EX.TipoDeConhecimento) not in g:
            g.add((uri_tipo, RDF.type, EX.TipoDeConhecimento))
            g.add((uri_tipo, EX.nome, Literal(tipo)))

        # Relaciona disciplina ao tipo de conhecimento
        g.add((uri_disciplina, EX.pertenceA, uri_tipo))

    # Conceitos da disciplina
    for conceito in disciplina.get("conceitos", []):
        nomeconceito = conceito.replace(" ", "_").replace("-", "_").replace("/", "_")
        conceito_nome = nomeconceito + "_Conceito"
        uri_conceito = EX[conceito_nome]
        # Instancia Conceito se ainda não existir
        if (uri_conceito, RDF.type, EX.Conceito) not in g:
            g.add((uri_conceito, RDF.type, EX.Conceito))
            g.add((uri_conceito, EX.nome, Literal(conceito)))

        # Relaciona conceito à disciplina que o estuda
        g.add((uri_conceito, EX.éEstudadoEm, uri_disciplina))

# Salva grafo atualizado
g.serialize("sapientia_povoada_disciplinas.ttl", format="turtle")
