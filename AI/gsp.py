"""
GSP - Goal Stack Planning (Blocks World)
Usage: python gsp.py
"""

# ─── Action Definitions ───────────────────────────────────────────────────────

ACTIONS = {
    "pickup(X)": {
        "preconditions": lambda s, X: f"onTable({X})" in s and f"clear({X})" in s and "armempty" in s,
        "add":          lambda X: {f"holding({X})"},
        "delete":       lambda X: {f"onTable({X})", f"clear({X})", "armempty"},
    },
    "putdown(X)": {
        "preconditions": lambda s, X: f"holding({X})" in s,
        "add":           lambda X: {f"onTable({X})", f"clear({X})", "armempty"},
        "delete":        lambda X: {f"holding({X})"},
    },
    "stack(X,Y)": {
        "preconditions": lambda s, X, Y: f"holding({X})" in s and f"clear({Y})" in s,
        "add":           lambda X, Y: {f"on({X},{Y})", f"clear({X})", "armempty"},
        "delete":        lambda X, Y: {f"holding({X})", f"clear({Y})"},
    },
    "unstack(X,Y)": {
        "preconditions": lambda s, X, Y: f"on({X},{Y})" in s and f"clear({X})" in s and "armempty" in s,
        "add":           lambda X, Y: {f"holding({X})", f"clear({Y})"},
        "delete":        lambda X, Y: {f"on({X},{Y})", f"clear({X})", "armempty"},
    },
}


def get_applicable_actions(state, blocks):
    """Return all ground actions applicable to achieve any predicate."""
    actions = []
    for X in blocks:
        actions.append(("pickup", (X,)))
        actions.append(("putdown", (X,)))
        for Y in blocks:
            if X != Y:
                actions.append(("stack", (X, Y)))
                actions.append(("unstack", (X, Y)))
    return actions


def apply_action(state, action_name, args):
    if action_name == "pickup":
        X = args[0]
        new = (state - {f"onTable({X})", f"clear({X})", "armempty"}) | {f"holding({X})"}
    elif action_name == "putdown":
        X = args[0]
        new = (state - {f"holding({X})"}) | {f"onTable({X})", f"clear({X})", "armempty"}
    elif action_name == "stack":
        X, Y = args
        new = (state - {f"holding({X})", f"clear({Y})"}) | {f"on({X},{Y})", f"clear({X})", "armempty"}
    elif action_name == "unstack":
        X, Y = args
        new = (state - {f"on({X},{Y})", f"clear({X})", "armempty"}) | {f"holding({X})", f"clear({Y})"}
    return new


def action_achieves(predicate, action_name, args):
    """Check if an action adds a specific predicate."""
    if action_name == "pickup":
        return predicate == f"holding({args[0]})"
    elif action_name == "putdown":
        X = args[0]
        return predicate in {f"onTable({X})", f"clear({X})", "armempty"}
    elif action_name == "stack":
        X, Y = args
        return predicate in {f"on({X},{Y})", f"clear({X})", "armempty"}
    elif action_name == "unstack":
        X, Y = args
        return predicate in {f"holding({X})", f"clear({Y})"}
    return False


def action_to_str(name, args):
    return f"{name}({','.join(args)})"


