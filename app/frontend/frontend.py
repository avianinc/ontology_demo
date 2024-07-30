import dash
from dash import html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testpassword"))

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'circle'},
        style={'width': '100%', 'height': '400px'},
        elements=[]
    ),
    html.Button('Add Node', id='add-node-btn', n_clicks=0),
    html.Button('Add Edge', id='add-edge-btn', n_clicks=0),
    dcc.Input(id='node-id', type='text', placeholder='Node ID'),
    dcc.Input(id='source-id', type='text', placeholder='Source ID'),
    dcc.Input(id='target-id', type='text', placeholder='Target ID')
])

# Function to fetch elements from Neo4j
def fetch_elements():
    elements = []
    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
        for record in result:
            elements.append({
                'data': {'id': record['n']['uri'], 'label': record['n']['uri']}
            })
            elements.append({
                'data': {'id': record['m']['uri'], 'label': record['m']['uri']}
            })
            elements.append({
                'data': {'source': record['r'].start_node['uri'], 'target': record['r'].end_node['uri']}
            })
    return elements

# Callback to update Cytoscape graph
@app.callback(
    Output('cytoscape', 'elements'),
    Input('add-node-btn', 'n_clicks'),
    Input('add-edge-btn', 'n_clicks'),
    State('node-id', 'value'),
    State('source-id', 'value'),
    State('target-id', 'value')
)
def update_graph(n_clicks_node, n_clicks_edge, node_id, source_id, target_id):
    if n_clicks_node > 0 and node_id:
        with driver.session() as session:
            session.run("CREATE (n:Entity {uri: $uri})", uri=node_id)
    if n_clicks_edge > 0 and source_id and target_id:
        with driver.session() as session:
            session.run("""
                MATCH (a:Entity {uri: $source}), (b:Entity {uri: $target})
                CREATE (a)-[:RELATED]->(b)
            """, source=source_id, target=target_id)
    return fetch_elements()

if __name__ == '__main__':
    app.run_server(debug=True)
