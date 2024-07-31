document.addEventListener('DOMContentLoaded', function () {
    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: [],
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'background-color': '#0074D9',
                    'color': '#000',  // Change text color to black
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': '60px',
                    'height': '60px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#0074D9',
                    'target-arrow-color': '#0074D9',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            }
        ],
        layout: {
            name: 'circle'
        }
    });

    function stripPrefix(uri) {
        const prefix = 'http://example.org/ontology#';
        if (uri.startsWith(prefix)) {
            return uri.slice(prefix.length);
        }
        return uri;
    }

    fetch('/api/ontology')
        .then(response => response.json())
        .then(data => {
            const elements = [];
            data.forEach(element => {
                if (element.data.id) {
                    element.data.label = stripPrefix(element.data.id);
                    element.group = 'nodes'; // Specify the group as nodes
                    elements.push(element);
                }
                if (element.data.source && element.data.target) {
                    element.group = 'edges'; // Specify the group as edges
                    elements.push(element);
                }
            });
            cy.add(elements);
            console.log("Elements added:", elements);
            cy.layout({ name: 'circle' }).run();
        })
        .catch(error => console.error('Error fetching data:', error));

    window.addNode = function () {
        const nodeId = document.getElementById('node-id').value;
        const strippedId = stripPrefix(nodeId);
        fetch('/api/ontology', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uri: nodeId })
        }).then(() => {
            cy.add({ data: { id: nodeId, label: strippedId } });
            cy.layout({ name: 'circle' }).run();
            console.log("Node added:", { id: nodeId, label: strippedId });
        }).catch(error => console.error('Error adding node:', error));
    };

    window.addEdge = function () {
        const sourceId = document.getElementById('source-id').value;
        const targetId = document.getElementById('target-id').value;
        const strippedSource = stripPrefix(sourceId);
        const strippedTarget = stripPrefix(targetId);

        // Check if both source and target nodes exist
        const sourceExists = cy.getElementById(sourceId).length > 0;
        const targetExists = cy.getElementById(targetId).length > 0;

        if (sourceExists && targetExists) {
            fetch('/api/ontology', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source: sourceId, target: targetId })
            }).then(() => {
                cy.add({ data: { source: strippedSource, target: strippedTarget } });
                cy.layout({ name: 'circle' }).run();
                console.log("Edge added:", { source: strippedSource, target: strippedTarget });
            }).catch(error => console.error('Error adding edge:', error));
        } else {
            console.error('Source or target node does not exist');
            alert('Source or target node does not exist. Please add the nodes first.');
        }
    };
});
