import argparse
import math
from pathlib import Path


def collect_pythagoras_segments(segments, x, y, length, angle, level):
    if level == 0:
        return

    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)
    segments.append((x, y, x2, y2, level))

    next_length = length * math.sqrt(2) / 2
    collect_pythagoras_segments(
        segments,
        x2,
        y2,
        next_length,
        angle + math.pi / 4,
        level - 1,
    )
    collect_pythagoras_segments(
        segments,
        x2,
        y2,
        next_length,
        angle - math.pi / 4,
        level - 1,
    )


def normalize_segments(segments, width=900, height=900, padding=60):
    xs = []
    ys = []

    for x1, y1, x2, y2, _ in segments:
        xs.extend([x1, x2])
        ys.extend([y1, y2])

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    scale_x = (width - 2 * padding) / (max_x - min_x or 1)
    scale_y = (height - 2 * padding) / (max_y - min_y or 1)
    scale = min(scale_x, scale_y)

    normalized = []
    for x1, y1, x2, y2, level in segments:
        sx1 = padding + (x1 - min_x) * scale
        sy1 = height - padding - (y1 - min_y) * scale
        sx2 = padding + (x2 - min_x) * scale
        sy2 = height - padding - (y2 - min_y) * scale
        normalized.append((sx1, sy1, sx2, sy2, level))

    return normalized


def create_svg(segments, level, width=900, height=900):
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="24" y="36" font-family="Arial" font-size="22" fill="#0f172a">'
        f'Pythagoras tree, recursion level {level}</text>',
    ]

    for x1, y1, x2, y2, current_level in segments:
        stroke_width = max(1, current_level * 1.4)
        green = 80 + current_level * 12
        color = f"#{34:02x}{min(green, 180):02x}{78:02x}"
        lines.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{stroke_width:.2f}" stroke-linecap="round"/>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


def create_pythagoras_tree(level, output_path="artifacts/pythagoras_tree.svg"):
    if level < 0:
        raise ValueError("Recursion level must be non-negative")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    segments = []
    collect_pythagoras_segments(segments, 0, 0, 100, math.pi / 2, level)
    normalized = normalize_segments(segments) if segments else []
    output.write_text(create_svg(normalized, level), encoding="utf-8")

    return output


parser = argparse.ArgumentParser(description="Draw Pythagoras tree fractal.")
parser.add_argument("--level", type=int, default=8, help="recursion level")
parser.add_argument("--output", default="artifacts/pythagoras_tree.svg")
args = parser.parse_args()

path = create_pythagoras_tree(args.level, args.output)
print(f"Pythagoras tree saved to {path}")
