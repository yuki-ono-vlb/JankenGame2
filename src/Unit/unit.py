
from tkinter import LEFT, Entry, Frame, Label
from const import Const

class UnitFrame(Frame):
	'''
	ユニット共通部分のGUI構成
	'''

	def __init__(self, root: Frame, text: str):
		'''
		初期設定
		'''
		# 継承元であるFrameへ設定を渡す
		super().__init__(root)
		# GUIのサイズを指定する
		# 他の関数で使用できる様にする
		self.text = text
		# ユニット名関連のフレームをメインとなるGUIに配置する
		self.pack()
		# ユニット名のアイテムを組み立てていく
		self.__create_wigets()

	def __create_wigets(self):
		'''
		GUIの構成を行う
		'''
		fonts = ("", 15)
		# ユニット名のラベルを作る
		unit_label: Label = Label(self, text=self.text,font=fonts)
		# ユニット名のラベルを配置する
		unit_label.pack(side=LEFT)
		# ユニット名の入力欄を作る(他の関数で利用できる様にselfを付ける)
		self.unit_name: Entry = Entry(self, state=Const.NORMAL, width="50")
		# ユニット名の入力欄を配置する
		self.unit_name.pack(side=LEFT)

	def get_name(self) -> str:
		'''
		ユニット名を取得する
		'''
		return self.unit_name.get()
	
	def is_name(self) ->bool:
		'''
		ユニット名が入力されているかを確認する
		'''
		return len(self.unit_name.get()) > 0

	def state_changed(self):
		'''
		ネーム入力欄の状態を変える
		'''
		# 入力可能状態であれば非入力状態にする
		if self.unit_name[Const.STATE] == Const.NORMAL:
			self.unit_name[Const.STATE] = Const.DISABLED
			return
		
		# 入力状態にする
		self.unit_name[Const.STATE] == Const.NORMAL


class StateFrame(Frame):
	'''
	ユニットの勝敗の表示を管理する
	'''

	# 勝利回数
	VICTORY_COUNTS: str = "勝利回数"
	# 勝利回数の最大値
	MAX_CONUT: int = 3
	# スラッシュ
	SLASH: str = "/"
	# 勝利回数
	value: int = 0
	# 回
	COUNT:str = "回"

	def __init__(self, root: Frame):
		'''
		初期設定
		'''
		# 継承元であるFrameへ設定を渡す
		super().__init__(root)
		# ユニットの勝敗表示関連のフレームをメインとなるGUIに配置する
		self.pack()
		# ユニット名のアイテムを組み立てていく
		self.__create_wigets()

	def __create_wigets(self):
		'''
		GUIの構成を行う
		'''
		# フォントの設定をする
		fonts = ("", 30)
		# 勝利回数の表示を行うLabelを設定する
		self.win_label: Label = Label(
			self, font=fonts, text=f"{self.VICTORY_COUNTS} {self.value}{self.SLASH}{self.MAX_CONUT}{self.COUNT}")
		
		# 勝利回数の表示を行うLabelを配置する
		self.win_label.pack()

	def set_win(self):
		'''
		勝利回数の状態を変化させる
		'''
		# valueを増やしていく
		self.value = self.value + 1
		# 勝利回数の表示を更新する
		self.win_label["text"] = f"{self.VICTORY_COUNTS} {self.value}{self.SLASH}{self.MAX_CONUT}{self.COUNT}"

	def reset(self):
		'''
		勝利回数の状態を初期化する
		'''
		# valueを0に戻す
		self.value = 0
		# 勝利回数の表示を更新する
		self.win_label["text"] = f"{self.VICTORY_COUNTS} {self.value}{self.SLASH}{self.MAX_CONUT}{self.COUNT}"

	def is_value(self) -> bool:
		'''
		勝利回数が３回かどうか
		'''
		return self.value == self.MAX_CONUT