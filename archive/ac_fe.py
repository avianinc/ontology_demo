from pyfuseki import FusekiQuery

# Variables for Fuseki server and ontology prefix
FUSEKI_SERVER = 'http://localhost:3030'
DATABASE = 'model'
ONTOLOGY_PREFIX = 'http://example.org/ontology#'

fuseki_query = FusekiQuery(FUSEKI_SERVER, DATABASE)

# Query: Retrieve aircraft with a fuel efficiency score above 5 and their corresponding mission success scores
decision_query = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?Aircraft ?FuelEfficiencyScore ?Mission ?MissionSuccessScore
WHERE {{
  ?Aircraft rdf:type ex:Aircraft .
  ?Aircraft ex:hasFuelEfficiency ?fe .
  ?fe ex:fuelEfficiencyScore ?FuelEfficiencyScore .
  FILTER (?FuelEfficiencyScore > 6)
  ?Aircraft ex:hasPayload ?Payload .
  ?Payload ex:impactsMissionSuccess ?ms .
  ?ms ex:missionSuccessScore ?MissionSuccessScore .
  ?Mission ex:hasMissionSuccess ?ms .
}}
"""

# Execute the query
decision_results = fuseki_query.run_sparql(decision_query).convert()

# Print the results
print("\nDecision Query Results (Aircraft with Fuel Efficiency > 5 and their corresponding mission success scores):")
for result in decision_results['results']['bindings']:
    print(f"Aircraft: {result['Aircraft']['value']}, Fuel Efficiency Score: {result['FuelEfficiencyScore']['value']}, Mission: {result['Mission']['value']}, Mission Success Score: {result['MissionSuccessScore']['value']}")
