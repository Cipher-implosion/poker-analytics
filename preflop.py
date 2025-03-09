def preflop_action(players, player_positions, small_blind, big_blind):
    action_order = []
    bb_position = None
    
    sorted_positions = [pos for pos in ["UTG", "UTG+1", "MP1", "MP2", "HJ", "CO", "BTN", "SB", "BB"] if pos in player_positions.values()]
    for pos in sorted_positions:
        for name, position in player_positions.items():
            if position == pos:
                if position == "BB":
                    bb_position = len(action_order)
                action_order.append(name)
    
    print("アクション順序:", action_order)
    
    current_bet = big_blind
    min_raise = big_blind
    player_bets = {name: 0 for name in action_order}
    player_stacks = {player["name"]: player["stack"] for player in players}
    active_players = set(action_order)
    all_in_players = []
    last_raiser = None
    has_raise_right = True  

    for name, position in player_positions.items():
        if position == "SB":
            player_bets[name] = small_blind
            player_stacks[name] -= small_blind
        elif position == "BB":
            player_bets[name] = big_blind
            player_stacks[name] -= big_blind

    display_pot_info(player_bets, player_stacks)  # 初期ポット表示
    
    while True:
        all_called = True
        
        for player in action_order:
            if player not in active_players:
                continue
            
            if last_raiser and player == last_raiser:
                print("プリフロップ終了")
                return process_pots(player_bets, player_stacks, active_players, all_in_players)
            
            while True:
                available_actions = ["F"]
                call_amount = current_bet - player_bets[player]
                
                if player_bets[player] < current_bet:
                    if player_stacks[player] >= call_amount:
                        available_actions.append("C")
                    else:
                        available_actions.append("A")  
                else:
                    available_actions.append("K")  
                
                if has_raise_right and player_stacks[player] >= (current_bet + min_raise):
                    available_actions.append("R")
                
                if player_stacks[player] > 0:
                    available_actions.append("A")  
                
                print(f"{player} のアクション {available_actions} (現在のベット額: {current_bet})")
                action = input().strip().upper()
                
                if action not in available_actions:
                    print("無効な選択です。もう一度選んでください。")
                    continue
                
                if action == "F":
                    active_players.remove(player)
                    print(f"{player} はフォールドしました。")
                elif action == "C":
                    player_bets[player] += call_amount
                    player_stacks[player] -= call_amount
                    print(f"{player} はコールしました ({call_amount})。")
                elif action == "K":
                    print(f"{player} はチェックしました。")
                elif action == "R":
                    while True:
                        try:
                            raise_amount = int(input("レイズ額を入力してください: "))
                            if raise_amount < current_bet + min_raise or raise_amount > player_stacks[player]:
                                raise ValueError(f"無効なレイズ額です。最低 {current_bet + min_raise} 以上、最大 {player_stacks[player]} までです。")
                            
                            min_raise = raise_amount - current_bet
                            current_bet = raise_amount
                            player_bets[player] = raise_amount
                            player_stacks[player] -= raise_amount
                            last_raiser = player
                            has_raise_right = True  
                            print(f"{player} は {raise_amount} にレイズしました。")
                            all_called = False
                            break
                        except ValueError as e:
                            print(f"入力エラー: {e}")
                elif action == "A":
                    all_in_amount = player_stacks[player] + player_bets[player] 
                    player_bets[player] = all_in_amount
                    player_stacks[player] = 0
                    all_in_players.append((player, all_in_amount))
                    if all_in_amount > current_bet:
                        current_bet = all_in_amount
                        last_raiser = player
                    print(f"{player} はオールインしました ({all_in_amount})。")
                    all_called = False
                
                display_pot_info(player_bets, player_stacks)  # アクション後にポット情報を表示
                break  
        
        if all_called or len(active_players) == 1:
            print("プリフロップ終了")
            return process_pots(player_bets, player_stacks, active_players, all_in_players)


def display_pot_info(player_bets, player_stacks):
    """ 現在の状況を表示する """
    print("\n=== 現在のポット情報 ===")
    total_pot = sum(player_bets.values())
    print(f"ポットサイズ: {total_pot}")
    for player, bet in player_bets.items():
        print(f"{player}: ベット額 {bet}, 残りスタック {player_stacks[player]}")
    print("======================\n")


def process_pots(player_bets, player_stacks, active_players, all_in_players):
    """ サイドポットとメインポットを作成する """
    
    # プレイヤーが1人だけなら、そのプレイヤーが勝ち
    if len(active_players) == 1:
        winner = next(iter(active_players))  # 唯一のプレイヤーを取得
        total_pot = sum(player_bets.values())  # ポットの合計
        player_stacks[winner] += total_pot  # 勝者がポットを獲得
        
        print("\n=== プリフロップ終了 ===")
        print(f"{winner} が最後のプレイヤーとして勝ちました！")
        print(f"獲得ポット: {total_pot}")
        print("========================\n")

        return player_bets, player_stacks, total_pot, active_players
    
    # サイドポットの処理
    pot_list = []
    sorted_all_in = sorted(all_in_players, key=lambda x: x[1])  
    previous_all_in_amount = 0

    for i, (all_in_player, all_in_amount) in enumerate(sorted_all_in):
        pot_size = 0
        eligible_players = set(active_players)  

        for player in active_players:
            contribution = min(all_in_amount - previous_all_in_amount, player_bets[player])
            pot_size += contribution
            player_bets[player] -= contribution
        
        pot_list.append((pot_size, eligible_players))
        previous_all_in_amount = all_in_amount

    remaining_pot = sum(player_bets.values())
    if remaining_pot > 0:
        pot_list.append((remaining_pot, active_players))

    for player in player_bets:
        player_bets[player] = 0

    # 確定したポット情報を表示
    print("\n=== 確定したポット情報 ===")
    for i, (pot_size, players) in enumerate(pot_list):
        print(f"ポット {i+1}: {pot_size} (参加プレイヤー: {', '.join(players)})")
    print("========================\n")

    return player_bets, player_stacks, sum(pot_size for pot_size, _ in pot_list), active_players