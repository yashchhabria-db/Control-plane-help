// // Example data for one node
// const nodeData = {
//     "access-control-78c6d875b8-rk98n": {
//       "pod_ip": "10.2.236.15",
//       "node_ip": "10.20.9.44",
//       "listening_ports": ["5678", "7777"],
//       "outgoing_ports": ["47246", "53488"],
//       "pid": [["7", "com.databricks.accesscontrol.AccessControlService"]],
//       "incomming_connections": [
//         [
//           "10.2.236.15:7777",
//           ["10.20.9.44:56510", "same_node"],
//           "TIME_WAIT",
//           "-"
//         ],
//         [
//           "10.2.236.15:7777",
//           ["10.20.9.44:41742", "same_node"],
//           "TIME_WAIT",
//           "-"
//         ]
//       ],
//       "incomming_connected_service_names": [],
//       "incomming_connected_pod_names": [],
//       "outgoing_connections": [
//         [
//           "10.2.236.15:47246",
//           ["10.3.58.124:3306", "test-shard-local-database-service"],
//           "ESTABLISHED",
//           "7/java"
//         ],
//         [
//           "10.2.236.15:53488",
//           ["10.3.58.124:3306", "test-shard-local-database-service"],
//           "ESTABLISHED",
//           "7/java"
//         ]
//       ],
//       "outgoing_connected_service_names": ["test-shard-local-database-service"],
//       "outgoing_connected_pod_names": []
//     }
//   };

d3.json('../control_plane_paper/json_pod_parsed.json').then(nodeData => {
  
  // Extract the pod names and connections from the data
  const podNames = Object.keys(nodeData);
  const connections = nodeData[podNames[0]].incomming_connections;
  
  // Create an empty graph object
  const graph = {
    nodes: [],
    links: []
  };
  
  // Add nodes to the graph
  podNames.forEach(podName => {
    console.log(podName)
    graph.nodes.push({ id: podName });
  });
  
  // Add edges (links) to the graph
  connections.forEach(connection => {
    const sourcePod = connection[0].split(':')[0];
    const targetPod = connection[1][0].split(':')[0];
    console.log(sourcePod,targetPod)
    graph.links.push({ source: sourcePod, target: targetPod });
  });
  
  // Visualization code
  const width = 600;
  const height = 400;
  
  const svg = d3.select('#chart')
    .attr('width', width)
    .attr('height', height);
  
  const simulation = d3.forceSimulation(graph.nodes)
    .force('link', d3.forceLink(graph.links).id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2));
  
  const link = svg.selectAll('line')
    .data(graph.links)
    .enter()
    .append('line')
    .style('stroke', 'steelblue')
    .style('stroke-width', 2);
  
  const node = svg.selectAll('circle')
    .data(graph.nodes)
    .enter()
    .append('circle')
    .attr('r', 10)
    .style('fill', 'steelblue');
  
  node.append('title').text(d => d.id);
  
  simulation.on('tick', () => {
    link.attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);
  
    node.attr('cx', d => d.x)
      .attr('cy', d => d.y);
  });
  
});