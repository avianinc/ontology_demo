from pyfuseki import FusekiUpdate, FusekiQuery

# Variables for Fuseki server and ontology prefix
FUSEKI_SERVER = 'http://localhost:3030'
DATABASE = 'model'
ONTOLOGY_PREFIX = 'http://example.org/ontology#'

# Variables for update and queries
new_fuel_efficiency_score = 7.756
fuel_efficiency_threshold = 5
aircraft_id = "Aircraft2"

# Connect to Fuseki
fuseki_update = FusekiUpdate(FUSEKI_SERVER, DATABASE)
fuseki_query = FusekiQuery(FUSEKI_SERVER, DATABASE)

# Update query to change the fuel efficiency score of Aircraft
update_query = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
DELETE {{
  ?fe ex:fuelEfficiencyScore ?oldScore .
}}
INSERT {{
  ?fe ex:fuelEfficiencyScore {new_fuel_efficiency_score} .
}}
WHERE {{
  ?aircraft ex:hasFuelEfficiency ?fe .
  ?fe ex:fuelEfficiencyScore ?oldScore .
  ?aircraft rdf:type ex:Aircraft .
  ?aircraft rdfs:label "{aircraft_id}" .
}}
"""

# Execute the update query
fuseki_update.run_sparql(update_query)
print("Fuel efficiency score updated for Aircraft1.")

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

# Execute the queries
results_1 = fuseki_query.run_sparql(query_1).convert()

# Print the results with explanations
print("Query 1 Results (Retrieve aircraft and their fuel efficiency scores):")
for result in results_1['results']['bindings']:
    print(f"Aircraft: {result['Aircraft']['value']}, Fuel Efficiency Score: {result['FuelEfficiencyScore']['value']}")

# Decision-making query: Retrieve aircraft with a fuel efficiency score above the threshold and their corresponding mission success scores
decision_query = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?Aircraft ?FuelEfficiencyScore ?Mission ?MissionSuccessScore
WHERE {{
  ?Aircraft rdf:type ex:Aircraft .
  ?Aircraft ex:hasFuelEfficiency ?fe .
  ?fe ex:fuelEfficiencyScore ?FuelEfficiencyScore .
  FILTER (?FuelEfficiencyScore > {fuel_efficiency_threshold})
  ?Aircraft ex:hasPayload ?Payload .
  ?Payload ex:impactsMissionSuccess ?ms .
  ?ms ex:missionSuccessScore ?MissionSuccessScore .
  ?Mission ex:hasMissionSuccess ?ms .
}}
"""

# Execute the decision-making query
decision_results = fuseki_query.run_sparql(decision_query).convert()

# Print the decision-making query results
print("\nDecision Query Results (Aircraft with Fuel Efficiency > {fuel_efficiency_threshold} and their corresponding mission success scores):")
for result in decision_results['results']['bindings']:
    print(f"Aircraft: {result['Aircraft']['value']}, Fuel Efficiency Score: {result['FuelEfficiencyScore']['value']}, Mission: {result['Mission']['value']}, Mission Success Score: {result['MissionSuccessScore']['value']}")

# Optimal payload configuration query: Retrieve payload configuration with the highest mission success score
optimal_payload_query = f"""
PREFIX ex: <{ONTOLOGY_PREFIX}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?Payload ?MissionSuccessScore
WHERE {{
  ?Payload rdf:type ex:Payload .
  ?Payload ex:impactsMissionSuccess ?ms .
  ?ms ex:missionSuccessScore ?MissionSuccessScore .
}}
ORDER BY DESC(?MissionSuccessScore)
LIMIT 1
"""

# Execute the optimal payload configuration query
optimal_payload_results = fuseki_query.run_sparql(optimal_payload_query).convert()

# Print the optimal payload configuration query results
print("\nOptimal Payload Configuration Results (Payload with the highest mission success score):")
for result in optimal_payload_results['results']['bindings']:
    print(f"Payload: {result['Payload']['value']}, Mission Success Score: {result['MissionSuccessScore']['value']}")
