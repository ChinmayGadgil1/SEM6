from math import gcd 
from collections import deque
def is_possible(target,j1_cap,j2_cap):
    if target % gcd(j1_cap,j2_cap)!=0:
        return False
    return True

def bfs(target,j1_cap,j2_cap,start):
    path=[]
    q=deque()
    visited=[]
    visited.append(start)
    q.append(start)
    parent={}
    parent[start]=None
    
    while q:
        state=q.popleft()
        j1,j2=state
        
        if j1==target or j2==target:
            p=parent[state]
            path.append(state)
            while p is not None:
                path.append(p)
                p=parent[p]
            path.reverse()
            return path
        transfer1 = min(j1, j2_cap - j2)   # J1 -> J2
        transfer2 = min(j2, j1_cap - j1)   # J2 -> J1

        new_states = {
            (j1, j2_cap),                      # Fill J2
            (j1_cap, j2),                      # Fill J1
            (0, j2),                           # Empty J1
            (j1, 0),                           # Empty J2
            (j1 - transfer1, j2 + transfer1), # Pour J1 -> J2
            (j1 + transfer2, j2 - transfer2)  # Pour J2 -> J1
        }   
        for st in new_states:
            if st in visited:
                continue
            if st[0] < 0 or st[1] < 0:
                continue
            if st[0] > j1_cap or st[1] > j2_cap:
                continue
            visited.append(st)
            parent[st]=state
            q.append(st)

    


j1_cap=int(input("Enter jug1 capacity:"))
j2_cap=int(input("Enter jug2 capacity:"))
target=int(input("Enter target:"))
if is_possible(target,j1_cap,j2_cap):
    start=(0,0)
    path=bfs(target,j1_cap,j2_cap,start)
    if path is None:
        print("nopath")
    else:
        for p in path:
            print(p,end=" ")
    print()
else:
    print("Not possible")