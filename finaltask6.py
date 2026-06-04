items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items, budget):
    sorted_items = sorted(
        items.items(),
        key=lambda item: item[1]["calories"] / item[1]["cost"],
        reverse=True,
    )

    selected_items = []
    total_cost = 0
    total_calories = 0

    for name, data in sorted_items:
        if total_cost + data["cost"] <= budget:
            selected_items.append(name)
            total_cost += data["cost"]
            total_calories += data["calories"]

    return selected_items, total_cost, total_calories


def dynamic_programming(items, budget):
    names = list(items.keys())
    rows = len(names) + 1
    cols = budget + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        name = names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]

        for current_budget in range(cols):
            if cost > current_budget:
                dp[i][current_budget] = dp[i - 1][current_budget]
            else:
                dp[i][current_budget] = max(
                    dp[i - 1][current_budget],
                    dp[i - 1][current_budget - cost] + calories,
                )

    selected_items = []
    current_budget = budget

    for i in range(len(names), 0, -1):
        if dp[i][current_budget] != dp[i - 1][current_budget]:
            name = names[i - 1]
            selected_items.append(name)
            current_budget -= items[name]["cost"]

    selected_items.reverse()
    total_cost = sum(items[name]["cost"] for name in selected_items)
    total_calories = dp[len(names)][budget]

    return selected_items, total_cost, total_calories


def print_result(title, result):
    selected_items, total_cost, total_calories = result

    print(title)
    print(f"Selected items: {selected_items}")
    print(f"Total cost: {total_cost}")
    print(f"Total calories: {total_calories}")
    print()


budget = 100

print_result("Greedy algorithm:", greedy_algorithm(items, budget))
print_result("Dynamic programming:", dynamic_programming(items, budget))
