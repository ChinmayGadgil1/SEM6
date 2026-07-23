
def h(node):
    return heuristic.get(node,999)

def bestfs(start,goal,graph):
    open_list=[(start,None,h(start))]
    closed_list=[]
    
    parent={}
    parent[start]=None
    visited=[]
    visited.append(start)
    while open_list:
        tuple=open_list[0]
        node=tuple[0]
        if node==goal:
            print(node)
            p=parent[node]
            while p is not None:
                print(p)
                p=parent[p]
            return
        open_list=open_list[1:]
        closed_list.insert(0,tuple)
        for new_node in graph[node]:
            if new_node not in visited:
                visited.append(new_node)
                open_list.append((new_node,node,h(new_node)))
                parent[new_node]=node
                open_list.sort(key=lambda x:x[2])
                
                
                
graph={}
heuristic={}

n = int(input("Enter the number of nodes: "))



for _ in range(n):
    name = input("\nNode: ").strip()
    val = int(input("Heuristic: "))
    children = input("Neighbors (space-separated): ").strip()
    heuristic[name] = val
    graph[name] = children

start = input("\nEnter start node: ").strip()
goal = input("Enter goal node: ").strip()

if heuristic.get(start, 99) < heuristic.get(goal, 99):
    isAscending = True

bestfs(start,goal,graph)