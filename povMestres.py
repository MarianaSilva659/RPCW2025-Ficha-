import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF


g = Graph()
g.parse("sapientia_povoada_disciplinas.ttl", format="turtle")


EX = Namespace("http://www.semanticweb.org/historiaas/")


with open("mestres.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

for mestre in dados["mestres"]:
    nome_mestre = mestre["nome"]
    uri_mestre = EX[nome_mestre.replace(" ", "_").replace("-", "_") + "_Mestre"]

    g.add((uri_mestre, RDF.type, EX.Mestre))
    g.add((uri_mestre, EX.nome, Literal(nome_mestre)))

    # Período histórico
    if "períodoHistórico" in mestre:
        nome_periodo = mestre["períodoHistórico"]
        uri_periodo = EX[nome_periodo.replace(" ", "_").replace("-", "_").replace("/", "_") + "_PeríodoHistorico"]

        if (uri_periodo, RDF.type, EX.PeríodoHistorico) not in g:
            g.add((uri_periodo, RDF.type, EX.PeríodoHistorico))
            g.add((uri_periodo, EX.nome, Literal(nome_periodo)))
        g.add((uri_mestre, EX.mestreDE, uri_periodo))

    # Disciplinas que ele ensina
    for disciplina in mestre.get("disciplinas", []):
        uri_disciplina = EX[disciplina.replace(" ", "_").replace("-", "_") + "_Disciplina"]
        if (uri_disciplina, RDF.type, EX.Disciplina) not in g:
            g.add((uri_disciplina, RDF.type, EX.Disciplina))
            g.add((uri_disciplina, EX.nome, Literal(disciplina)))
        g.add((uri_mestre, EX.ensina, uri_disciplina))

# Salva grafo atualizado
g.serialize("sapientia_povoada_mestres.ttl", format="turtle")
