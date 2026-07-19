from collections import deque

def bfs(graph,start):
    visited=[]
    queue=deque()
    
    queue.append(start)
    visited.append(start)
    
    while queue:
        u=queue.popleft()
        print(u,end=" ")
        for v in graph[u]:
            if v not in visited:
                visited.append(v)
                queue.append(v)
    

n=int(input("Enter no of nodes:"))
graph={}

for i in range(n):
    v=input(f"Enter vertex {i+1}:")
    l=input("Enter neighbours").split()
    graph[v]=l

start=input("Enter start:")    
bfs(graph,start)
