start=[
    [1,0,4],
    [2,5,7],
    [3,6,8]
]
goal=[
    [1,4,7],
    [2,5,8],
    [3,6,0]
]


def h(state):
    count=0
    for i in range(3):
        for j in range(3):
            if state[i][j]!=0 and state[i][j]==goal[i][j]:
                count+=1
                
    return 8-count

def moveGen(state):
    next_states=[]
    for i in range(3):
        for j in range(3):
            if state[i][j]==0:
                r=i
                c=j
    
    new_states={
        (r-1,c),
        (r,c-1),
        (r+1,c),
        (r,c+1)
    }
    
    for st in new_states:
        newr=st[0]
        newc=st[1]
        if newr<0 or newc<0 or newr>2 or newc>2:
            continue
        new_state=state
        new_state[newr][newc],new_state[r][c]=new_state[r][c],new_state[newr][newc]
        next_states.append(new_states)
    
    return next_states


def hillClimb(state):
    path=[]
    while True:
        path.append(state)
        if h(start)==0:
            return path
        