# 利用するライブラリをインポートする
from ctypes.wintypes import BOOLEAN
import sys
from tkinter import HORIZONTAL, LEFT, END, TOP, Button, Frame,  PhotoImage, Text, Tk
from tkinter.messagebox import showinfo, showerror
from functools import partial
from Unit.unit import StateFrame, UnitFrame
from const import Const
from random import randrange


class Application(Frame):
	'''
	GUI構成
	'''
	# エラータイトル
	ERR_TITLE: str = "ユニットネーム 未入力"
	# 未入力の文言
	ERR_MESSAGE: str = "の名前を入力してください。"
	# プレイヤー
	PRAYER: str = "プレイヤー"
	# エネミー
	ENEMY: str = "エネミー"
	# 勝ち
	WIN: str = "の勝ち!"
	# ボタンの横幅
	BTN_WIDTH: int = 15
	# 改行
	NEW_LINE: str = "\n"
	# じゃんけん
	JANKEN: dict = {"グー": 0, "チョキ": 1, "パー": 2}
	# じゃんけんランダム数値用の値
	JANKEN_NAM: int = 3

	def __init__(self, root: Frame):
		'''
		初期設定
		'''
		# 継承元であるFrameへ設定を渡す
		super().__init__(root, borderwidth=0, relief='groove')
		# 他の関数で使用できる様にする
		self.root = root
		# GUI上のタイトルを設定
		self.root.title("Janken Game")
		# GUIのアイコンを設定する
		self.root.iconphoto(False, PhotoImage(file='src/file/janken.png'))
		# メインとなるGUIを配置する
		self.pack()

		# グーボタンのアイコンを設定する
		self.rock_img: PhotoImage = PhotoImage(
			file="src/file/janken_rock.png").subsample(3, 3)
		# チョキボタンのアイコンを設定する
		self.scissors_img: PhotoImage = PhotoImage(
			file="src/file/janken_scissors.png").subsample(3, 3)
		# パーボタンのアイコンを設定する
		self.paper_img: PhotoImage = PhotoImage(
			file="src/file/janken_paper.png").subsample(3, 3)

		# メインとなるGUIの上にアイテムを表示していく
		self.__create_wigets()

	def __create_wigets(self):
		'''
		GUIの構成を行う
		'''
		# Enemy側のユニット名入力欄を組み立てていく
		self.enemy_unit: UnitFrame = UnitFrame(root=self, text="Enemy Name")
		# Enemy側のユニットの勝利回数表示を組み立てていく
		self.enemy_state: StateFrame = StateFrame(root=self)

		# ログ表示用のTextを用意する
		self.log_message: Text = Text(self, state=Const.NORMAL)
		self.log_message.pack()
		# ログを表示できる様にする
		self.print: partial = partial(self.log_message.insert, END)

		# プレイヤーのじゃんけんの手用のボタンを組み立てていく
		# Prayer側のユニット名入力欄を組み立てていく
		self.prayer_unit: UnitFrame = UnitFrame(root=self, text="Prayer Name")
		# Prayer側のユニットの勝利回数表示を組み立てていく
		self.prayer_state: StateFrame = StateFrame(root=self)

		# ゲームの進行を管理するボタンを組み立てていく
		# ボタンを配置するフレームを用意する
		menu_frame: Frame = Frame(self)
		# フレームを配置する
		menu_frame.pack()
		# ゲーム開始ボタンを用意する
		self.start: Button = Button(
			menu_frame, text="Start", width=self.BTN_WIDTH, state=Const.NORMAL)
		# ボタンを押した際に、動作させたい関数を指定する
		self.start.bind("<ButtonPress>", self.__start)
		# ゲーム再スタートボタンを用意する
		self.restart: Button = Button(
			menu_frame, text="ReStart", width=self.BTN_WIDTH, state=Const.DISABLED)
		# ボタンを押した際に、動作させたい関数を指定する
		self.restart.bind("<ButtonPress>", self.__restart)
		# ゲーム終了ボタンを用意する
		self.end: Button = Button(menu_frame, text="End",
		                          width=self.BTN_WIDTH, state=Const.DISABLED)
		# ボタンを押した際に、動作させたい関数を指定する
		self.end.bind("<ButtonPress>", self.__end)

		# ゲーム開始ボタンを配置する
		self.start.pack(side=LEFT)
		# ゲーム再スタートボタンを配置する
		self.restart.pack(side=LEFT)
		# ゲーム終了ボタンを配置する
		self.end.pack(side=LEFT)

		# じゃんけんの手を管理するボタンを組み立てていく
		# ボタンを配置するフレームを用意する
		janken_frame: Frame = Frame(self)
		# フレームを配置する
		janken_frame.pack()
		# グーボタンを用意する
		self.rock: Button = Button(janken_frame, text="グー", image=self.rock_img,
                             compound="top", state=Const.DISABLED)
		# ボタンを押した際に、動作させたい関数を指定する
		self.rock.bind("<ButtonPress>", self.__judge)
		# チョキスタートボタンを用意する
		self.scissors: Button = Button(janken_frame, text="チョキ",
                                 image=self.scissors_img, compound="top", state=Const.DISABLED)
		# ボタンを押した際に、動作させたい関数を指定する
		self.scissors.bind("<ButtonPress>", self.__judge)
		# パーボタンを用意する
		self.paper: Button = Button(janken_frame, text="パー",
                              image=self.paper_img, compound="top", state=Const.DISABLED)
		# ボタンを押した際に、動作させたい関数を指定する
		self.paper.bind("<ButtonPress>", self.__judge)

		# グーボタンを配置する
		self.rock.pack(side=LEFT)
		# チョキボタンを配置する
		self.scissors.pack(side=LEFT)
		# パーボタンを配置する
		self.paper.pack(side=LEFT)

	def __start(self, event):
		'''
		ゲームの開始をする
		'''

		# ログを削除する
		if len(self.log_message.get('insert', 'insert +1c')) > 1:
			print(len(self.log_message.get('insert', 'insert +1c')))
			self.log_message.delete(0, END)

		# Enemy名とPrayer名が未入力の場合
		if not self.enemy_unit.is_name() and not self.prayer_unit.is_name():
			# エラーメッセージを出す
			showerror(self.ERR_TITLE, f"{self.PRAYER}と{self.ENEMY}{self.ERR_MESSAGE}")
			# 処理を終了させる
			return

		# Enemy名とPrayer名のどちらが未入力の場合
		elif not self.enemy_unit.is_name() or not self.prayer_unit.is_name():
			# 未入力の対象名をデフォルトでは「エネミー」にしておく
			target: str = self.ENEMY
			# Prayer名が未入力の場合はtargetを「プレイヤー」に変更する
			if not self.prayer_unit.is_name():
				target = {self.PRAYER}
			# エラーメッセージを出す
			showerror(self.ERR_TITLE, f"{target}{self.ERR_MESSAGE}")
			# 処理を終了させる
			return

		# 両ユニットの勝利回数表示のリセットを行う
		self.__reset()

		# 両ユニットの入力欄の入力状態を変更する
		self.__state_changed()

		# じゃんけんの手のクリック状態を変更する
		self.__menu_btn_state_changed()

		# じゃんけんの手のクリック状態を変更する
		self.__hand_btn_state_changed()

		self.print(f"ゲーム開始!!{self.NEW_LINE}")

	def __restart(self, event):
		'''
		ゲームを最初から行う
		'''
		# 両ユニットの勝利回数表示のリセットを行う
		self.__reset()

	def __end(self, event):
		'''
		ゲームの終了と後処理をする
		'''
		# 両ユニットの入力欄の入力状態を変更する
		self.__state_changed()

		# じゃんけんの手のクリック状態を変更する
		self.__menu_btn_state_changed()

		# じゃんけんの手のクリック状態を変更する
		self.__hand_btn_state_changed()

		# 両ユニットの勝利回数表示のリセットを行う
		self.__reset()

	def __state_changed(self):
		'''
		両ユニット名入力欄の入力の状態を変更する
		'''
		# エネミー名入力欄を入力状態を変更する
		self.enemy_unit.state_changed()
		# プレイヤー名入力欄を入力状態を変更する
		self.prayer_unit.state_changed()

	def __menu_btn_state_changed(self):
		'''
		ボタンの状態を変更する
		'''
		# ゲーム開始ボタンがクリック可能の場合
		if self.start[Const.STATE] == Const.NORMAL:
			# ゲーム開始ボタンをクリック不可にする
			self.start[Const.STATE] = Const.DISABLED
		else:
			# ゲーム開始ボタンをクリック可能にする
			self.start[Const.STATE] = Const.NORMAL
		# ゲーム再スタートボタンがクリック可能の場合
		if self.restart[Const.STATE] == Const.NORMAL:
			# ゲーム再スタートボタンをクリック不可にする
			self.restart[Const.STATE] = Const.DISABLED
		else:
			# ゲーム再スタートボタンをクリック可能にする
			self.restart[Const.STATE] = Const.NORMAL
		# ゲーム終了ボタンがクリック可能の場合
		if self.end[Const.STATE] == Const.NORMAL:
			# ゲーム終了ボタンをクリック可不可にする
			self.end[Const.STATE] = Const.DISABLED
		else:
			# ゲーム終了ボタンをクリック可能にする
			self.end[Const.STATE] = Const.NORMAL


	def __hand_btn_state_changed(self):
		'''
		ボタンの状態を変更する
		'''
		# グーボタンがクリック可能の場合
		if self.rock[Const.STATE] == Const.NORMAL:
			# グーボタンをクリック不可にする
			self.rock[Const.STATE] = Const.DISABLED
		else:
			# グーボタンをクリック可能にする
			self.rock[Const.STATE] = Const.NORMAL
		# チョキボタンがクリック可能の場合
		if self.scissors[Const.STATE] == Const.NORMAL:
			# チョキボタンをクリック不可にする
			self.scissors[Const.STATE] = Const.DISABLED
		else:
			# チョキボタンをクリック可能にする
			self.scissors[Const.STATE] = Const.NORMAL
		# パーボタンがクリック可能の場合
		if self.paper[Const.STATE] == Const.NORMAL:
			# パーボタンをクリック可不可にする
			self.paper[Const.STATE] = Const.DISABLED
		else:
			# パーボタンをクリック可能にする
			self.paper[Const.STATE] = Const.NORMAL

	def __reset(self):
		'''
		両ユニットの勝利回数表示をリセットする
		'''
		# エネミーの勝利回数表示をリセットする
		self.enemy_state.reset()
		# プレイヤーの勝利回数表示をリセットする
		self.prayer_state.reset()

	def __judge(self, event):
		'''
		じゃんけんの勝敗を決める
		'''
		# 押されたボタンでプレイヤーの手を設定する
		prayer_hand: int = self.JANKEN[event.widget["text"]]
		# プレイヤーの手をログに表示する
		self.print(
			f"{self.prayer_unit.get_name()}は{event.widget['text']}を出した。{self.NEW_LINE}")
		# ランダムでエネミーの手を決める
		enemy_hand: int = randrange(start=0, stop=self.JANKEN_NAM)
		# エネミーの手をログに表示する
		self.print(
			f"{self.enemy_unit.get_name()}は{[key for key, value in self.JANKEN.items() if value == enemy_hand][0]}を出してきた。{self.NEW_LINE}")

		# 結果をデフォルトでは「あいこ」にしておく
		result: str = f"あいこだ!!"

		# プレイヤーの勝ち
		if ((prayer_hand == self.JANKEN["グー"]) and (enemy_hand == self.JANKEN["チョキ"])) or ((prayer_hand == self.JANKEN["チョキ"]) and (enemy_hand == self.JANKEN["パー"])) or ((prayer_hand == self.JANKEN["パー"]) and (enemy_hand == self.JANKEN["グー"])):
			# 結果をプレイヤーの勝ちに変更する
			result = f"{self.PRAYER}{self.WIN}"
			# プレイヤーの勝利回数を更新する
			self.prayer_state.set_win()
		# エネミーの勝ち
		elif ((prayer_hand == self.JANKEN["グー"]) and (enemy_hand == self.JANKEN["パー"])) or ((prayer_hand == self.JANKEN["チョキ"]) and (enemy_hand == self.JANKEN["グー"])) or ((prayer_hand == self.JANKEN["パー"]) and (enemy_hand == self.JANKEN["チョキ"])):
			# 結果をエネミーの勝ちに変更する
			result = f"{self.ENEMY}{self.WIN}"
			# エネミーの勝利回数を変更する
			self.enemy_state.set_win()

		#結果をログに表示する
		self.print(f"{result}{self.NEW_LINE}")

		# ログが最終行へ持っていく
		self.log_message.see('end')

		# プレイヤーまたはエネミーのどちらかの勝利回数が3になった場合
		if self.prayer_state.is_value() or self.enemy_state.is_value():
			# 結果をデフォルトでは「YOU WIN」にしておく
			win_result:str ="YOU WIN!!"
			
			# エネミーが勝利者の場合
			if self.enemy_state.is_value():
				# 結果を「YOU LOSE」にする
				win_unit = "YOU LOSE!!"
			
			# 勝利結果をダイアログに表示する
			showinfo("ゲーム結果",win_result)
			self.__end(event)


if __name__ == '__main__':
	#ウィジットの設定
	app = Application(Tk())

	# GUIを表示
	app.mainloop()
