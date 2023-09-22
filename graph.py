import networkx as nx
import matplotlib.pyplot as plt
import sys

def draw_graph(graph):
    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Add edges from the dictionary to the graph
    for start_node, end_nodes in graph.items():
        for end_node in end_nodes:
            G.add_edge(start_node, end_node)

    # Counter to ensure unique filenames for each component
    component_counter = 1

    # For each weakly connected component, extract subgraph and plot it
    for component in nx.weakly_connected_components(G):
        subG = G.subgraph(component)
        pos = nx.kamada_kawai_layout(subG, scale=100)
        plt.figure(figsize=(12, 12))
        nx.draw(subG, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=8, width=2.0, alpha=0.6)
        plt.title('Directed Graph Visualization of Component')
        
        # Save the figure to an image file
        file_name = f"component_{component_counter}.png"
        plt.savefig(file_name)
        print(f"Saved component to {file_name}")
        
        # Increment the counter
        component_counter += 1

        # Close the plot to release memory
        plt.close()

def read_graph_from_file(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if "===" in line:
                break
            start_node, end_node = line.strip().split(" -> ")
            # If the start node is not in the graph, add it with an empty set
            if start_node not in graph:
                graph[start_node] = set()
            # Add the end node to the start node's set
            graph[start_node].add(end_node)
    return graph

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py file_name")
        sys.exit(1)
    
    file_name = sys.argv[1]
    graph = read_graph_from_file(file_name)
    draw_graph(graph)
