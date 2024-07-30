from pyfuseki import FusekiUpdate, FusekiQuery
from pyfuseki.rdf import rdf_prefix, NameSpace as ns
from pyfuseki.rdf import NameSpace, rdf_property
from rdflib import URIRef, Graph, RDF, Literal, RDFS, OWL

# Variables for Fuseki server and ontology prefix
FUSEKI_SERVER = 'http://localhost:3030'
DATABASE = 'model'
ONTOLOGY_PREFIX = 'http://example.org/ontology#'

# Connect to Fuseki
fuseki_update = FusekiUpdate(FUSEKI_SERVER, DATABASE)
fuseki_query = FusekiQuery(FUSEKI_SERVER, DATABASE)

# Define the RDF prefix for our ontology
@rdf_prefix(ONTOLOGY_PREFIX)
class RdfPrefix():
    Aircraft: ns
    Payload: ns
    Mission: ns
    FuelEfficiency: ns
    MissionSuccess: ns

rp = RdfPrefix()

# Define object properties
@rdf_property(ONTOLOGY_PREFIX)
class ObjectProperty:
    hasPayload: URIRef
    impactsFuelEfficiency: URIRef
    impactsMissionSuccess: URIRef
    hasFuelEfficiency: URIRef
    hasMissionSuccess: URIRef

# Define data properties
@rdf_property(ONTOLOGY_PREFIX)
class DataProperty:
    missionSuccessScore: URIRef
    fuelEfficiencyScore: URIRef

# Define annotation properties
@rdf_property(ONTOLOGY_PREFIX)
class AnnotationProperty:
    comment: URIRef

op = ObjectProperty()
dp = DataProperty()
ap = AnnotationProperty()

# Example instances
aircraft1 = URIRef(f'{ONTOLOGY_PREFIX}Aircraft1')
payload1 = URIRef(f'{ONTOLOGY_PREFIX}Payload1')
fuel_efficiency1 = URIRef(f'{ONTOLOGY_PREFIX}FuelEfficiency1')
mission1 = URIRef(f'{ONTOLOGY_PREFIX}Mission1')
mission_success1 = URIRef(f'{ONTOLOGY_PREFIX}MissionSuccess1')

aircraft2 = URIRef(f'{ONTOLOGY_PREFIX}Aircraft2')
payload2 = URIRef(f'{ONTOLOGY_PREFIX}Payload2')
fuel_efficiency2 = URIRef(f'{ONTOLOGY_PREFIX}FuelEfficiency2')
mission2 = URIRef(f'{ONTOLOGY_PREFIX}Mission2')
mission_success2 = URIRef(f'{ONTOLOGY_PREFIX}MissionSuccess2')

# Build the graph
g = Graph()

# Define RDF types and labels
g.add((rp.Aircraft.to_uri(), RDF.type, OWL.Class))
g.add((aircraft1, RDF.type, rp.Aircraft.to_uri()))
g.add((aircraft1, RDFS.label, Literal('Aircraft1')))
g.add((aircraft1, RDFS.comment, Literal('This is an example of an aircraft instance.')))
g.add((rp.Payload.to_uri(), RDF.type, OWL.Class))
g.add((payload1, RDF.type, rp.Payload.to_uri()))
g.add((payload1, RDFS.label, Literal('Payload1')))
g.add((payload1, RDFS.comment, Literal('This is an example of a payload instance.')))
g.add((rp.FuelEfficiency.to_uri(), RDF.type, OWL.Class))
g.add((fuel_efficiency1, RDF.type, rp.FuelEfficiency.to_uri()))
g.add((fuel_efficiency1, RDFS.label, Literal('FuelEfficiency1')))
g.add((fuel_efficiency1, RDFS.comment, Literal('This is an example of a fuel efficiency instance.')))
g.add((rp.Mission.to_uri(), RDF.type, OWL.Class))
g.add((mission1, RDF.type, rp.Mission.to_uri()))
g.add((mission1, RDFS.label, Literal('Mission1')))
g.add((mission1, RDFS.comment, Literal('This is an example of a mission instance.')))
g.add((rp.MissionSuccess.to_uri(), RDF.type, OWL.Class))
g.add((mission_success1, RDF.type, rp.MissionSuccess.to_uri()))
g.add((mission_success1, RDFS.label, Literal('MissionSuccess1')))
g.add((mission_success1, RDFS.comment, Literal('This is an example of a mission success instance.')))

g.add((aircraft2, RDF.type, rp.Aircraft.to_uri()))
g.add((aircraft2, RDFS.label, Literal('Aircraft2')))
g.add((aircraft2, RDFS.comment, Literal('This is another example of an aircraft instance.')))
g.add((payload2, RDF.type, rp.Payload.to_uri()))
g.add((payload2, RDFS.label, Literal('Payload2')))
g.add((payload2, RDFS.comment, Literal('This is another example of a payload instance.')))
g.add((fuel_efficiency2, RDF.type, rp.FuelEfficiency.to_uri()))
g.add((fuel_efficiency2, RDFS.label, Literal('FuelEfficiency2')))
g.add((fuel_efficiency2, RDFS.comment, Literal('This is another example of a fuel efficiency instance.')))
g.add((mission2, RDF.type, rp.Mission.to_uri()))
g.add((mission2, RDFS.label, Literal('Mission2')))
g.add((mission2, RDFS.comment, Literal('This is another example of a mission instance.')))
g.add((mission_success2, RDF.type, rp.MissionSuccess.to_uri()))
g.add((mission_success2, RDFS.label, Literal('MissionSuccess2')))
g.add((mission_success2, RDFS.comment, Literal('This is another example of a mission success instance.')))

