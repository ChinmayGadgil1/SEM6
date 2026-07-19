from math import gcd

def is_possible(target,jug1_c,jug2_c):
    if target%gcd(jug1_c,jug2_c)!=0:
        return False
    else: 
        return True


def dfs(target,jug1_c,jug2_c,state,visited=None,path=None):
    if visited is None:
        visited=[]
    if path is None:
        path=[]
    
    j1,j2=state
    visited.append(state)
    path.append(state)
    if j1==target or j2==target:
        for x,y in enumerate(path):
            print(f"Step{x}: {y}")
        return True
    
    next_states=[
        (jug1_c, j2),
        (j1, jug2_c), 
        (0, j2), 
        (j1, 0), 
        (j1 - min(j1, jug2_c - j2), j2 + min(j1, jug2_c - j2)), 
        (j1 + min(j2, jug1_c - j1), j2 - min(j2, jug1_c - j1)) 
    ]
    
    for n in next_states:
        if n[0] < 0 or n[1] < 0:
            continue
        if n[0] > jug1_c or n[1] > jug2_c:
            continue
        if n not in visited:
            result = dfs(target, jug1_c, jug2_c,n, visited, path)
            if result:
                return result
    

jug1_c=int(input("Enter jug1 cap:"))
jug2_c=int(input("Enter jug2 cap:"))
target=int(input("Enter target:"))

if is_possible(target,jug1_c,jug2_c):
    start=(0,0)
    dfs(target,jug1_c,jug2_c,start)
else:
    print("Not possible")
