import argparse
import heapq
import html
import uuid
from pathlib import Path


class Node:
    def __init__(self, key, color="#87ceeb"):
        self.left = None
        self.right = None
        self.value = key
        self.color = color
        self.id = str(uuid.uuid4())


def heap_to_tree(heap):
    if not heap:
        return None

    nodes = [Node(value) for value in heap]

    for index, node in enumerate(nodes):
        left_index = 2 * index + 1
        right_index = 2 * index + 2

        if left_index < len(nodes):
            node.left = nodes[left_index]
        if right_index < len(nodes):
            node.right = nodes[right_index]

    return nodes[0]


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
    if root is None:
        raise ValueError("Heap is empty")

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
            f'<circle cx="{item["sx"]:.2f}" cy="{item["sy"]:.2f}" r="28" '
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


def visualize_heap(values, output_path="artifacts/binary_heap.svg"):
    heap = values[:]
    heapq.heapify(heap)
    root = heap_to_tree(heap)
    return write_tree_svg(root, output_path, f"Binary min-heap: {heap}")


parser = argparse.ArgumentParser(description="Visualize binary heap as binary tree.")
parser.add_argument(
    "--values",
    nargs="+",
    type=int,
    default=[12, 5, 7, 3, 9, 1, 4, 8, 6],
)
parser.add_argument("--output", default="artifacts/binary_heap.svg")
args = parser.parse_args()

path = visualize_heap(args.values, args.output)
print(f"Binary heap visualization saved to {path}")
