from preflop import preflop_action

def get_players(num_players):
    default_players = [
        {'name': 'Alice', 'stack': 5000},
        {'name': 'Bob', 'stack': 7000},
        {'name': 'Charlie', 'stack': 10000},
        {'name': 'David', 'stack': 8000},
        {'name': 'Eve', 'stack': 12000},
        {'name': 'Frank', 'stack': 9000},
        {'name': 'Grace', 'stack': 15000},
        {'name': 'Hank', 'stack': 11000},
        {'name': 'Ivy', 'stack': 13000}
    ]
    return default_players[:num_players]


def assign_positions(players):
    positions = ['SB', 'BB'] + ['UTG', 'MP', 'CO', 'BTN'][:len(players)-2]
    return {player['name']: pos for player, pos in zip(players, positions)}


def main():
    num_players = int(input("プレイヤー数を入力してください（2〜9）: "))
    players = get_players(num_players)
    positions = assign_positions(players)
    sb = 100
    bb = 300
    
    preflop_bets = preflop_action(players, positions, sb, bb)
    print("プリフロップのベット情報:", preflop_bets)


if __name__ == "__main__":
    main()
