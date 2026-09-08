"""Coherent conditional path DAG, exact multiplicity, and resumable custody."""
from collections import defaultdict
from pathlib import Path
import hashlib
from .compiler import observation_key
from .exact import canonical, digest


def implementation_binding():
    root = Path(__file__).parent
    names = ('contracts.py', 'exact.py', 'compiler.py', 'native.py', 'inverse.py',
             'dependencies/native/t18.py', 'dependencies/common_reception.py')
    return digest({name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names})


class JointAnswer:
    @classmethod
    def start(cls, block, observations, directions, initial_states, view):
        obj = cls()
        obj.block = block
        obj.view = view
        obj.observations = tuple(observation_key(v, view) for v in observations)
        if not obj.observations:
            raise ValueError('At least one observation position is required')
        width = len(next(iter(block.keys(view).values())))
        if any(v is not None and len(v) != width for v in obj.observations):
            raise ValueError('Observation width disagrees with receiver contract')
        n = len(obj.observations) - 1
        obj.directions = (None,) * n if directions is None else tuple(directions)
        if len(obj.directions) != n or any(d is not None and (type(d) is not int or d not in (-1, 1)) for d in obj.directions):
            raise ValueError('Supply one signed direction or None per event')
        roots = block.states if initial_states is None else tuple(block.contract.admit_state(q) for q in initial_states)
        if any(q not in block.state_set for q in roots):
            raise ValueError('Initial state outside declared domain')
        roots = tuple(sorted(set(roots)))
        obj.known_initial_states = None if initial_states is None else roots
        obj.nodes = []  # (time, root, current, accumulated barrier)
        obj.edges = []  # (source node, target node, event label)
        obj.frontier = []
        for q in roots:
            if obj.observations[0] is None or block.observe(q, view) == obj.observations[0]:
                obj.frontier.append(len(obj.nodes))
                obj.nodes.append((0, q, q, None if block.contacts[q] is None else 0))
        obj.processed_steps = 0
        obj.expansions = 0
        obj.lookup_count = 0
        return obj

    def advance(self, max_steps=None):
        if max_steps is not None and (type(max_steps) is not int or max_steps < 0):
            raise ValueError('max_steps must be a nonnegative integer')
        end = len(self.directions) if max_steps is None else min(len(self.directions), self.processed_steps + max_steps)
        keys = self.block.keys(self.view)
        for position in range(self.processed_steps, end):
            before, after = self.observations[position:position + 2]
            direction = self.directions[position]
            by_source = None
            if before is not None and after is not None:
                rows = self.block.transition_index(self.view, direction is not None).get((direction, before, after), ())
                by_source = defaultdict(list)
                for row in rows:
                    by_source[row[0]].append(row)
                self.lookup_count += 1
            following = {}
            for parent in self.frontier:
                _, root, q, barrier = self.nodes[parent]
                rows = self.block.outgoing[q] if by_source is None else by_source.get(q, ())
                for _, label, target, d in rows:
                    self.expansions += 1
                    if direction is not None and direction != d:
                        continue
                    if after is not None and keys[target] != after:
                        continue
                    b = None if barrier is None else max(barrier, self.block.contacts[target] - self.block.contacts[root])
                    joint = (root, target, b)
                    if joint not in following:
                        following[joint] = len(self.nodes)
                        self.nodes.append((position + 1, root, target, b))
                    self.edges.append((parent, following[joint], label))
            self.frontier = list(following.values())
            self.processed_steps += 1
        return self

    @property
    def complete(self):
        return self.processed_steps == len(self.directions)

    def _path_counts(self):
        counts = {i: 1 for i, row in enumerate(self.nodes) if row[0] == 0}
        for source, target, _ in self.edges:
            counts[target] = counts.get(target, 0) + counts[source]
        return counts

    @property
    def path_count(self):
        counts = self._path_counts()
        return sum(counts[n] for n in self.frontier)

    def iter_paths(self, limit=None):
        """Iterate admitted histories without expanding their Cartesian marginals."""
        if limit is not None and (type(limit) is not int or limit < 0):
            raise ValueError('Path iterator limit must be nonnegative')
        predecessors = defaultdict(list)
        for source, target, label in self.edges:
            predecessors[target].append((source, label))
        emitted = 0
        # Iterative reverse DFS supports streams well beyond Python recursion depth.
        for leaf in self.frontier:
            stack = [(leaf, 0)]
            path_nodes = [leaf]
            path_labels = []
            while stack:
                node, choice = stack[-1]
                if self.nodes[node][0] == 0:
                    if limit is not None and emitted >= limit:
                        return
                    root = self.nodes[node][1]
                    states = [self.nodes[i][2] for i in reversed(path_nodes)]
                    yield canonical({'initial': root, 'program': list(reversed(path_labels)),
                                     'states': states, 'barrier': self.nodes[leaf][3],
                                     'contact_profile': [self.block.contacts[q] for q in states]})
                    emitted += 1
                    stack.pop(); path_nodes.pop()
                    if path_labels:
                        path_labels.pop()
                elif choice < len(predecessors[node]):
                    parent, label = predecessors[node][choice]
                    stack[-1] = (node, choice + 1)
                    stack.append((parent, 0)); path_nodes.append(parent); path_labels.append(label)
                else:
                    stack.pop(); path_nodes.pop()
                    if path_labels:
                        path_labels.pop()

    def _live(self):
        live = set(self.frontier)
        for source, target, _ in reversed(self.edges):
            if target in live:
                live.add(source)
        return live

    def program_projection(self, limit=4096):
        live = self._live()
        labels = defaultdict(set)
        for source, target, label in self.edges:
            if target in live:
                labels[self.nodes[source][0]].add(label)
        if self.frontier and all(len(labels[i]) == 1 for i in range(self.processed_steps)):
            word = [next(iter(labels[i])) for i in range(self.processed_steps)]
            return {'complete': True, 'count': 1, 'programs': [word]}
        if self.path_count <= limit:
            words = sorted({tuple(p['program']) for p in self.iter_paths()})
            return {'complete': True, 'count': len(words), 'programs': [list(w) for w in words]}
        return {'complete': False, 'count': None, 'programs': None,
                'reason': 'Program projection remains represented by the complete labeled DAG; explicit expansion exceeds projection limit'}

    def to_dict(self, include_graph=False, projection_limit=4096):
        paths = self.path_count
        projection = self.program_projection(projection_limit)
        live = self._live()
        out = {'schema': 'SLC_GEN2_JOINT_ANSWER_V1', 'contract_id': self.block.contract_id,
               'complete': self.complete, 'extent': {'processed_steps': self.processed_steps, 'requested_steps': len(self.directions)},
               'status': 'COMPLETE' if self.complete else 'WORK_LIMITED_PREFIX',
               'fiber_status': ('EMPTY' if paths == 0 else 'UNIQUE' if paths == 1 else 'MULTIPLE') if self.complete else 'UNFINISHED',
               'path_count': paths, 'path_count_scope': 'complete_fiber' if self.complete else 'processed_prefix',
               'program_projection': projection,
               'root_state_barrier': sorted({(self.nodes[n][1], self.nodes[n][2], self.nodes[n][3]) for n in self.frontier}),
               'graph': {'vertices': len(self.nodes), 'edges': len(self.edges), 'live_vertices': len(live)},
               'cost': {'transition_expansions': self.expansions, 'local_lookups': self.lookup_count},
               'view': self.view,
               'information': {'directions': self.directions, 'initial_states': self.known_initial_states,
                               'receipt_supplied': False},
               'unresolved': ([] if self.complete else ['unprocessed observations']) + ([] if paths <= 1 else ['joint alternatives retained'])}
        if include_graph:
            out.update(nodes=self.nodes, edges=self.edges, frontier=self.frontier)
        return canonical(out)

    def checkpoint(self):
        body = canonical({'schema': 'SLC_GEN2_DAG_CHECKPOINT_V1', 'contract': self.block.contract.to_dict(),
                          'implementation_binding': implementation_binding(), 'view': self.view,
                          'observations': self.observations, 'directions': self.directions,
                          'known_initial_states': self.known_initial_states,
                          'nodes': self.nodes, 'edges': self.edges, 'frontier': self.frontier,
                          'processed_steps': self.processed_steps, 'expansions': self.expansions,
                          'lookup_count': self.lookup_count})
        return {'body': body, 'sha256': digest(body)}

    @classmethod
    def restore(cls, block, checkpoint):
        body = checkpoint['body']
        if checkpoint['sha256'] != digest(body):
            raise ValueError('Checkpoint payload digest mismatch')
        if body['schema'] != 'SLC_GEN2_DAG_CHECKPOINT_V1' or body['implementation_binding'] != implementation_binding():
            raise ValueError('Checkpoint code/schema binding mismatch')
        if body['contract'] != block.contract.to_dict():
            raise ValueError('Checkpoint mathematical contract mismatch')
        obj = cls.start(block, body['observations'], body['directions'], body['known_initial_states'], body['view'])
        obj.nodes = [(time, tuple(root), tuple(q), barrier) for time, root, q, barrier in body['nodes']]
        obj.edges = [tuple(e) for e in body['edges']]
        obj.frontier = list(body['frontier'])
        obj.processed_steps = body['processed_steps']
        obj.expansions = body['expansions']; obj.lookup_count = body['lookup_count']
        if not 0 <= obj.processed_steps <= len(obj.directions):
            raise ValueError('Invalid checkpoint input cursor')
        for source, target, label in obj.edges:
            if not 0 <= source < target < len(obj.nodes):
                raise ValueError('Invalid checkpoint DAG edge')
            t, root, q, b = obj.nodes[source]
            t1, root1, q1, b1 = obj.nodes[target]
            expected_b = None if b is None else max(b, block.contacts[q1] - block.contacts[root])
            if t1 != t + 1 or root1 != root or block.forward(q, label) != q1 or expected_b != b1:
                raise ValueError('Checkpoint loses a source/path/readout association')
        if any(obj.nodes[n][0] != obj.processed_steps for n in obj.frontier):
            raise ValueError('Checkpoint frontier does not match its input cursor')
        return obj
