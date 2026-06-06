"""
Shortest s-t walk with exactly K special edges.

Algorithm: Layered Dijkstra on the product graph G x {0,1,...,K}.
State (v, k) = "currently at vertex v, having used exactly k special edges."

Transitions from state (u, k):
  For each edge (u -> v, weight w, special b):
    if b == 0: relax (v, k)     with cost w   [non-special: k unchanged]
    if b == 1: relax (v, k+1)  with cost w   [special: k increments]
                                (only if k+1 <= K)

Answer: dist[t][K]

Complexity: O(m * K * log(n * K))
            m,K <= 2e5, 100 => ~2e7 relaxations, ~log(2e7) ~ 24 => feasible.

Input format (stdin):
    Line 1: n m K s t          (1-indexed vertices)
    Lines 2..m+1: u v w b      (edge u->v, weight w, special flag b in {0,1})

Output: minimum total weight (float/int), or "IMPOSSIBLE"

Usage examples:
    python solution.py < input.txt
    echo "4 5 2 1 4
1 2 1 0
1 3 3 1
2 4 10 1
3 2 1 1
3 4 5 0" | python solution.py
"""

import heapq
import sys
from math import inf


def solve(n: int, m: int, K: int, s: int, t: int, edges: list) -> str:
    # Build adjacency list: adj[u] = list of (v, w, b)
    adj = [[] for _ in range(n)]
    for u, v, w, b in edges:
        adj[u].append((v, w, b))

    # dist[v][k] = min cost to reach v using exactly k special edges
    INF = inf
    dist = [[INF] * (K + 1) for _ in range(n)]
    dist[s][0] = 0.0

    # Min-heap: (cost, node, special_count_used)
    heap = [(0.0, s, 0)]

    while heap:
        d, u, k = heapq.heappop(heap)

        # Stale entry check
        if d > dist[u][k]:
            continue

        for v, w, b in adj[u]:
            nk = k + b                    # new special count after traversing edge
            if nk > K:
                continue                  # can't exceed K special edges
            nd = d + w
            if nd < dist[v][nk]:
                dist[v][nk] = nd
                heapq.heappush(heap, (nd, v, nk))

    ans = dist[t][K]
    if ans == INF:
        return "IMPOSSIBLE"
    # Return int if answer is whole number, else float
    return str(int(ans) if ans == int(ans) else ans)


def main():
    input_data = sys.stdin.read().split()
    idx = 0

    def rd():
        nonlocal idx
        v = input_data[idx]; idx += 1
        return v

    n, m, K, s, t = int(rd()), int(rd()), int(rd()), int(rd()), int(rd())
    s -= 1; t -= 1          # convert to 0-indexed

    edges = []
    for _ in range(m):
        u, v, w, b = int(rd()), int(rd()), float(rd()), int(rd())
        u -= 1; v -= 1
        edges.append((u, v, w, b))

    print(solve(n, m, K, s, t, edges))


if __name__ == "__main__":
    main()
