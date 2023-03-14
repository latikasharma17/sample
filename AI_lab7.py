def __init__(self, is_goal, children):
        self.is_goal = is_goal
        self.children = children

def BT(n):
    if n.children is None or len(n.children) == 0:
        return n.is_goal
    else:
        for c in n.children:
            if BT(c):
                return True
        return False

print("hello")

variables = ['X', 'Y', 'Z']
domains = {
    'X': [1, 2, 3],
    'Y': [1, 2, 3],
    'Z': [1, 2, 3]
}

# Define the constraints as a list of tuples
constraints = [
    ('X', 'Y', lambda x, y: x != y),
    ('Y', 'Z', lambda y, z: y != z),
    ('X', 'Z', lambda x, z: x < z)
]

# Define a function to create the constraint graph
def create_constraint_graph(variables, constraints):
    # Initialize an empty dictionary to store the graph
    graph = {}
    
    # Add each variable as a node to the graph
    for variable in variables:
        graph[variable] = set()
    
    # Add the constraints as edges to the graph
    for (var1, var2, constraint) in constraints:
        graph[var1].add((var2, constraint))
        graph[var2].add((var1, constraint))
    
    return graph

# Create the constraint graph
constraint_graph = create_constraint_graph(variables, constraints)

# Define a function for backtracking with constraint propagation
def BT(node):
    global domains, constraint_graph, num_nodes_visited
    num_nodes_visited += 1
    
    # If node is a leaf node, check if it is a goal node
    if node in domains and len(domains[node]) == 1:
        if domains[node][0] == 1:  # Goal node condition
            return True
        else:
            return False
    
    # Apply constraint propagation to all adjacent nodes if node is fixed
    if node not in domains:
        for neighbor, constraint in constraint_graph[node]:
            if neighbor in domains:
                old_domain = domains[neighbor]
                new_domain = []
                for value in old_domain:
                    if any(constraint(value, v) for v in domains[node]):
                        new_domain.append(value)
                domains[neighbor] = new_domain
                if len(new_domain) == 0:
                    return False
    
    # Iterate over the domain of the current node and recurse
    if node in domains:
        for value in domains[node]:
            domains_copy = domains.copy()
            domains_copy[node] = [value]
            success = True
            for neighbor, constraint in constraint_graph[node]:
                if neighbor not in domains_copy:
                    continue
                old_domain = domains_copy[neighbor]
                new_domain = []
                for v in old_domain:
                    if any(constraint(value, v) for value in domains_copy[node]):
                        new_domain.append(v)
                domains_copy[neighbor] = new_domain
                if len(new_domain) == 0:
                    success = False
                    break
            if success and BT(next_node()):
                domains = domains_copy
                return True
    
    return False

# Define a function to get the next node for backtracking
def next_node():
    # Use the minimum remaining values (MRV) heuristic to choose the next node
    node = None
    min_remaining_values = float('inf')
    for variable in variables:
        if variable not in domains:
            remaining_values = len(set.union()*(constraint_graph[variable] - set([(n, c) for n, c in domains.items() if n in constraint_graph[variable]]) for variable, domain in domains.items()))
            if remaining_values < min_remaining_values:
                node = variable
                min_remaining_values = remaining_values
