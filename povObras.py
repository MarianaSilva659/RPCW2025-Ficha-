import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF


g = Graph()
g.parse("sapientia_povoada_mestres.ttl", format="turtle")

EX = Namespace("http://www.semanticweb.org/historiaas/")

with open("obras.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

for obra in dados["obras"]:
    # Cria URI da obra
    titulo_formatado = obra["titulo"].replace(" ", "_").replace("-", "_")
    obra_uri = EX[titulo_formatado + "_Obra"]
    g.add((obra_uri, RDF.type, EX.Obra))
    g.add((obra_uri, EX.titulo, Literal(obra["titulo"])))

    # Cria URI do autor (Mestre)
    autor_formatado = obra["autor"].replace(" ", "_")
    autor_uri = EX[autor_formatado + "_Mestre"]
    if (autor_uri, RDF.type, EX.Mestre) not in g:
        print(f"Adicionando autor: {obra['autor']}")
        g.add((autor_uri, RDF.type, EX.Mestre))
        g.add((autor_uri, EX.nome, Literal(obra["autor"])))

    g.add((obra_uri, EX.foiEscritoPor, autor_uri))

    # Adiciona os conceitos explicados na obra
    for conceito in obra.get("conceitos", []):
        conceito_formatado = conceito.replace(" ", "_").replace("-", "_").replace("/", "_")
        conceito_uri = EX[conceito_formatado + "_Conceito"]
        if (conceito_uri, RDF.type, EX.Conceito) not in g:
            print(f"Adicionando conceito: {conceito}")
            g.add((conceito_uri, RDF.type, EX.Conceito))
            g.add((conceito_uri, EX.nome, Literal(conceito)))
        g.add((obra_uri, EX.explica, conceito_uri))

# Salva o grafo povoado
g.serialize("sapientia_povoada_obras.ttl", format="turtle")