# Define relationships and properties
g.add((aircraft1, op.hasPayload, payload1))
g.add((aircraft1, op.hasFuelEfficiency, fuel_efficiency1))
g.add((payload1, op.impactsFuelEfficiency, fuel_efficiency1))
g.add((payload1, op.impactsMissionSuccess, mission_success1))
g.add((mission1, op.hasMissionSuccess, mission_success1))
g.add((fuel_efficiency1, dp.fuelEfficiencyScore, Literal(9)))
g.add((mission_success1, dp.missionSuccessScore, Literal(8)))

g.add((aircraft2, op.hasPayload, payload2))
g.add((aircraft2, op.hasFuelEfficiency, fuel_efficiency2))
g.add((payload2, op.impactsFuelEfficiency, fuel_efficiency2))
g.add((payload2, op.impactsMissionSuccess, mission_success2))
g.add((mission2, op.hasMissionSuccess, mission_success2))
g.add((fuel_efficiency2, dp.fuelEfficiencyScore, Literal(6)))
g.add((mission_success2, dp.missionSuccessScore, Literal(5)))

# Insert the graph into Fuseki
fuseki_update.insert_graph(g)

print("Ontology model has been uploaded to Fuseki.")

# Perform SPARQL queries

# Query 1: Retrieve aircraft and their fuel efficiency scores
query_1 = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?Aircraft ?FuelEfficiencyScore
WHERE {{
  ?Aircraft rdf:type ex:Aircraft .
  ?Aircraft ex:hasFuelEfficiency ?fe .
  ?fe ex:fuelEfficiencyScore ?FuelEfficiencyScore .
}}
"""

# Query 2: Retrieve payload configurations and their impact on mission success scores
query_2 = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?Payload ?MissionSuccessScore
WHERE {{
  ?Payload rdf:type ex:Payload .
  ?Payload ex:impactsMissionSuccess ?ms .
  ?ms ex:missionSuccessScore ?MissionSuccessScore .
}}
"""

# Query 3: Retrieve payloads and their impact on fuel efficiency scores
query_3 = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?Payload ?FuelEfficiencyScore
WHERE {{
  ?Payload rdf:type ex:Payload .
  ?Payload ex:impactsFuelEfficiency ?fe .
  ?fe ex:fuelEfficiencyScore ?FuelEfficiencyScore .
}}
"""

# Query 4: Retrieve aircraft and their corresponding payloads
query_4 = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?Aircraft ?Payload
WHERE {{
  ?Aircraft rdf:type ex:Aircraft .
  ?Aircraft ex:hasPayload ?Payload .
}}
"""

# Query 5: Retrieve missions and their success scores along with the mission names
query_5 = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?Mission ?MissionName ?MissionSuccessScore
WHERE {{
  ?Mission rdf:type ex:Mission .
  ?Mission ex:hasMissionSuccess ?ms .
  ?ms ex:missionSuccessScore ?MissionSuccessScore .
  ?Mission rdfs:label ?MissionName .
}}
"""

# Execute the queries
results_1 = fuseki_query.run_sparql(query_1).convert()
results_2 = fuseki_query.run_sparql(query_2).convert()
results_3 = fuseki_query.run_sparql(query_3).convert()
results_4 = fuseki_query.run_sparql(query_4).convert()
results_5 = fuseki_query.run_sparql(query_5).convert()

# Print the results with explanations
print("Query 1 Results (Retrieve aircraft and their fuel efficiency scores):")
for result in results_1['results']['bindings']:
    print(f"Aircraft: {result['Aircraft']['value']}, Fuel Efficiency Score: {result['FuelEfficiencyScore']['value']}")

print("\nQuery 2 Results (Retrieve payload configurations and their impact on mission success scores):")
for result in results_2['results']['bindings']:
    print(f"Payload: {result['Payload']['value']}, Mission Success Score: {result['MissionSuccessScore']['value']}")

print("\nQuery 3 Results (Retrieve payloads and their impact on fuel efficiency scores):")
for result in results_3['results']['bindings']:
    print(f"Payload: {result['Payload']['value']}, Fuel Efficiency Score: {result['FuelEfficiencyScore']['value']}")

print("\nQuery 4 Results (Retrieve aircraft and their corresponding payloads):")
for result in results_4['results']['bindings']:
    print(f"Aircraft: {result['Aircraft']['value']}, Payload: {result['Payload']['value']}")

print("\nQuery 5 Results (Retrieve missions and their success scores along with the mission names):")
for result in results_5['results']['bindings']:
    print(f"Mission: {result['Mission']['value']}, Mission Name: {result['MissionName']['value']}, Mission Success Score: {result['MissionSuccessScore']['value']}")
