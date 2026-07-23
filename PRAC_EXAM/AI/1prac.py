
def dfs(graph,state,visited):
    if visited is None:
        visited=[]    
    visited.append(state)
    print(state,end='')
    
    for n in graph[state]:
        if n not in visited:
            dfs(graph,n,visited)
    
    return 


graph={}
visited=[]

n=int(input("Enter no of nodes:"))


for _ in range(n):
    node=input("Enter node:")
    neighbors=input("Enter neighbors:").split()
    graph[node]=neighbors

start=input("Enter start:")
dfs(graph,start,visited)    