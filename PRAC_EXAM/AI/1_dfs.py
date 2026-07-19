
def dfs(graph,u,visited=None):
    if visited is None:
        visited=[]
    print(u)
    visited.append(u)
    for v in graph[u]:
        if v not in visited:
            dfs(graph,v,visited)




graph={}
n=int(input("Enter no of nodes:"))
for i in range(n):
    v=input("Enter vertex:")
    l=input("Enter neighbors:").split()
    graph[v]=l

start = input("\nEnter the starting vertex: ")

dfs(graph,start)    