def GSP(given_state, given_goal, blocks, verbose=True):
    state = set(given_state)
    plan = []
    stack = []

    # Push goal set
    stack.append(("goal_set", frozenset(given_goal)))
    for g in given_goal:
        stack.append(("goal", g))

    if verbose:
        print(f"\npush  → {' ∧ '.join(given_goal)}")

    visited = set()
    max_steps = 200

    for _ in range(max_steps):
        if not stack:
            break

        x = stack.pop()
        kind = x[0]

        if kind == "action":
            action_name, args = x[1], x[2]
            a_str = action_to_str(action_name, args)
            plan.append(a_str)
            state = apply_action(state, action_name, args)
            if verbose:
                print(f"pop   ← {a_str}")
                print(f"S = {{{', '.join(sorted(state))}}}")

        elif kind == "goal":
            g = x[1]
            if g in state:
                if verbose:
                    print(f"pop   ← {g}   /* true in current state */")
                continue
            # Find action that achieves g
            chosen = None
            for aname, aargs in get_applicable_actions(state, blocks):
                if action_achieves(g, aname, aargs):
                    chosen = (aname, aargs)
                    break
            if chosen is None:
                if verbose:
                    print(f"\nFAILURE: no action achieves {g}")
                return None
            aname, aargs = chosen
            a_str = action_to_str(aname, aargs)
            if verbose:
                print(f"push  →{a_str}   /* action to achieve {g} */")
            # Push: preconditions, then action
            stack.append(("action", aname, aargs))
            # Push preconditions as a goal set
            if aname == "pickup":
                precs = [f"onTable({aargs[0]})", f"clear({aargs[0]})", "armempty"]
            elif aname == "putdown":
                precs = [f"holding({aargs[0]})"]
            elif aname == "stack":
                precs = [f"holding({aargs[0]})", f"clear({aargs[1]})"]
            elif aname == "unstack":
                precs = [f"on({aargs[0]},{aargs[1]})", f"clear({aargs[0]})", "armempty"]
            else:
                precs = []
            if verbose:
                print(f"push  →{' ∧ '.join(precs)}   /* preconditions of {a_str} */")
            for p in reversed(precs):
                stack.append(("goal", p))

        elif kind == "goal_set":
            goals = set(x[1])
            unsatisfied = [g for g in goals if g not in state]
            if unsatisfied:
                if verbose:
                    print(f"push  → {' ∧ '.join(goals)}")
                for g in reversed(unsatisfied):
                    stack.append(("goal", g))

    # Check goal achieved
    if all(g in state for g in given_goal):
        if verbose:
            print(f"\nPlan = ({', '.join(plan)})")
        return plan
    else:
        if verbose:
            print("\nFAILURE: goal not achieved within step limit")
        return None


# ─── Input Parsing ────────────────────────────────────────────────────────────

def parse_predicates(text):
    """Parse comma-separated predicates like: onTable(A), clear(B), armempty
    Handles commas inside parentheses (e.g. on(A,B))."""
    predicates = []
    current = ""
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
            current += ch
        elif ch == ")":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            p = current.strip()
            if p:
                predicates.append(p)
            current = ""
        else:
            current += ch
    p = current.strip()
    if p:
        predicates.append(p)
    return predicates


def extract_blocks(predicates):
    """Extract block names from predicates."""
    import re
    blocks = set()
    for p in predicates:
        args = re.findall(r'\(([^)]+)\)', p)
        for arg in args:
            for a in arg.split(","):
                a = a.strip()
                if a and a != "armempty":
                    blocks.add(a)
    return blocks


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  GSP - Goal Stack Planning | Blocks World")
    print("=" * 60)
    print()
    print("Enter predicates as comma-separated values.")
    print("Available: onTable(X), on(X,Y), clear(X), holding(X), armempty")
    print()
    print("Example start: onTable(A), onTable(B), onTable(C), clear(A), clear(B), clear(C), armempty")
    print("Example goal : on(A,B), on(B,C)")
    print()

    start_input = input("Start state : ").strip()
    goal_input  = input("Goal state  : ").strip()

    start = parse_predicates(start_input)
    goal  = parse_predicates(goal_input)

    blocks = extract_blocks(start + goal)

    print()
    print("-" * 60)
    print(f"Start : {{{', '.join(start)}}}")
    print(f"Goal  : {{{', '.join(goal)}}}")
    print(f"Blocks: {{{', '.join(sorted(blocks))}}}")
    print("-" * 60)

    plan = GSP(start, goal, blocks, verbose=True)

    print()
    if plan:
        print("=" * 60)
        print(f"  SOLUTION FOUND")
        print(f"  Plan = ({', '.join(plan)})")
        print("=" * 60)
    else:
        print("=" * 60)
        print("  NO SOLUTION FOUND")
        print("=" * 60)


if __name__ == "__main__":
    main()