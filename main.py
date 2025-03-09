from game_settings import get_blinds, get_num_players, get_players, assign_positions
from preflop import preflop_action

def main():
    small_blind, big_blind = get_blinds()
    num_players = get_num_players()  # ここで人数を取得
    players = get_players(num_players)  # num_players を渡す
    player_positions = assign_positions(players)

    print("スモールブラインド:", small_blind)
    print("ビッグブラインド:", big_blind)
    print("プレイヤー情報:", players)
    print("ポジション情報:", player_positions)
    
     # プリフロップの処理を実行
    preflop_bets = preflop_action(players, player_positions, small_blind, big_blind)
    print("プリフロップのベット情報:", preflop_bets)


if __name__ == "__main__":
    main()