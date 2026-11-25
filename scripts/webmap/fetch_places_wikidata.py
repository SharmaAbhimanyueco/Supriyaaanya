import sys, json, requests
q = """
SELECT ?item ?itemLabel ?coord ?typeLabel WHERE {
  SERVICE wikibase:box {
    ?item wdt:P625 ?coord .
    bd:serviceParam wikibase:cornerSouthWest "Point(76.48 30.35)"^^geo:wktLiteral .
    bd:serviceParam wikibase:cornerNorthEast "Point(76.95 30.96)"^^geo:wktLiteral .
  }
  ?item wdt:P31 ?type .
  ?type wdt:P279* wd:Q486972 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""
r = requests.get("https://query.wikidata.org/sparql", params={"query": q, "format": "json"}, timeout=90,
                 headers={"User-Agent": "student-lulc-webmap/1.0 (educational project)", "Accept": "application/sparql-results+json"})
print("status", r.status_code)
r.raise_for_status()
rows = r.json()["results"]["bindings"]
json.dump(rows, open(sys.argv[1], "w"))
print("rows", len(rows))
