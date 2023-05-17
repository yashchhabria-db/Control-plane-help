d3.json('d3_test_data.json').then(data => {
    // Data processing and visualization code goes here
    const nodes = data.nodes;
    const links = data.links;
  
    const width = 600;
    const height = 400;
  
    const svg = d3.select('#chart')
      .attr('width', width)
      .attr('height', height);
  
    const line = d3.line()
      .curve(d3.curveBundle.beta(0.85));
  
    // Generate path for each link
    links.forEach(link => {
      const sourceNode = nodes.find(node => node.id === link.source);
      const targetNode = nodes.find(node => node.id === link.target);
      link.path = [sourceNode, targetNode];
    });
  
    // Define open ports information
    const openPorts = {
      A: [80, 443],    // Example open ports for Node A
      B: [22, 8080],   // Example open ports for Node B
      C: [3306]        // Example open ports for Node C
    };
  
    // Function to check if a port is open for a node
    const isPortOpen = (nodeId, port) => openPorts[nodeId]?.includes(port);
  
    svg.selectAll('path')
      .data(links)
      .enter()
      .append('path')
      .attr('d', d => line(d.path.map(node => [node.x, node.y])))
      .style('fill', 'none')
      .style('stroke', 'steelblue')
      .style('opacity', 0.6)
      .attr('marker-end', 'url(#arrow)');
  
    svg.selectAll('line')
      .data(links.flatMap(link => {
        const sourceNode = link.path[0];
        const targetNode = link.path[1];
        const ports = openPorts[sourceNode.id] || [];
        return ports.map(port => ({ source: sourceNode, target: targetNode, port }));
      }))
      .enter()
      .append('line')
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
      .style('stroke', 'green')
      .style('stroke-width', 2);
  
    svg.selectAll('circle')
      .data(nodes)
      .enter()
      .append('circle')
      .attr('cx', width / 2)
      .attr('cy', height / 2)
      .attr('r', 20)
      .style('fill', d => isPortOpen(d.id, 80) ? 'green' : 'red') // Set color based on open port (80 in this example)
      .attr('transform', d => `translate(${d.x - width / 2},${d.y - height / 2})`);
  
    svg.selectAll('text')
      .data(nodes)
      .enter()
      .append('text')
      .attr('x', d => d.x)
      .attr('y', d => d.y)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .text(d => d.id)
      .style('fill', 'black');
  });