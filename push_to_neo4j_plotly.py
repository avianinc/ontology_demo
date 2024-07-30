import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph as rdflibGraph, URIRef, Literal, RDF
from py2neo import Graph, Node, Relationship
from pyvis.network import Network
import networkx as nx

# Configure logging
logging.basicConfig(level=logging.INFO)

# Variables for Fuseki server and ontology prefix
FUSEKI_SERVER = 'http://localhost:3030'
DATABASE = 'model'
ONTOLOGY_PREFIX = 'http://example.org/ontology#'
NEO4J_SERVER = 'bolt://localhost:7687'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = 'testpassword'

# Query Fuseki server to retrieve the ontology data
sparql = SPARQLWrapper(f"{FUSEKI_SERVER}/{DATABASE}/sparql")
sparql.setQuery("""
    SELECT ?s ?p ?o
    WHERE { ?s ?p ?o }
    LIMIT 100
""")
sparql.setReturnFormat(JSON)

try:
    results = sparql.query().convert()
    logging.info("Retrieved ontology data from Fuseki")
except Exception as e:
    logging.error("Error querying Fuseki server: %s", e)
    exit(1)

# Print the results for verification
print("Sample data from Fuseki:")
for result in results["results"]["bindings"]:
    print(result)

# Save the retrieved data as an OWL file
owl_file_path = "ontology_export.owl"
try:
    owl_model = rdflibGraph()
    for result in results["results"]["bindings"]:
        subj = URIRef(result["s"]["value"])
        pred = URIRef(result["p"]["value"])
        obj_value = result["o"]["value"]
        
        # Check if the object is a URI or a literal
        if result["o"]["type"] == "uri":
            obj = URIRef(obj_value)
        else:
            obj = Literal(obj_value)
        
        owl_model.add((subj, pred, obj))
    owl_model.serialize(destination=owl_file_path, format='application/rdf+xml')
    logging.info("Ontology data saved to %s", owl_file_path)
except Exception as e:
    logging.error("Error saving OWL file: %s", e)
    exit(1)

# Load the OWL model using rdflib
try:
    owl_model.parse(owl_file_path, format='application/rdf+xml')
    logging.info("OWL model loaded successfully")
except Exception as e:
    logging.error("Error loading OWL model: %s", e)
    exit(1)

# Connect to Neo4j
try:
    graph = Graph(NEO4J_SERVER, auth=(NEO4J_USER, NEO4J_PASSWORD))
    logging.info("Connected to Neo4j server")
except Exception as e:
    logging.error("Error connecting to Neo4j: %s", e)
    exit(1)

# Clear existing data in Neo4j
try:
    graph.run("MATCH (n) DETACH DELETE n")
    logging.info("Cleared existing data in Neo4j")
except Exception as e:
    logging.error("Error clearing data in Neo4j: %s", e)
    exit(1)

# Add nodes and relationships to Neo4j
for subj, pred, obj in owl_model:
    subj_str = str(subj)
    pred_str = str(pred)
    obj_str = str(obj)

    if isinstance(obj, URIRef):
        # Add nodes and relationships
        subj_node = Node("Entity", uri=subj_str)
        obj_node = Node("Entity", uri=obj_str)
        relationship = Relationship(subj_node, pred_str, obj_node)
        graph.merge(subj_node, 'Entity', 'uri')
        graph.merge(obj_node, 'Entity', 'uri')
        graph.merge(relationship)
    elif isinstance(obj, Literal):
        # Add nodes and properties
        subj_node = Node("Entity", uri=subj_str)
        graph.merge(subj_node, 'Entity', 'uri')
        graph.run("MATCH (a:Entity {uri: $subj_str}) SET a += {pred_str: $obj_str}",
                  subj_str=subj_str, pred_str=pred_str, obj_str=obj_str)

# Query Neo4j to retrieve the graph
query = """
MATCH (n)-[r]->(m)
RETURN n.uri AS source, type(r) AS relationship, m.uri AS target
"""
results = graph.run(query)

# Create a Pyvis Network graph
net = Network(height="750px", width="100%", notebook=True)

# Add nodes and edges to the network
for record in results:
    net.add_node(record['source'], label=record['source'])
    net.add_node(record['target'], label=record['target'])
    net.add_edge(record['source'], record['target'], title=record['relationship'])

# Generate and display the network
net.show("ontology_network.html")
