"""Buddy - a travel route assistant (AI lab project). Run it and type 'help'."""

import math
import heapq
from collections import deque

# Made-up (x, y) positions in km, used only for the project demo
COORDS = {
    "Ahmedabad": (0, 0),
    "Gandhinagar": (0, 25),
    "Mehsana": (-30, 60),
    "Palanpur": (-40, 120),
    "Vadodara": (100, -10),
    "Surat": (130, -140),
    "Rajkot": (-170, -60),
    "Bhavnagar": (-50, -130),
}

LINKS = [
    ("Ahmedabad", "Gandhinagar"), ("Ahmedabad", "Mehsana"),
    ("Gandhinagar", "Mehsana"), ("Mehsana", "Palanpur"),
    ("Ahmedabad", "Vadodara"), ("Vadodara", "Surat"),
    ("Ahmedabad", "Rajkot"), ("Ahmedabad", "Bhavnagar"),
    ("Rajkot", "Bhavnagar"), ("Bhavnagar", "Surat"),
]

# Road length = straight-line distance * 1.2 (so the A* heuristic never overestimates)
ROADS = {city: {} for city in COORDS}
for a, b in LINKS:
    d = round(math.dist(COORDS[a], COORDS[b]) * 1.2)
    ROADS[a][b] = d
    ROADS[b][a] = d

NAMES = {"bfs": "BFS", "dfs": "DFS", "ids": "Iterative Deepening", "astar": "A*"}


def path_cost(path):
    total = 0
    for i in range(len(path) - 1):
        total += ROADS[path[i]][path[i + 1]]
    return total


def bfs(start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        city = path[-1]
        if city == goal:
            return path
        for nxt in ROADS[city]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None


def dfs(start, goal):
    stack = [[start]]
    visited = set()
    while stack:
        path = stack.pop()
        city = path[-1]
        if city == goal:
            return path
        if city in visited:
            continue
        visited.add(city)
        for nxt in ROADS[city]:
            stack.append(path + [nxt])
    return None


def depth_limited(path, goal, limit):
    city = path[-1]
    if city == goal:
        return path
    if limit == 0:
        return None
    for nxt in ROADS[city]:
        if nxt not in path:
            result = depth_limited(path + [nxt], goal, limit - 1)
            if result:
                return result
    return None


def ids(start, goal):
    # Iterative Deepening: try depth 0, 1, 2, ... until the goal is found
    for limit in range(len(ROADS)):
        result = depth_limited([start], goal, limit)
        if result:
            return result
    return None


def straight_line(a, b):
    return math.dist(COORDS[a], COORDS[b])


def a_star(start, goal, blocked=()):
    # frontier items: (f = g + h, g, path)
    frontier = [(straight_line(start, goal), 0, [start])]
    best_g = {}
    while frontier:
        f, g, path = heapq.heappop(frontier)
        city = path[-1]
        if city == goal:
            return path, g
        if city in best_g and best_g[city] <= g:
            continue
        best_g[city] = g
        for nxt, cost in ROADS[city].items():
            if nxt in blocked:
                continue
            new_g = g + cost
            heapq.heappush(frontier, (new_g + straight_line(nxt, goal), new_g, path + [nxt]))
    return None, 0


def find_path(algo, start, goal):
    if algo == "bfs":
        return bfs(start, goal)
    if algo == "dfs":
        return dfs(start, goal)
    if algo == "ids":
        return ids(start, goal)
    path, _ = a_star(start, goal)
    return path


def ask_two_cities():
    print("Cities:", ", ".join(ROADS))
    start = input("From: ").strip().title()
    goal = input("To: ").strip().title()
    if start not in ROADS or goal not in ROADS:
        print("Buddy: I don't know one of those cities.")
        return None, None
    return start, goal


def route_skill():
    start, goal = ask_two_cities()
    if start is None:
        return
    choice = input("Algorithm (bfs / dfs / ids / astar / all): ").strip().lower()
    if choice == "all":
        chosen = list(NAMES)
    elif choice in NAMES:
        chosen = [choice]
    else:
        print("Buddy: I don't know that algorithm.")
        return
    for algo in chosen:
        path = find_path(algo, start, goal)
        if path is None:
            print(f"Buddy: {NAMES[algo]} found no route.")
        else:
            print(f"Buddy: {NAMES[algo]}: {' -> '.join(path)} ({path_cost(path)} km)")


def detour_skill():
    # D*-style idea: plan with A*, and if a new blocked road is discovered
    # while travelling, replan from the CURRENT city (not from the start).
    start, goal = ask_two_cities()
    if start is None:
        return
    closed = input("Which city's road is closed (unknown to me yet)? ").strip().title()
    current = start
    travelled = [start]
    blocked = []
    while current != goal:
        path, _ = a_star(current, goal, blocked)
        if path is None:
            print("Buddy: There is no route to", goal)
            return
        nxt = path[1]
        if nxt == closed and closed not in blocked:
            print(f"Buddy: Oh no, the road to {closed} is closed! Replanning from {current}...")
            blocked.append(closed)
            continue
        travelled.append(nxt)
        current = nxt
    print("Buddy: Final trip:", " -> ".join(travelled))
    print("Buddy: Distance:", path_cost(travelled), "km")


def show_help():
    print("Buddy: I can help you travel between cities:")
    print("   route   - find a route (bfs, dfs, ids, astar, or all to compare)")
    print("   detour  - find a route when a road turns out to be closed")
    print("   cities  - list the cities I know")
    print("   help, bye")


def main():
    print("Buddy: Hello! I'm Buddy, your travel route assistant. Type 'help' to see what I can do.")
    while True:
        text = input("You: ").strip().lower()
        if text in ("bye", "exit", "quit"):
            print("Buddy: Goodbye!")
            break
        elif text in ("hi", "hello", "hey"):
            print("Buddy: Hello! Where would you like to go?")
        elif "detour" in text or "closed" in text or "blocked" in text:
            detour_skill()
        elif "route" in text or "path" in text:
            route_skill()
        elif "cities" in text:
            print("Buddy: I know:", ", ".join(ROADS))
        elif "help" in text:
            show_help()
        else:
            print("Buddy: Sorry, I didn't understand. Type 'help' to see what I can do.")


main()
