import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF

# Função única para formatar nomes de URIs
def formatar_uri(nome, sufixo):
    nome_formatado = nome.replace(" ", "_").replace("-", "_").replace("/", "_")
    return EX[nome_formatado + f"_{sufixo}"]

# Carrega o grafo da ontologia
g = Graph()
g.parse("sapientia_base.ttl", format="turtle")

EX = Namespace("http://www.semanticweb.org/historiaas/")

with open("conceitos.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

for conceito in dados["conceitos"]:
    conceito_uri = formatar_uri(conceito["nome"], "Conceito")
    g.add((conceito_uri, RDF.type, EX.Conceito))
    g.add((conceito_uri, EX.nome, Literal(conceito["nome"])))

    for aplicacao in conceito.get("aplicações", []):
        aplicacao_uri = formatar_uri(aplicacao, "Aplicacao")
        if (aplicacao_uri, RDF.type, EX.Aplicação) not in g:
            g.add((aplicacao_uri, RDF.type, EX.Aplicação))
            g.add((aplicacao_uri, EX.nome, Literal(aplicacao)))
        g.add((conceito_uri, EX.temAplicaçãoEm, aplicacao_uri))

    if "períodoHistórico" in conceito:
        periodo_uri = formatar_uri(conceito["períodoHistórico"], "PeríodoHistorico")
        if (periodo_uri, RDF.type, EX.PeríodoHistorico) not in g:
            g.add((periodo_uri, RDF.type, EX.PeríodoHistorico))
            g.add((periodo_uri, EX.nome, Literal(conceito["períodoHistórico"])))
        g.add((conceito_uri, EX.surgeEm, periodo_uri))

    for relacionado in conceito.get("conceitosRelacionados", []):
        conceito_relacionado_uri = formatar_uri(relacionado, "Conceito")
        if (conceito_relacionado_uri, RDF.type, EX.Conceito) not in g:
            g.add((conceito_relacionado_uri, RDF.type, EX.Conceito))
            g.add((conceito_relacionado_uri, EX.nome, Literal(relacionado)))
        g.add((conceito_uri, EX.estáRelacionadoCom, conceito_relacionado_uri))

# Salva o grafo
g.serialize("sapientia_povoada_conceitos.ttl", format="ttl")
