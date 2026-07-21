import math

def alphabeta(node, alpha, beta, tree, evals, depth=0):
    children = tree.get(node, [])
    
    if not children:
        return evals[node]
    
    is_max = depth % 2 == 0
    indent = "  " * depth
    
    if is_max:
        print(f"{indent}MAX {node}")
        for child in children:
            alpha = max(alpha, alphabeta(child, alpha, beta, tree, evals, depth+1))
            if alpha >= beta:
                print(f"{indent}  β-prune")
                return beta
        return alpha
    else:
        print(f"{indent}MIN {node}")
        for child in children:
            beta = min(beta, alphabeta(child, alpha, beta, tree, evals, depth+1))
            if alpha >= beta:
                print(f"{indent}  α-prune")
                return alpha
        return beta

print("Alpha-Beta Pruning\n")

tree = {}
evals = {}
root = None

while True:
    line = input("Node (done to finish): ").strip()
    if line.lower() == "done" or not line:
        break
    
    parts = line.split()
    node = parts[0]
    
    if root is None:
        root = node
    
    if len(parts) > 1:
        tree[node] = parts[1].split(",")
    else:
        tree[node] = []
        val = int(input(f"  Value of {node}: "))
        evals[node] = val

print()
result = alphabeta(root, -math.inf, math.inf, tree, evals)
print(f"\nResult: {result}")
