def get_game_setting():
    # スモールブラインドとビッグブラインドの額を取得
    small_blind = int(input("スモールブラインドを入力してください："))
    big_blind = int(input("ビッグブラインドを入力してください："))

    # プレイヤーの人数を取得
    num_players = int(input("プレイヤーの人数を入力してください："))

    players = {}    # プレイヤー情報を記録する

    # 各プレイヤーの情報を取得
    for i in range(num_players):
        name = input(f"プレイヤー{i+1}の名前：")
        stack = int(input(f"{name}の初期スタック："))
        players[name] + stack   # 辞書にプレイヤー情報を追加
