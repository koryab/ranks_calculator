import sys
from PyQt5 import QtWidgets
import design
from logic import*

class windowApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
	"""docstring for windowApp"""
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.faq_btn.clicked.connect(self.instructions)
		self.overall_browse_btn.clicked.connect(self.browse_overall)
		self.overall_clear_btn.clicked.connect(self.clear_overall_line)
		self.season_browse_btn.clicked.connect(self.browse_season)
		self.season_clear_btn.clicked.connect(self.clear_season_line)
		self.games_browse_btn.clicked.connect(self.browse_games)
		self.games_clear_btn.clicked.connect(self.clear_games_line)
		self.exit_btn.clicked.connect(sys.exit)
		self.action_btn.clicked.connect(self.action)
		self.overall_line.setReadOnly(True)
		self.season_line.setReadOnly(True)
		self.games_line.setReadOnly(True)
		self.msg_plain.setReadOnly(True)

	def instructions(self):
		self.msg_plain.clear()
		self.msg_plain.setPlainText("Программа создана для подсчёта рейтингов КВИЗ,ПЛИЗ!\n\n"+
		"Как посчитать?\n 1. Необходимо выбрать файлы с общим рейтингом, рейтингом сезона и итогами игры. Для этого нажми кнопку \"Выбор файла\" под соответствующим полем."
		+"Откроется окно файловой системы, где можно будет найти и выбрать файл(ы). Если не выбран файл с рейтингом сезона,"+
		" то новый рейтинг сезона будет сформирован из итогов игры. Можно выбирать несколько файлов с итогами игры, например все игры за неделю.\n"+
		"3. После выбора файлов нажми кнопку \"Посчитай,плиз!\". Программа сделает свою работу и запросит у тебя места сохранения и названия"+
		" для новых файлов с общим рейтингом и рейтингом сезона, открыв поочередно два окна:" + 
		"\"Сохранить файл с общим рейтингом\" и \"Сохранить файл с рейтингом сезона\", соответственно. По окончании своей работы в прямоугольном поле будет выведено сообщение "+
		"\"ГОТОВО\" и список команд с повышениями, если таковые имеются. Если рейтинг сезона не требуется, его подсчёт можно отключить.\n"+ 
		"4. Открой эти файлы.\n5. PROFIT! Проделав все шаги предыдущие шаги можно посчитать рейтинги ещё раз.\n6. Для завершения работы программы нажми выход.\n\n"+
		"\t!!!Есть ограничения по работе программы!!!\n1.Для корретной работы таблицы с итогами игры должны быть в следующем формате:\n"+
		"Столбец \"А\" (1 столбец) должен содержать названия команд, столбец \"I\" (9 столбец) - итоговые баллы! Между - баллы по раундам. Остальное нужно стереть.\n"+"Таблицы сезона и общего рейтинга - четыре столбца:"+
		" с названиями команд, количеством игр, баллами и рангами, соответственно. Для КиМ пятый столбец - оскары. Остальное - стереть.\n"+
		"2.Программа различает регистры, не исправляет ошибки и опечатки. Если название команды написано иначе, чем уже имеющееся в таблице - оно будет вписано в конец,"+
		" как новая команда.")

	def action(self):
		try:
			self.msg_plain.clear()

			team = extract_scores(self.overall_line.text())
			played = extract_games(*self.games_line.text().split(', '))
			
			team = game_to_scores(played, team)
			gametype = self.gametype_box.currentIndex()
			#promoted = rank.rank(team, played.keys(), gametype)
			promoted = ranking(team, played, gametype)

			save_name = QtWidgets.QFileDialog.getSaveFileName(self,"Сохранить файл с общим рейтингом")
			save_result(team, save_name[0])

			if self.season_on.isChecked() is True:
				
				if self.season_line.text() != '': 
					season_team = extract_scores(self.season_line.text())
					season_team = game_to_scores(played, season_team)
				else:
					season_team = played
				
				ranking(season_team, played, gametype)

				save_name = QtWidgets.QFileDialog.getSaveFileName(self,"Сохранить файл с рейтингом сезона")
				save_result(season_team, save_name[0])
			
			print(promoted)
			if promoted != {} or promoted != None:
				text = 'ГОТОВО\n\n'+'Поздравляем с повышением!\n'
				for i in promoted.keys():
					text = text + '\n' + i + ':\n' + '\n'.join(promoted[i]) + '\n'
			else: text = 'ГОТОВО'
			self.msg_plain.setPlainText(text)

		except AssertionError as e:
			self.msg_plain.setPlainText(str(e))
			#self.msg_plain.setPlainText("Что-то пошло не так!\nПроверь корректность таблиц!")
		except ValueError:
			self.msg_plain.setPlainText("Save: отмена сохранения.\n")

	def clear_overall_line(self):
		self.overall_line.clear()

	def browse_overall(self):
		self.overall_line.clear()
		file_overall = QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
		self.overall_line.setText(file_overall[0])
	
	def clear_season_line(self):
		self.season_line.clear()

	def browse_season(self):
		self.season_line.clear()
		file_season = QtWidgets.QFileDialog.getOpenFileName(self,"Выберите файл")
		self.season_line.setText(file_season[0])
	
	def clear_games_line(self):
		self.games_line.clear()

	def browse_games(self):
		self.games_line.clear()
		files_games = QtWidgets.QFileDialog.getOpenFileNames(self,"Выберите файл(ы)")
		text = ', '.join(files_games[0])
		self.games_line.setText(text)	

def main():
	app = QtWidgets.QApplication(sys.argv)
	window = windowApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	#logic()
	main()
	pass