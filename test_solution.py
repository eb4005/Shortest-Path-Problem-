"""
Unit tests for the Layered Dijkstra shortest-path-with-K-special-edges solver.

Each test constructs edges in 0-indexed form (as expected by solve()) and
verifies the output against a known correct answer.

Run:  python test_solution.py
"""

import unittest
from math import inf
from solution import solve


class TestShortestPathKSpecial(unittest.TestCase):
    """Tests for solve(n, m, K, s, t, edges)."""

    # ------------------------------------------------------------------ #
    # Basic / example tests
    # ------------------------------------------------------------------ #

    def test_example_from_docstring(self):
        """The 4-node, 5-edge example from the docstring (K=2)."""
        # 1→2 w=1 b=0,  1→3 w=3 b=1,  2→4 w=10 b=1,
        # 3→2 w=1 b=1,  3→4 w=5 b=0
        # (0-indexed)
        edges = [
            (0, 1, 1, 0),
            (0, 2, 3, 1),
            (1, 3, 10, 1),
            (2, 1, 1, 1),
            (2, 3, 5, 0),
        ]
        # Walk 1→2→4 uses special edges {2→4} → only 1 special, not valid for K=2.
        # Walk 1→3→2→4 uses special edges {1→3, 3→2, 2→4} → 3 special, too many.
        # Walk 1→3→4 uses special edge {1→3} → 1 special.
        # Walk 1→2→(via non-special) … need to find path with exactly 2.
        # Actually: 1→3(special, w3)→4(non-special, w5) = 1 special.
        #           1→2(non-special, w1)→4(special, w10) = 1 special.
        #           1→3(special, w3)→2(special, w1)→… k=2 reached, need non-special to 4
        #             but 2→4 is special. Dead end for exactly 2.
        # Best K=2: 1→3(special)→2(special)→ now at node 2 with k=2.
        #   From 2, only edge is 2→4(special) → would make k=3, skip.
        #   No non-special edge from 2 → IMPOSSIBLE?  Actually need to check graph.
        #   Actually 1→2 is in adj[0], but we need adj[1] to have a non-special to 3.
        #   adj[1] = [(3,10,1)], adj[2] = [(1,1,1),(3,5,0)]
        #   From node 1 (0-idx) with k=2: edge (1→3, w=10, special) → k=3>2, skip.
        #   So K=2 from 0→3 is IMPOSSIBLE through that sub-path?  Wait—
        #   Let me re-check: 0→2(special,3)→1(special,1) → at node1,k=2
        #     node1 edges: (3,10,1) → k=3, skip. Dead end. 
        #   0→2(special,3)→3(non-special,5) → at node3,k=1 (not 2). 
        #   0→1(non-special,1)→3(special,10) → at node3,k=1.
        #   Seems like K=2 might be IMPOSSIBLE for this graph.
        result = solve(4, 5, 2, 0, 3, edges)
        self.assertEqual(result, "IMPOSSIBLE")

    def test_simple_all_special(self):
        """Single path s→t with one special edge, K=1."""
        edges = [(0, 1, 5, 1)]
        self.assertEqual(solve(2, 1, 1, 0, 1, edges), "5")

    def test_simple_no_special_needed(self):
        """K=0: just find shortest path ignoring special edges."""
        edges = [
            (0, 1, 3, 0),
            (1, 2, 4, 0),
            (0, 2, 10, 0),
        ]
        self.assertEqual(solve(3, 3, 0, 0, 2, edges), "7")

    def test_k_zero_with_special_edges_present(self):
        """K=0 but special edges exist — they must be avoided entirely."""
        edges = [
            (0, 1, 1, 1),   # special — can't use
            (0, 1, 10, 0),  # non-special — must use this
        ]
        self.assertEqual(solve(2, 2, 0, 0, 1, edges), "10")

    # ------------------------------------------------------------------ #
    # Impossible cases
    # ------------------------------------------------------------------ #

    def test_no_path(self):
        """No edges at all → IMPOSSIBLE."""
        self.assertEqual(solve(3, 0, 0, 0, 2, []), "IMPOSSIBLE")

    def test_not_enough_special_edges(self):
        """Path exists but doesn't have K special edges."""
        edges = [
            (0, 1, 1, 0),
            (1, 2, 1, 0),
        ]
        self.assertEqual(solve(3, 2, 1, 0, 2, edges), "IMPOSSIBLE")

    def test_too_many_special_forced(self):
        """Only path has 2 special edges, but K=1."""
        edges = [
            (0, 1, 1, 1),
            (1, 2, 1, 1),
        ]
        self.assertEqual(solve(3, 2, 1, 0, 2, edges), "IMPOSSIBLE")

    # ------------------------------------------------------------------ #
    # Walk (not just simple path) tests
    # ------------------------------------------------------------------ #

    def test_walk_revisits_vertex(self):
        """
        Optimal walk must revisit a vertex.
        Graph: 0 ↔ 1 (special, w=1 each direction) and 0→2 (non-special, w=1).
        K=2: walk 0→1(special)→0(special)→2(non-special) = weight 3.
        """
        edges = [
            (0, 1, 1, 1),  # 0→1 special
            (1, 0, 1, 1),  # 1→0 special
            (0, 2, 1, 0),  # 0→2 non-special
        ]
        self.assertEqual(solve(3, 3, 2, 0, 2, edges), "3")

    def test_walk_revisits_edge(self):
        """
        Optimal walk must reuse the same edge.
        0→1 (special, w=1), 1→0 (non-special, w=1), 0→2 (non-special, w=100).
        K=2: 0→1(sp)→0(non-sp)→1(sp)→0(non-sp)→2 = 1+1+1+1+100 = 104
        K=0: 0→2 = 100
        """
        edges = [
            (0, 1, 1, 1),
            (1, 0, 1, 0),
            (0, 2, 100, 0),
        ]
        self.assertEqual(solve(3, 3, 0, 0, 2, edges), "100")
        self.assertEqual(solve(3, 3, 2, 0, 2, edges), "104")

    # ------------------------------------------------------------------ #
    # Multiple paths — pick cheapest with correct K
    # ------------------------------------------------------------------ #

    def test_choose_cheaper_path(self):
        """Two paths with exactly K=1 special edge, pick the cheaper one."""
        edges = [
            (0, 1, 2, 1),   # 0→1 special w=2
            (1, 3, 1, 0),   # 1→3 non-special w=1  → total = 3
            (0, 2, 5, 1),   # 0→2 special w=5
            (2, 3, 1, 0),   # 2→3 non-special w=1  → total = 6
        ]
        self.assertEqual(solve(4, 4, 1, 0, 3, edges), "3")

    def test_k_equals_path_length(self):
        """All edges on the only path are special."""
        edges = [
            (0, 1, 2, 1),
            (1, 2, 3, 1),
            (2, 3, 4, 1),
        ]
        self.assertEqual(solve(4, 3, 3, 0, 3, edges), "9")

    # ------------------------------------------------------------------ #
    # Edge cases
    # ------------------------------------------------------------------ #

    def test_source_equals_target_k_zero(self):
        """s == t with K=0 → distance is 0."""
        edges = [(0, 1, 5, 1)]
        self.assertEqual(solve(2, 1, 0, 0, 0, edges), "0")

    def test_source_equals_target_k_positive(self):
        """s == t with K=2 → must take a loop using exactly 2 special edges."""
        edges = [
            (0, 1, 1, 1),  # special
            (1, 0, 1, 1),  # special
        ]
        # Walk: 0→1(sp)→0(sp), cost = 2, K=2 ✓
        self.assertEqual(solve(2, 2, 2, 0, 0, edges), "2")

    def test_large_k_zero(self):
        """K=0 on a graph with no special edges — standard shortest path."""
        edges = [
            (0, 1, 1, 0),
            (1, 2, 2, 0),
            (0, 2, 5, 0),
        ]
        self.assertEqual(solve(3, 3, 0, 0, 2, edges), "3")

    def test_float_weights(self):
        """Non-integer weights should work correctly."""
        edges = [
            (0, 1, 1.5, 1),
            (1, 2, 2.5, 0),
        ]
        # solve() converts whole-number floats to int: 4.0 → "4"
        self.assertEqual(solve(3, 2, 1, 0, 2, edges), "4")

    def test_zero_weight_edges(self):
        """Zero-weight edges are valid."""
        edges = [
            (0, 1, 0, 1),
            (1, 2, 0, 0),
        ]
        self.assertEqual(solve(3, 2, 1, 0, 2, edges), "0")


if __name__ == "__main__":
    unittest.main()
