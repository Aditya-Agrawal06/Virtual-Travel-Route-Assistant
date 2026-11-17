# Buddy - Travel Route Assistant

Buddy is a text-based virtual assistant written in basic Python for the Artificial Intelligence lab. It does one job: **it helps you travel between cities by finding routes for you.**

You type a request, Buddy picks the matching skill, and the answer is produced by a search algorithm from the course syllabus.

## How to run

Requires only Python 3. No libraries to install.

    python assistant.py

Type `help` to see what Buddy can do, and `bye` to exit.

## What Buddy can do

| Command   | What Buddy does                                                        | Syllabus topic                    |
|-----------|------------------------------------------------------------------------|-----------------------------------|
| `route`   | Finds a route between two cities. Choose bfs, dfs, ids, astar or all.  | BFS, DFS, Iterative Deepening, A* |
| `detour`  | Plans a route, then replans from the current city when a road is found closed | D* (simplified replanning idea) |
| `cities`  | Lists the cities Buddy knows                                           | -                                 |

## How it works

1. Buddy reads what you type and looks for a keyword (e.g. "route", "detour").
2. The cities and roads are stored as a graph.
3. The chosen search algorithm explores the graph and returns the path.
4. Buddy prints the route and its distance.

Choosing `all` runs every algorithm on the same trip so you can compare them. BFS finds the route with the fewest stops, DFS may find a longer route, and A* finds the shortest distance by using straight-line distance as its guide.

## Example session

    You: route
    Cities: Ahmedabad, Gandhinagar, Mehsana, Palanpur, Vadodara, Surat, Rajkot, Bhavnagar
    From: Ahmedabad
    To: Surat
    Algorithm (bfs / dfs / ids / astar / all): all
    Buddy: BFS: Ahmedabad -> Vadodara -> Surat (281 km)
    Buddy: DFS: Ahmedabad -> Bhavnagar -> Surat (383 km)
    Buddy: Iterative Deepening: Ahmedabad -> Vadodara -> Surat (281 km)
    Buddy: A*: Ahmedabad -> Vadodara -> Surat (281 km)

## Notes

- The city map uses made-up coordinates, only for demonstration.
- `detour` is a simplified version of D*: it replans with A* from the current city when a new blocked road is found, instead of the full incremental D* algorithm.

## Files

- `assistant.py` - the whole project
- `README.md` - this file


## MADE BY:
Aditya Agrawal

2025KUAD3032
