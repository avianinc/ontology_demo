from flask import Flask, request, jsonify, send_from_directory
from neo4j import GraphDatabase
import os

app = Flask(__name__, static_folder='frontend')

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testpassword"))

@app.route('/api/ontology', methods=['GET'])
def get_ontology():
    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
        data = []
        for record in result:
            data.append({'data': {'id': record['n']['uri']}, 'group': 'nodes'})
            data.append({'data': {'id': record['m']['uri']}, 'group': 'nodes'})
            data.append({'data': {'source': record['r'].start_node['uri'], 'target': record['r'].end_node['uri']}, 'group': 'edges'})
        return jsonify(data)

@app.route('/api/ontology', methods=['POST'])
def add_node():
    data = request.json
    with driver.session() as session:
        if 'source' in data and 'target' in data:
            session.run("""
                MATCH (a:Entity {uri: $source}), (b:Entity {uri: $target})
                CREATE (a)-[:RELATED]->(b)
            """, source=data['source'], target=data['target'])
        else:
            session.run("CREATE (n:Entity {uri: $uri})", uri=data['uri'])
    return jsonify({"status": "Success"}), 201

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
