from collections import deque
def bfs(graph,state,visited):
    visited=[]    
    q=deque()
    
    q.append(state)
    visited.append(state)
    while q:
        node=q.popleft()
        print(node,end=' ')    
        for n in graph[node]:
            if n not in visited:
                visited.append(n)
                q.append(n)
            
    
graph={}
visited=[]

n=int(input("Enter no of nodes:"))


for _ in range(n):
    node=input("Enter node:")
    neighbors=input("Enter neighbors:").split()
    graph[node]=neighbors

start=input("Enter start:")
bfs(graph,start,visited)    