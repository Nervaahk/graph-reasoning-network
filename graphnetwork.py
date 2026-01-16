import numpy as np


class TopoNode:
    def __init__(self, name, vector_dim=5):
        self.name = name
        self.vector = np.random.rand(vector_dim) * 0.1

    def propagate(self, neighbors, alpha=0.5):
        """Move this node's vector toward the average of neighbor vectors."""
        if not neighbors:
            return
        agg = np.mean([n.vector for n in neighbors], axis=0)
        new_vector = alpha * self.vector + (1 - alpha) * agg
        self.vector = new_vector / (np.linalg.norm(new_vector) + 1e-8)


class ConvergentGraphReasoner:


    def __init__(self, sequence, vector_dim=5, iterations=5, max_infer_iter=5):
        self.sequence = sequence
        self.vector_dim = vector_dim
        self.iterations = iterations
        self.max_infer_iter = max_infer_iter

        self.nodes = []
        self.known = {}  

    def build_nodes(self):
        self.nodes = []
        self.known = {}

        for i, val in enumerate(self.sequence):
            if val is None:
                name = f"B{i}"  
            else:
                name = f"K{i}"  
                self.known[i] = val
            self.nodes.append(TopoNode(name, self.vector_dim))

    def propagate(self):
        # Optional: keep known nodes fixed by skipping updates.
        for _ in range(self.iterations):
            for i, node in enumerate(self.nodes):
                if i in self.known:
                    continue
                neighbors = []
                if i > 0:
                    neighbors.append(self.nodes[i - 1])
                if i < len(self.nodes) - 1:
                    neighbors.append(self.nodes[i + 1])
                node.propagate(neighbors)

    def infer_blanks(self):
        """
        Fill blanks by searching nearest known/inferred neighbors.

        Uses linear interpolation when both sides exist:
            left + (right-left) * (dist_left / total_dist)
        Falls back to +/- 1 stepping if only one side exists.
        """
        inferred = {}  # index -> value

        for _ in range(self.max_infer_iter):
            changed = False

            for i in range(len(self.nodes)):
                if i in self.known:
                    continue

                # nearest known/inferred on the left
                left_idx, left_val = None, None
                for j in range(i - 1, -1, -1):
                    if j in self.known:
                        left_idx, left_val = j, self.known[j]
                        break
                    if j in inferred:
                        left_idx, left_val = j, inferred[j]
                        break

                # nearest known/inferred on the right
                right_idx, right_val = None, None
                for j in range(i + 1, len(self.nodes)):
                    if j in self.known:
                        right_idx, right_val = j, self.known[j]
                        break
                    if j in inferred:
                        right_idx, right_val = j, inferred[j]
                        break

                # propose value
                if left_val is not None and right_val is not None:
                    total = right_idx - left_idx
                    dleft = i - left_idx
                    new_val = left_val + (right_val - left_val) * dleft // total
                elif left_val is not None:
                    new_val = left_val + 1
                elif right_val is not None:
                    new_val = right_val - 1
                else:
                    new_val = 0

                # avoid duplicates (simple global uniqueness)
                used = set(self.known.values()) | set(inferred.values())
                while new_val in used:
                    new_val += 1

                if inferred.get(i) != new_val:
                    inferred[i] = new_val
                    changed = True

            if not changed:
                break

        return inferred

    def solve(self):
        self.build_nodes()
        self.propagate()
        inferred = self.infer_blanks()

        final = []
        for i, val in enumerate(self.sequence):
            final.append(val if val is not None else inferred[i])

        return final, inferred


if __name__ == "__main__":
    user_input = input("Enter sequence with blanks as _: ")
    seq = []
    for x in user_input.split(','):
        x = x.strip()
        seq.append(None if x == "_" else int(x))

    reasoner = ConvergentGraphReasoner(seq)
    result, inferred = reasoner.solve()

    print("\n--- Final Reasoned Sequence ---")
    print("Reasoned sequence:", result)
    for idx in sorted(inferred):
        print(f"Blank B{idx} inferred as: {inferred[idx]}")
