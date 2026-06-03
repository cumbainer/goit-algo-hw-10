def find_coins_greedy(coins, change: int) -> dict[int, int]:
    out = {}

    for coin in sorted(coins, reverse=True):
        while change >= coin:
            out[coin] = out.get(coin, 0) + 1
            change -= coin

    return out


def find_coins_dynamic_programming(coins, change:int) -> dict[int, int]:
    dp: list[dict[int, int] | None] = [None] * (change + 1)
    dp[0] = {}

    for amount in range(1, change + 1):
        best = None

        for coin in coins:
            if amount >= coin and dp[amount - coin] is not None:
                candidate = dp[amount - coin].copy()
                candidate[coin] = candidate.get(coin, 0) + 1

                if best is None or sum(candidate.values()) < sum(best.values()):
                    best = candidate

        dp[amount] = best

    if dp[change] is None:
        return {}

    return dp[change]



param_coins = [25, 25, 5, 3, 1]
change = 69
print(find_coins_dynamic_programming(param_coins, change))