# Shortest Path with Exactly K Special Edges

A Python implementation of the **Layered Dijkstra** algorithm for finding the minimum-weight directed walk between two vertices that uses **exactly K special edges**.

## Problem Statement

Given a directed graph $G = (V, E)$ with $|V| = n$ and $|E| = m$, where each edge $e = (u, v)$ has:
- A **nonnegative weight** $w(e) \geq 0$
- A **binary attribute** $b(e) \in \{0, 1\}$ indicating whether the edge is *special* ($b(e) = 1$) or not ($b(e) = 0$)

Given two vertices $s, t \in V$ and an integer $K \geq 0$, find:

$$\min_{P \in \mathcal{P}(s,t)} \sum_{e \in P} w(e) \quad \text{such that} \quad \sum_{e \in P} b(e) = K$$

where $\mathcal{P}(s,t)$ denotes the set of all directed $s \to t$ walks in $G$.

If no such walk exists, output `IMPOSSIBLE`.

### Constraints
- $n, m \leq 2 \times 10^5$
- $K \leq 100$

## Algorithm

**Layered Dijkstra on the product graph $G \times \{0, 1, \dots, K\}$.**

The key insight is to expand the state space: each state $(v, k)$ represents "currently at vertex $v$, having used exactly $k$ special edges so far."

### Transitions
From state $(u, k)$, for each edge $(u \to v, w, b)$:
| Edge Type | Condition | New State | Cost |
|---|---|---|---|
| Non-special ($b = 0$) | Always | $(v, k)$ | $w$ |
| Special ($b = 1$) | $k + 1 \leq K$ | $(v, k+1)$ | $w$ |

### Answer
$\text{dist}[t][K]$ — the minimum cost to reach $t$ using exactly $K$ special edges.

### Complexity
- **States**: $O(n \cdot K)$
- **Relaxations**: $O(m \cdot K)$
- **Total**: $O(m \cdot K \cdot \log(n \cdot K))$

With $m \leq 2 \times 10^5$ and $K \leq 100$, this gives ~$2 \times 10^7$ relaxations with ~24-bit heap operations — feasible within time limits.

## Usage

### Input Format (stdin)
```
n m K s t
u₁ v₁ w₁ b₁
u₂ v₂ w₂ b₂
...
uₘ vₘ wₘ bₘ
```
- **Line 1**: `n` (vertices), `m` (edges), `K` (required special edges), `s` (source), `t` (target) — all **1-indexed**
- **Lines 2 to m+1**: edge `u → v` with weight `w` and special flag `b ∈ {0, 1}`

### Running
```bash
# From file
python solution.py < input.txt

# Inline example
echo "4 5 2 1 4
1 2 1 0
1 3 3 1
2 4 10 1
3 2 1 1
3 4 5 0" | python solution.py
```

### Output
The minimum total weight (as an integer if whole, otherwise float), or `IMPOSSIBLE`.

## Example Walkthrough

Given the graph with 4 vertices, 5 edges, K=2, source=1, target=4:

```
Edges:
  1 → 2  (weight=1, non-special)
  1 → 3  (weight=3, special)
  2 → 4  (weight=10, special)
  3 → 2  (weight=1, special)
  3 → 4  (weight=5, non-special)
```

**Optimal walk**: 1 → 3 → 4 uses special edge 1→3, then non-special 3→4 — but that's only 1 special edge. We need exactly 2.

**Walk with K=2 special edges**: 1 → 3 → 2 → 4 uses special edges 1→3 and 3→2... but 2→4 is also special (that would be 3). The answer depends on available paths with exactly 2 special edges.

## Running Tests

```bash
python test_solution.py
```

## Project Structure

```
├── README.md              # This file
├── solution.py            # Main algorithm implementation
├── test_solution.py       # Unit tests
├── Shortest Path.pdf      # Original problem statement
└── .gitignore
```

## License

MIT
