# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 08:03:31 2017

@author: Owner
"""
from random import sample, choice
import os


class Cards:
    def __init__(self):
        self.TYPES = ("H", "D", "C", "S")
        self.MAXNUMBER = 13
        self.cards = [(t, i) for t in self.TYPES for i in range(1, self.MAXNUMBER+1)]

    def reset(self):
        self.cards = [(t, i) for t in self.TYPES for i in range(1, self.MAXNUMBER+1)]
        self.shuffle()

    def shuffle(self):
        self.cards = sample(self.cards, len(self.cards))

    def draw_a_card(self):
        index = choice(range(len(self.cards)))
        card = self.cards.pop(index)
        return card


class Player:
    def __init__(self, chip, name):
        self.name = name
        self.chip = chip
        self.bet = 0
        self.point = 0
        self.cards = []
        self.s = ""

        self.doflg = True
        self.bastflg = False
        self.playableflg = False

    def reset(self):
        self.point = 0
        self.bet = 0
        self.cards = []
        self.s = ""

        self.doflg = True
        self.bastflg = False

    # チップ 掛け金 関係
    def calc_chip(self, s="L"):
        if s == "W":
            self.chip += self.bet
        elif s == "L":
            self.chip -= self.bet

    def do_bet(self):
        while True:
            try:
                self.bet = int(input("賭け金を入力してください:"))
            except ValueError:
                print("入力が不正です。再入力をしてください。")
                continue
            if self.bet <= 0:
                print("自然数のみの入力です。再入力をしてください。")
                continue
            if self.bet > self.chip:
                print("賭け金が足りません。再入力をお願いします。")
                continue
            break

    def check_betable(self):
        return self.chip > 0

    # ポイント関係
    def calc_point(self):
        if not self.cards:
            self.point = 0
            return
        point = 0
        count = 0
        for card in self.cards:
            if card[1] == 1:
                count += 1
            elif card[1] < 10:
                point += card[1]
            else:
                point += 10

        if count:
            for i in range(count):
                if point <= 10:
                    point += 11
                else:
                    point += 1

        self.point = point

    # カード関係
    def draw_a_card(self, cards):
        self.cards.append(cards.draw_a_card())
        self.cards.sort()

    def draw_cards(self, cards, num):
        for i in range(num):
            self.draw_a_card(cards)

    def card2str(self, card):
        return "({0[0]},{0[1]:>2})".format(card)

    def print_cards(self):
        if not self.cards:
            print("None")
        else:
            for card in self.cards:
                print(self.card2str(card))

    # 続行可能かどうかの判定関係
    def check_playable(self):
        return self.check_betable()

    def check_bast(self):
        return self.point > 21

    # 選択関係
    def choice(self, cards):
        self.calc_point()
        if self.check_bast():
            print("残念初期の手札でBastしました。")
            self.doflg = False
            self.bastflg = True
            input("Enterキーを入力してください...")
            return
        self.print_blackjack()
        print("どれか選択してください。")
        print("0:Stand")
        print("1:Hit")
        print("2:Double")
        while True:
            n = input(">>")
            try:
                n = int(n)
            except ValueError:
                print("不正な入力です。再入力をしてください。")
                continue
            if not (n in range(3)):
                print("範囲内の数字を入力してください。")
                continue
            if n == 2 and not self.check_doubleablle():
                print("Doubleは選択できません。再入力をしてください。")
                continue
            break

        if n == 0:
            if self.check_blackjack():
                self.bet *= 2
            self.stand()
        elif n == 1:
            self.hit(cards)
        elif n == 2:
            self.double(cards)

        self.calc_point()
        if self.check_bast():
            print("Bastしました。")
            self.bastflg = True
            self.doflg = False
        self.print_player()
        input("続けるにはEnterキーを入力してください...")

    def stand(self):
        print("Standを選択しました。")
        print("この手札で勝負します。")
        self.doflg = False

    def hit(self, cards):
        print("Hitを選択しました。")
        print("カードを一枚引きます。")
        self.draw_a_card(cards)

    def check_doubleablle(self):
        if len(self.cards) != 2:
            return False
        return True

    def double(self, cards):
        """doubleが使えるというときのみ使うこと"""
        print("Doubleを選択しました。")
        print("3枚目のカードを引きます。")
        self.doflg = False
        self.draw_a_card(cards)
        self.bet *= 2

    def check_blackjack(self):
        self.calc_point()
        return len(self.cards) == 2 and self.point == 21

    # 表示関係
    def print_blackjack(self):
        if self.check_blackjack():
            print("ブラックジャックです。")
            print("負けることはありません。")
            print("最善手はStandです。")

    def print_player(self):
        self.calc_point()
        print(self.name + "の手札とその手札の得点です。")
        print("[{0}点]".format(self.point))
        self.print_cards()


class Dealer(Player):
    def __init__(self, chip, num):
        Player.__init__(self, num*chip, "ディーラー")

    # 賭け金 チップ関係
    def do_bet(self):
        self.bet = 0

    def add_chip(self, chip):
        self.chip += chip

    # 選択関係
    def choice(self, cards):
        if self.check_bast():
            self.bastflg = True
            return
        if self.point > 17:
            self.stand()
        else:
            self.hit(cards)
        self.calc_point()
        if self.check_bast():
            self.bastflg = True
            self.doflg = False


class Game:
    def __init__(self):
        print("このゲームはブラックジャックを簡単にしたゲームです。")
        print("誰かの掛け金がなくなるまでゲームは続きます。")
        print("がんばって21点に近づけて掛け金を回収してくださいね。")
        print("ルールの詳細は同フォルダ内のreadme.txtを読んでください。")
        print("では、ゲームを開始します。")

        num = self.input_number("遊ぶ人数を入力してください。")
        s = "全員に共通するチップの金額を入力してください。\nしかしディーラーはその"+str(num)+"倍です。"
        chip = self.input_number(s)
        print("開始する順番の通りに名前を入力してください。")
        self.players = [Player(chip, input(str(i+1) + "人目 名前:")) for i in range(num)]
        self.dealer = Dealer(chip, num)

        self.cards = Cards()
        self.continueflg = True

    def reset(self):
        for player in self.players:
            player.reset()
        self.dealer.reset()
        self.cards.reset()

    # 実行関係
    def loop(self):
        while self.continueflg:

            os.system("cls")
            # Betする
            print("各プレーヤーは掛け金を決めてください。")
            num = 0
            for player in self.players:
                print(player.name+"の所持金額は"+str(player.chip)+"円です。")
                player.do_bet()
                num = max([num, player.bet])
            self.dealer.do_bet()

            # トランプを配る
            for player in self.players:
                player.draw_cards(self.cards, 2)
            self.dealer.draw_a_card(self.cards)

            # 各プレイヤーは行動できなくなるまで行動する。
            for player in self.players:
                while player.doflg:
                    os.system("cls")
                    self.dealer.print_player()
                    print("-"*10)
                    player.print_player()
                    player.choice(self.cards)
                    print()

            # ディーラーの行動
            os.system("cls")
            print("ディーラの行動を開始します。")
            while self.dealer.doflg:
                self.dealer.choice(self.cards)
            input("ディーラーの手札などを確認するにはEnterキーを入力してください。")
            if self.dealer.check_bast():
                print("Bastしました。")
            self.dealer.print_player()
            input("続けるにはEnterキーを入力してください。")

            self.calc_points()

            # 勝敗判定
            self.continueflg = self.check_continue()
            os.system("cls")
            self.print_status()
            input("続けるにはEinterキーを入力してください...")

            self.reset()

        os.system("cls")
        print("勝負がつきました。")
        input("Enterキーを入力すると結果を表示します。")
        os.system("cls")
        self.print_finish()
        input("終了するにはEnterキーを入力してください...")

    # 勝敗関係
    def calc_points(self):
        for player in self.players:
                if player.bastflg:
                    player.s = "Bast "
                    if self.dealer.bastflg:
                        player.calc_chip("E")  # 引き分け
                        player.s += "DeerBast Even"
                        self.dealer.s = "Bast"
                    else:
                        player.calc_chip("L")  # プレーヤーの負け
                        self.dealer.add_chip(player.bet)
                        player.s += "Lose"
                else:
                    if self.dealer.bastflg:
                        player.calc_chip("W")  # プレーヤーの勝ち
                        self.dealer.add_chip(-player.bet)
                        player.s += "DearBast Win"
                    else:
                        if player.point < self.dealer.point:  # プレーヤーの負け
                            player.calc_chip("L")
                            self.dealer.add_chip(player.bet)
                            player.s = "Lose"
                        elif player.point > self.dealer.point:  # プレーヤーの勝ち
                            player.calc_chip("W")
                            self.dealer.add_chip(-player.bet)
                            player.s = "Win"
                        else:
                            player.calc_chip("E")  # 引き分け
                            player.s = "Even"

    # 入力関係
    def input_number(self, msg):
        print(msg)
        while True:
            n = input(">>")
            try:
                n = int(n)
            except ValueError:
                print("入力が不正です。再入力してください。")
                continue
            if n <= 0:
                print("自然数しか扱えません。再入力してください。")
                continue
            break
        return n

    # 続行可能判定フラグ関係
    def check_continue(self):
        flg = True
        for player in self.players:
            flg = flg and player.check_playable()
        flg = flg and self.dealer.check_playable()
        return flg

    # 表示関係
    def print_status(self):
        print("名前：チップ(円)")
        pairs = [(player.name, player.chip, player.s) for player in self.players]
        pairs.append((self.dealer.name, self.dealer.chip, self.dealer.s))
        for pair in pairs:
            print("{0[0]} : {0[1]}円 {0[2]}".format(pair))

    def print_finish(self):
        print("順位 名前：チップ(円)")
        pairs = [(player.name, player.chip) for player in self.players]
        pairs.append((self.dealer.name, self.dealer.chip))
        pairs.sort(key=lambda p: p[1], reverse=True)
        rank_pairs = []
        rank = 1
        for pair in pairs:
            if not rank_pairs:
                rank_pairs.append((rank, pair))
                rank += 1
            else:
                r, p = rank_pairs[-1]
                if pair[1] == p[1]:
                    rank_pairs.append((r, pair))
                else:
                    rank_pairs.append((rank, pair))
                    rank += 1

        for rank, pair in rank_pairs:
            s = "{0}位 {1[0]}:{1[1]}円".format(rank, pair)
            print(s)


if __name__ == "__main__":
    game = Game()
    game.loop()
