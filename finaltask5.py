import argparse
import html
import uuid
from collections import deque
from pathlib import Path


class Node:
    def __init__(self, key, color="#87ceeb"):
        self.left = None
        self.right = None
        self.value = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_sample_tree():
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    root.right.right = Node(7)
    return root


def generate_color(step, total):
    if total <= 1:
        intensity = 255
    else:
        intensity = 45 + int(210 * step / (total - 1))

    return f"#{intensity:02x}{(95 + step * 19) % 256:02x}f0"


def dfs_iterative(root):
    if root is None:
        return []

    order = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_iterative(root):
    if root is None:
        return []

    order = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        order.append(node)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order


def reset_colors(root, color="#87ceeb"):
    for node in bfs_iterative(root):
        node.color = color


def apply_traversal_colors(order):
    total = len(order)

    for index, node in enumerate(order):
        node.color = generate_color(index, total)


def collect_tree_layout(node, positions, edges, x=0.0, y=0.0, layer=1):
    if node is None:
        return

    positions[node.id] = {
        "x": x,
        "y": y,
        "label": str(node.value),
        "color": node.color,
    }

    if node.left:
        left_x = x - 1 / 2**layer
        edges.append((node.id, node.left.id))
        collect_tree_layout(node.left, positions, edges, left_x, y + 1, layer + 1)

    if node.right:
        right_x = x + 1 / 2**layer
        edges.append((node.id, node.right.id))
        collect_tree_layout(node.right, positions, edges, right_x, y + 1, layer + 1)


def scale_positions(positions, width=900, height=600, padding=70):
    xs = [item["x"] for item in positions.values()]
    ys = [item["y"] for item in positions.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    for item in positions.values():
        item["sx"] = padding + (item["x"] - min_x) / (max_x - min_x or 1) * (
            width - 2 * padding
        )
        item["sy"] = padding + (item["y"] - min_y) / (max_y - min_y or 1) * (
            height - 2 * padding
        )


def write_tree_svg(root, output_path, title):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    width = 900
    height = 600
    positions = {}
    edges = []
    collect_tree_layout(root, positions, edges)
    scale_positions(positions, width, height)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="24" y="36" font-family="Arial" font-size="22" fill="#0f172a">{html.escape(title)}</text>',
    ]

    for parent_id, child_id in edges:
        parent = positions[parent_id]
        child = positions[child_id]
        lines.append(
            f'<line x1="{parent["sx"]:.2f}" y1="{parent["sy"]:.2f}" '
            f'x2="{child["sx"]:.2f}" y2="{child["sy"]:.2f}" '
            'stroke="#334155" stroke-width="2"/>'
        )

    for item in positions.values():
        lines.append(
            f'<circle cx="{item["sx"]:.2f}" cy="{item["sy"]:.2f}" r="30" '
            f'fill="{item["color"]}" stroke="#1e293b" stroke-width="2"/>'
        )
        lines.append(
            f'<text x="{item["sx"]:.2f}" y="{item["sy"] + 5:.2f}" '
            'text-anchor="middle" font-family="Arial" font-size="16" fill="#0f172a">'
            f'{html.escape(item["label"])}</text>'
        )

    lines.append("</svg>")
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def visualize_traversal(root, traversal_name, output_path):
    reset_colors(root)

    if traversal_name == "dfs":
        order = dfs_iterative(root)
        title = "DFS traversal"
    elif traversal_name == "bfs":
        order = bfs_iterative(root)
        title = "BFS traversal"
    else:
        raise ValueError("Traversal must be 'dfs' or 'bfs'")

    apply_traversal_colors(order)
    path = write_tree_svg(root, output_path, title)

    return [node.value for node in order], path


parser = argparse.ArgumentParser(description="Visualize iterative DFS and BFS traversals.")
parser.parse_args()

sample_tree = build_sample_tree()

dfs_order, dfs_path = visualize_traversal(
    sample_tree,
    "dfs",
    "artifacts/dfs_traversal.svg",
)
print(f"DFS order: {dfs_order}")
print(f"DFS visualization saved to {dfs_path}")

bfs_order, bfs_path = visualize_traversal(
    sample_tree,
    "bfs",
    "artifacts/bfs_traversal.svg",
)
print(f"BFS order: {bfs_order}")
print(f"BFS visualization saved to {bfs_path}")
