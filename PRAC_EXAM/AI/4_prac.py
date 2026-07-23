
def mcdfs(state,visited=None,path=None):
    if visited is None:
        visited=[]
    if path is None:
        path=[]
    visited.append(state)
    path.append(state)
    
    m,c,b=state
    
    if b=='L':
        new_states={
            (m-2,c,'R'),
            (m,c-2,'R'),
            (m-1,c-1,'R'),
            (m-1,c,'R'),
            (m,c-1,'R')
        }
    else:
        new_states={
            (m+2,c,'L'),
            (m,c+2,'L'),
            (m+1,c+1,'L'),
            (m+1,c,'L'),
            (m,c+1,'L')
        }

    if state[0]==0 and state[1]==0 and b=='R':
        for p in path:
            print(p,end=' ')
        print()
        return True
    
    for st in new_states:
        if st[0]<0 or st[1]<0 or st[0]>3 or st[1]>3:
            continue
        if st[0]<st[1] and st[0]>0:
            continue
        if 3-st[0]<3-st[1] and 3-st[0]>0:
            continue
        if st not in visited:
            result=mcdfs(st,visited,path)
            if result:
                return True

    path.pop()
    return None
    
m=int(input("Enter no of missionaries:"))
c=int(input("Enter no of cannibals:"))
b='L'

start=(m,c,b)
mcdfs(start)

