"""
GSP - Goal Stack Planning (Blocks World) with Shortest Path via BFS
Usage: python gsp.py
"""

from collections import deque
import re

# ─── State Transitions ────────────────────────────────────────────────────────

def get_all_actions(blocks):
    actions = []
    for X in blocks:
        actions.append(("pickup",  (X,)))
        actions.append(("putdown", (X,)))
        for Y in blocks:
            if X != Y:
                actions.append(("stack",   (X, Y)))
                actions.append(("unstack", (X, Y)))
    return actions


def is_applicable(state, action_name, args):
    if action_name == "pickup":
        X = args[0]
        return f"onTable({X})" in state and f"clear({X})" in state and "armempty" in state
    elif action_name == "putdown":
        return f"holding({args[0]})" in state
    elif action_name == "stack":
        X, Y = args
        return f"holding({X})" in state and f"clear({Y})" in state
    elif action_name == "unstack":
        X, Y = args
        return f"on({X},{Y})" in state and f"clear({X})" in state and "armempty" in state
    return False


def apply_action(state, action_name, args):
    s = set(state)
    if action_name == "pickup":
        X = args[0]
        return (s - {f"onTable({X})", f"clear({X})", "armempty"}) | {f"holding({X})"}
    elif action_name == "putdown":
        X = args[0]
        return (s - {f"holding({X})"}) | {f"onTable({X})", f"clear({X})", "armempty"}
    elif action_name == "stack":
        X, Y = args
        return (s - {f"holding({X})", f"clear({Y})"}) | {f"on({X},{Y})", f"clear({X})", "armempty"}
    elif action_name == "unstack":
        X, Y = args
        return (s - {f"on({X},{Y})", f"clear({X})", "armempty"}) | {f"holding({X})", f"clear({Y})"}


def action_to_str(name, args):
    return f"{name}({','.join(args)})"


def get_preconditions(action_name, args):
    if action_name == "pickup":
        return [f"onTable({args[0]})", f"clear({args[0]})", "armempty"]
    elif action_name == "putdown":
        return [f"holding({args[0]})"]
    elif action_name == "stack":
        return [f"holding({args[0]})", f"clear({args[1]})"]
    elif action_name == "unstack":
        return [f"on({args[0]},{args[1]})", f"clear({args[0]})", "armempty"]
    return []


# ─── BFS for Shortest Plan ────────────────────────────────────────────────────

def bfs_shortest(start_state, goal, blocks):
    start    = frozenset(start_state)
    goal_set = frozenset(goal)
    all_acts = get_all_actions(blocks)

    queue   = deque()
    queue.append((start, []))
    visited = {start}

    while queue:
        state, plan = queue.popleft()

        if goal_set.issubset(state):
            return plan

        for aname, aargs in all_acts:
            if is_applicable(state, aname, aargs):
                new_state = frozenset(apply_action(state, aname, aargs))
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, plan + [action_to_str(aname, aargs)]))

    return None


# ─── GSP-style Push/Pop Trace ─────────────────────────────────────────────────

def gsp_trace(start_state, goal, plan):
    state = set(start_state)
    print(f"\npush  -> {' ^ '.join(goal)}")

    for a_str in plan:
        m     = re.match(r'(\w+)\(([^)]*)\)', a_str)
        aname = m.group(1)
        aargs = tuple(x.strip() for x in m.group(2).split(",")) if m.group(2) else ()
        precs = get_preconditions(aname, aargs)

        print(f"push  ->{a_str}   /* action */")
        print(f"push  ->{' ^ '.join(precs)}   /* preconditions of {a_str} */")

        for p in precs:
            if p in state:
                print(f"pop   <- {p}   /* true in current state */")
            else:
                print(f"pop   <- {p}   /* achieved */")

        state = apply_action(state, aname, aargs)
        print(f"pop   <- {a_str}")
        print(f"S = {{{', '.join(sorted(state))}}}")

    print(f"\nPlan = ({', '.join(plan)})")


# ─── Input Parsing ────────────────────────────────────────────────────────────

def parse_predicates(text):
    predicates, current, depth = [], "", 0
    for ch in text:
        if ch == "(":
            depth += 1; current += ch
        elif ch == ")":
            depth -= 1; current += ch
        elif ch == "," and depth == 0:
            p = current.strip()
            if p: predicates.append(p)
            current = ""
        else:
            current += ch
    p = current.strip()
    if p: predicates.append(p)
    return predicates


def extract_blocks(predicates):
    blocks = set()
    for p in predicates:
        for arg_group in re.findall(r'\(([^)]+)\)', p):
            for a in arg_group.split(","):
                a = a.strip()
                if a: blocks.add(a)
    return blocks


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  GSP - Goal Stack Planning | Blocks World")
    print("  Shortest Path via BFS")
    print("=" * 60)
    print()
    print("Predicates: onTable(X), on(X,Y), clear(X), holding(X), armempty")
    print()
    print("Example start : onTable(A), onTable(B), onTable(C), clear(A), clear(B), clear(C), armempty")
    print("Example goal  : on(A,B), on(B,C)")
    print()

    start_input = input("Start state : ").strip()
    goal_input  = input("Goal state  : ").strip()

    start  = parse_predicates(start_input)
    goal   = parse_predicates(goal_input)
    blocks = extract_blocks(start + goal)

    print()
    print("-" * 60)
    print(f"Start  : {{{', '.join(start)}}}")
    print(f"Goal   : {{{', '.join(goal)}}}")
    print(f"Blocks : {{{', '.join(sorted(blocks))}}}")
    print("-" * 60)
    print("\nSearching for shortest plan via BFS...")

    plan = bfs_shortest(start, goal, blocks)

    print()
    if plan is None:
        print("=" * 60)
        print("  NO SOLUTION FOUND")
        print("=" * 60)
        return

    print(f"Shortest plan length: {len(plan)} action(s)")
    print("-" * 60)

    gsp_trace(start, goal, plan)

    print()
    print("=" * 60)
    print(f"  SOLUTION FOUND  (optimal: {len(plan)} steps)")
    print(f"  Plan = ({', '.join(plan)})")
    print("=" * 60)


if __name__ == "__main__":
    main()