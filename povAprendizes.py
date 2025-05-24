import json
from rdflib import Graph, Namespace, Literal, RDF, XSD


g = Graph()
g.parse("sapientia_povoada_obras.ttl", format="turtle")


EX = Namespace("http://www.semanticweb.org/historiaas/")


with open("pg55980.json", "r", encoding="utf-8") as f:
    aprendizes = json.load(f)

for ap in aprendizes:
    nome_aprendiz = ap["nome"].replace(" ", "_")
    aprendiz_uri = EX[nome_aprendiz + "_Aprendiz"]

    g.add((aprendiz_uri, RDF.type, EX.Aprendiz))
    g.add((aprendiz_uri, EX.nome, Literal(ap["nome"])))
    g.add((aprendiz_uri, EX.idade, Literal(ap["idade"])))

    for disciplina in ap.get("disciplinas", []):
        nome_disciplina = disciplina.replace(" ", "_")
        disciplina_uri = EX[nome_disciplina + "_Disciplina"]

        # Garante que a disciplina existe
        if (disciplina_uri, RDF.type, EX.Disciplina) not in g:
            print(f"Adicionando disciplina: {disciplina}")
            g.add((disciplina_uri, RDF.type, EX.Disciplina))
            g.add((disciplina_uri, EX.nome, Literal(disciplina)))

        g.add((aprendiz_uri, EX.aprende, disciplina_uri))

# Salva o grafo atualizado
g.serialize("sapientia_ind.ttl", format="turtle")
