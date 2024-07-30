document.addEventListener('DOMContentLoaded', function () {
    var cy = cytoscape({
        container: document.getElementById('cy'),
        elements: [],
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(id)',
                    'background-color': '#0074D9'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#0074D9',
                    'target-arrow-color': '#0074D9',
                    'target-arrow-shape': 'triangle'
                }
            }
        ],
        layout: {
            name: 'circle'
        }
    });

    fetch('/api/ontology')
        .then(response => response.json())
        .then(data => {
            cy.add(data);
            cy.layout({ name: 'circle' }).run();
        });

    window.addNode = function () {
        const nodeId = document.getElementById('node-id').value;
        fetch('/api/ontology', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ uri: nodeId })
        }).then(() => {
            cy.add({ data: { id: nodeId } });
            cy.layout({ name: 'circle' }).run();
        });
    };

    window.addEdge = function () {
        const sourceId = document.getElementById('source-id').value;
        const targetId = document.getElementById('target-id').value;
        fetch('/api/ontology', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source: sourceId, target: targetId })
        }).then(() => {
            cy.add({ data: { source: sourceId, target: targetId } });
            cy.layout({ name: 'circle' }).run();
        });
    };
});
