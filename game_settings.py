def get_blinds():
    while True:
        try:
            small_blind = int(input("スモールブラインドを入力してください："))
            big_blind = int(input("ビッグブラインドを入力してください："))
            if small_blind <= 0 or big_blind <= 0:
                raise ValueError("ブラインドは正の整数である必要があります。")
            if small_blind >= big_blind:
                raise ValueError("スモールブラインドはビッグブラインドより小さい必要があります。")
            return small_blind, big_blind
        except ValueError as e:
            print(f"入力エラー: {e}")

def get_num_players():
    while True:
        try:
            num_players = int(input("プレイヤーの人数を入力してください（2〜9）："))
            if num_players < 2 or num_players > 9:
                raise ValueError("プレイヤーは2人以上9人以下である必要があります。")
            return num_players
        except ValueError as e:
            print(f"入力エラー: {e}")

def get_players(num_players):
    players = []
    for i in range(num_players):
        while True:
            name = input(f"プレイヤー {i+1} の名前を入力してください：").strip()
            if not name:
                print("名前を入力してください。")
                continue
            if any(player['name'] == name for player in players):
                print("同じ名前のプレイヤーがすでにいます。別の名前を入力してください。")
                continue
            break
        
        while True:
            try:
                stack = int(input(f"{name} の初期スタックを入力してください："))
                if stack <= 0:
                    raise ValueError("スタックは正の整数である必要があります。")
                break
            except ValueError as e:
                print(f"入力エラー: {e}")
        
        players.append({"name": name, "stack": stack})
    
    return players

def assign_positions(players):
    num_players = len(players)
    position_templates = {
        2: ["SB", "BB"],
        3: ["BTN", "SB", "BB"],
        4: ["BTN", "SB", "BB", "UTG"],
        5: ["BTN", "SB", "BB", "UTG", "CO"],
        6: ["BTN", "SB", "BB", "UTG", "HJ", "CO"],
        7: ["BTN", "SB", "BB", "UTG", "MP", "HJ", "CO"],
        8: ["BTN", "SB", "BB", "UTG", "MP1", "MP2", "HJ", "CO"],
        9: ["BTN", "SB", "BB", "UTG", "UTG+1", "MP1", "MP2", "HJ", "CO"]
    }
    
    positions = position_templates[num_players]
    player_positions = {}
    
    print("各プレイヤーのポジションを選択してください。")
    available_positions = positions[:]
    
    for player in players:
        while True:
            print("利用可能なポジション:", ", ".join(f"{i}: {pos}" for i, pos in enumerate(available_positions)))
            try:
                pos_index = int(input(f"{player['name']} のポジション番号を選んでください："))
                if pos_index < 0 or pos_index >= len(available_positions):
                    raise ValueError("無効な番号です。")
                break
            except ValueError as e:
                print(f"入力エラー: {e}")
        
        player_positions[player['name']] = available_positions.pop(pos_index)
    
    sorted_positions = sorted(player_positions.items(), key=lambda x: positions.index(x[1]))
    return dict(sorted_positions)

if __name__ == "__main__":
    small_blind, big_blind = get_blinds()
    num_players = get_num_players()
    players = get_players(num_players)
    player_positions = assign_positions(players)
    
    print("スモールブラインド：", small_blind)
    print("ビッグブラインド：", big_blind)
    print("プレイヤー情報：", players)
    print("ポジション情報：", player_positions)
