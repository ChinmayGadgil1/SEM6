graph={}
heuristics={}

Nil=None

def h(node):
    return heuristics.get(node,99)

def reconstructPath(curr,closed_list):
    node=curr[0]
    parent=curr[1]
    path=[node]
    while parent:
        path.insert(0,parent)
        node=next((item for item in closed_list if item[0]==parent),Nil)
        parent=node[1] if node else Nil
    
    return path


def bestfs(start,goal,isAscending):
    open_list=[(start,Nil,h(start))]
    closed_list=[]
    
    while open_list:
        curr=open_list[0]
        node=curr[0]
        
        if node==goal:
            return reconstructPath(curr,closed_list)

        closed_list.insert(0,curr)
        children=graph.get(node,[])
        
        seen={c[0] for c in open_list} | {c[0] for c in closed_list}
        new_children=[c for c in children if c not in seen]
        new_nodes=[(c,node,h(c)) for c in new_children]
        open_list=new_nodes + open_list[1:]
        open_list.sort(key=lambda x:x[2],reverse=isAscending)


    return None

n=int(input("Enter no of nodes"))

for _ in range(n):
    node=input("Enter node:")
    heu=int(input("Enter h val:"))
    children=input("Enter children:").strip().split()
    
    graph[node]=children
    heuristics[node]=heu

start=input("enter start:")
goal=input("enter goal:")

if h(start)>h(goal):
    isAscending=False
else:
    isAscending=True

path=bestfs(start,goal,isAscending)

if path is None:
    print("No path found")
else:
    for node in path:
        print(node,end=' ')
    print()

        











