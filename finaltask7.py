import argparse
import random
from pathlib import Path

ANALYTICAL_PROBABILITIES = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


def simulate_dice_rolls(sample_amount):
    counts = {total: 0 for total in range(2, 13)}

    for _ in range(sample_amount):
        first = random.randint(1, 6)
        second = random.randint(1, 6)
        counts[first + second] += 1

    return counts


def calculate_probabilities(counts):
    total_rolls = sum(counts.values())

    return {
        total: count / total_rolls
        for total, count in counts.items()
    }


def build_comparison_rows(probabilities):
    rows = []

    for total in range(2, 13):
        monte_carlo = probabilities[total]
        analytical = ANALYTICAL_PROBABILITIES[total]
        difference = abs(monte_carlo - analytical)

        rows.append(
            {
                "sum": total,
                "monte_carlo": monte_carlo,
                "analytical": analytical,
                "difference": difference,
            }
        )

    return rows


def print_comparison_table(rows):
    print("Sum | Monte Carlo | Analytical | Difference")
    print("----|-------------|------------|-----------")

    for row in rows:
        print(
            f"{row['sum']:>3} | "
            f"{row['monte_carlo'] * 100:>10.2f}% | "
            f"{row['analytical'] * 100:>9.2f}% | "
            f"{row['difference'] * 100:>8.2f}%"
        )


def save_probability_chart(rows, output_path="artifacts/monte_carlo_dice.svg"):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    width = 1000
    height = 620
    margin_left = 70
    margin_bottom = 80
    chart_top = 70
    chart_height = height - chart_top - margin_bottom
    chart_width = width - margin_left - 40
    group_width = chart_width / len(rows)
    bar_width = group_width * 0.32
    max_percent = 18

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="24" y="36" font-family="Arial" font-size="22" fill="#0f172a">'
        "Probabilities of sums for two dice</text>",
        f'<line x1="{margin_left}" y1="{chart_top + chart_height}" '
        f'x2="{margin_left + chart_width}" y2="{chart_top + chart_height}" '
        'stroke="#334155" stroke-width="2"/>',
        f'<line x1="{margin_left}" y1="{chart_top}" x2="{margin_left}" '
        f'y2="{chart_top + chart_height}" stroke="#334155" stroke-width="2"/>',
    ]

    for percent in range(0, max_percent + 1, 3):
        y = chart_top + chart_height - percent / max_percent * chart_height
        lines.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" '
            f'x2="{margin_left + chart_width}" y2="{y:.2f}" '
            'stroke="#cbd5e1" stroke-width="1"/>'
        )
        lines.append(
            f'<text x="{margin_left - 12}" y="{y + 4:.2f}" text-anchor="end" '
            'font-family="Arial" font-size="12" fill="#475569">'
            f"{percent}%</text>"
        )

    for index, row in enumerate(rows):
        group_x = margin_left + index * group_width + group_width * 0.18
        monte_height = row["monte_carlo"] * 100 / max_percent * chart_height
        analytical_height = row["analytical"] * 100 / max_percent * chart_height
        baseline = chart_top + chart_height

        lines.append(
            f'<rect x="{group_x:.2f}" y="{baseline - monte_height:.2f}" '
            f'width="{bar_width:.2f}" height="{monte_height:.2f}" fill="#3b82f6"/>'
        )
        lines.append(
            f'<rect x="{group_x + bar_width:.2f}" y="{baseline - analytical_height:.2f}" '
            f'width="{bar_width:.2f}" height="{analytical_height:.2f}" fill="#f59e0b"/>'
        )
        lines.append(
            f'<text x="{group_x + bar_width:.2f}" y="{baseline + 24:.2f}" '
            'text-anchor="middle" font-family="Arial" font-size="13" fill="#0f172a">'
            f'{row["sum"]}</text>'
        )

    lines.extend(
        [
            '<rect x="760" y="22" width="16" height="16" fill="#3b82f6"/>',
            '<text x="784" y="36" font-family="Arial" font-size="14" fill="#0f172a">Monte Carlo</text>',
            '<rect x="880" y="22" width="16" height="16" fill="#f59e0b"/>',
            '<text x="904" y="36" font-family="Arial" font-size="14" fill="#0f172a">Analytical</text>',
            "</svg>",
        ]
    )

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def monte_carlo(sample_amount=1_000_000, output_path="artifacts/monte_carlo_dice.svg"):
    counts = simulate_dice_rolls(sample_amount)
    probabilities = calculate_probabilities(counts)
    rows = build_comparison_rows(probabilities)
    chart_path = save_probability_chart(rows, output_path)

    return counts, rows, chart_path


parser = argparse.ArgumentParser(description="Monte Carlo simulation for two dice.")
parser.add_argument("--samples", type=int, default=1_000_000)
parser.add_argument("--output", default="artifacts/monte_carlo_dice.svg")
args = parser.parse_args()

counts, comparison_rows, path = monte_carlo(args.samples, args.output)

print(f"Samples: {args.samples}")
print_comparison_table(comparison_rows)
print(f"Chart saved to {path}")
