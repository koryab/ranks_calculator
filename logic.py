import os.path
from pandas import DataFrame, read_excel, concat, core

def game_to_scores(game, scores):
	"""
	Merging game results with scores into one DataFrame.
					
	"""
	try:
		assert type(game) is core.frame.DataFrame, "Game_to_Scores: Ошибка распаковки таблицы с игрой."
		assert type(scores) is core.frame.DataFrame, "Game_to_Scores: Ошибка распаковки рейтинга."

		df = concat([scores, game])
		df['Points'] = df.groupby(['Title'])['Points'].transform('sum')
		df['Games'] = df.groupby(['Title'])['Games'].transform('sum')
		df = df.reset_index()		
		df = df.drop_duplicates(subset=['Title']) #drop duplicates
		df = df.sort_values(by=['Points'], ascending=False)
		df = df.set_index('Title')

		return df

	except AssertionError as e:
		print(e)

def extract_scores(filepath):
	"""
	Extracting overall scores from Excel spreadsheets into DataFrame.

	"""
	extensions = ['xls', 'xlsx', 'xlsm', 'xlsb', 'xlt', 'xltx', 'xltm', 'xml']

	#try:
	assert type(filepath) is str, "Exctract_Overall: Неверный путь к файлу. Ожидается строка в формате \"my_dir/my_filename\"\n."
	assert os.path.exists(filepath), "Exctract_Overall: Не найден файл\"{}\".\n".format(filepath)
	assert filepath.split('.')[-1].lower() in extensions, "Exctract_Overall: Файл \"{}\" не является таблицой Excel.\n".format(filepath)
	
	df = read_excel(filepath, "Лист1").dropna(how='all')
	df = df.dropna(axis=1, how='all')
	assert len(df.columns) <= 5, "Exctract_Overall: Неверный формат таблицы \"{}\". Читай инструкцию.\n".format(filepath)
	if len(df.columns) == 3:
		df['Rank'] = None
	if len(df.columns) == 4:
		df.columns = ['Title','Games', 'Points', 'Rank']
	else:
		df.columns = ['Title','Games', 'Points', 'Rank', 'Extra Rank']
	df['Title'] = df['Title'].str.replace('ё','е').str.lower().str.title()
	df = df.set_index('Title')

	return df

	#except AssertionError as e:
	#	print(e)

def extract_games(*filepath):
	"""
	Extracting games results from Excel spreadsheets and merging into one DataFrame.

	"""
	try:
		extensions = ['xls', 'xlsx', 'xlsm', 'xlsb', 'xlt', 'xltx', 'xltm', 'xml']
		frames = list();
		j = -1
		#print(filepath)

		for i in range(len(filepath)):
			
			#try:
			assert type(filepath[i]) is str, "Exctract_Games: Неверный путь к файлу. Ожидается строка в формате \"my_dir/my_filename\"\n."
			assert os.path.exists(filepath[i]), "Exctract_Games:  Не найден файл\"{}\".\n".format(filepath[i])
			assert filepath[i].split('.')[-1].lower() in extensions, "Exctract_Games: Файл \"{}\" не является таблицой Excel.\n".format(filepath[i])
			
			j += 1
			frames.append(DataFrame())
			frames[j] = read_excel(filepath[i], "Лист1").dropna(how='all')
			frames[j] = frames[j].dropna(axis=1,how='any')
			assert len(frames[j].columns) == 9, "Exctract_Games: Неверный формат таблицы \"{}\". Читай инструкцию.\n".format(filepath[i])
			frames[j] = frames[j].iloc[:,[0,8]]
			frames[j].columns = ['Title','Total']
			frames[j]["Games"] = 1
			frames[j]['Title'] = frames[j]['Title'].str.replace('ё','е').str.lower().str.title()
			#print(frames[i],'\n',type(frames[i]),'\n')
	
			#except AssertionError as e:
			#	print(e)
			#except IndexError as e:
			#	print(e)

		df = concat(frames)
		df['Points'] = df.groupby(['Title'])['Total'].transform('sum')
		df['Games'] = df.groupby(['Title'])['Games'].transform('sum')
		df['Rank'] = None
		df = df.drop_duplicates(subset=['Title']) #drop duplicates
		df = df.drop('Total', axis=1) #drop exceeding column
		df = df.sort_values(by=['Points'], ascending=False)
		df = df.set_index('Title')

		return df

	except ZeroDivisionError as e:
		print(e)

def ranking(scores, game, gametype):
	
	"""promoted = {'Недосягаемые':[], 'Чак Норрис':[], 'Рэмбо':[], 'Генерал':[], 'Лейтенант':[], 'Сержант':[],
	'Бриллиантовая пластинка':[], 'Платиновая пластинка':[], '3 золотые пластинки':[], '2 золотые пластинки':[],
	'1 золотая пластинка':[], '3 виниловые пластинки':[], '2 виниловые пластинки':[], '1 виниловая пластинка':[],
	'10 уровень':[], '9 уровень':[],'8 уровень':[], '7 уровень':[], '6 уровень':[], '5 уровень':[], '4 уровень':[], '3 уровень':[], '2 уровень':[], '1 уровень':[],
	'Илон в маске и перчатках':[], 'Невыходные':[],'Чак QR-кодис':[], 'Рэмбо Балконный':[], 'Маршал удаленного полка':[], 'Генерал кухонной армии':[],
	'Лейтенант диванных войск':[], 'Сержант кресельного батальона':[], '':[]}"""

	promoted = dict()

	ranks = {'nedosyag':'Недосягаемые','chuck':'Чак Норрис','rambo':'Рэмбо','gener':'Генерал','liet':'Лейтенант','serg':'Сержант',
	'kim8':'Бриллиантовая пластинка','kim7':'Платиновая пластинка','kim6':'3 золотые пластинки','kim5':'2 золотые пластинки',
	'kim4':'1 золотая пластинка', 'kim3':'3 виниловые пластинки', 'kim2':'2 виниловые пластинки', 'kim1':'1 виниловая пластинка',
	'lvl10':'10 уровень','lvl9':'9 уровень','lvl8':'8 уровень','lvl7':'7 уровень','lvl6':'6 уровень','lvl5':'5 уровень',
	'lvl4':'4 уровень','lvl3':'3 уровень','lvl2':'2 уровень','lvl1':'1 уровень',
	'ilon-strim':'Илон в маске и перчатках','nedosyag-strim':'Невыходные','chuck-strim':'Чак QR-кодис','rambo-strim':'Рэмбо Балконный',
	'marsh-strim':'Маршал удаленного полка',
	'gener-strim':'Генерал кухонной армии',
	'liet-strim':'Лейтенант диванных войск',
	'serg-strim':'Сержант кресельного батальона', None : ''}

	#try:
	assert not game.empty, "Ranking: Нет результатов игры.\n"

	updated = game.index
	for team in updated:
		new_rank = rank_check(scores.at[team, "Points"], gametype)

		if new_rank != scores.at[team, "Rank"]:
			
			if ranks[new_rank] in promoted.keys():
				promoted[ranks[new_rank]].append(team)
			else:
				promoted[ranks[new_rank]] =  [team]
			
			scores.at[team, "Rank"] = new_rank
		else: 
			pass

	del promoted['']

	return promoted
	
	#except AssertionError as e:
	#	print(e)

def diap(x1, x2, y):
	if y >= x1 and y < x2:
		return True

def rank_check(score, gametype=0):

	if gametype == 0:
		if diap(0, 100, score):
			return None
		if diap(100, 250, score):
			return 'serg'
		if diap(250, 500, score):
			return 'liet'
		if diap(500, 1000, score):
			return 'gener'
		if diap(1000, 2000, score):
			return 'rambo'
		if diap(2000, 6000, score):
			return 'chuck'
		if diap(6000, 10e6, score):
			return 'nedosyag'
	if gametype == 3:
		if diap(0, 50, score):
			return None
		if diap(50, 100, score):
			return 'serg-strim'
		if diap(100, 250, score):
			return 'liet-strim'
		if diap(200, 400, score):
			return 'gener-strim'
		if diap(400, 600, score):
			return 'marsh-strim'
		if diap(600, 800, score):
			return 'rambo-strim'	
		if diap(800, 1000, score):
			return 'chuck-strim'
		if diap(1000, 5000, score):
			return 'nedosyag-strim'
		if diap(5000, 10e6, score):
			return 'ilon-strim'
	if gametype == 1:
		if diap(0, 100, score):
			return None
		if diap(100, 250, score):
			return 'kim1'
		if diap(250, 500, score):
			return 'kim2'
		if diap(500, 1000, score):
			return 'kim3'
		if diap(1000, 1500, score):
			return 'kim4'
		if diap(1500, 2000, score):
			return 'kim5'
		if diap(2000, 3000, score):
			return 'kim6'
		if diap(3000, 5000, score):
			return 'kim7'
		if diap(5000, 10e6, score):
			return 'kim8'
	if gametype == 2:
		if diap(0, 20, score):
			return None
		if diap(20, 50, score):
			return 'lvl1'
		if diap(50, 100, score):
			return 'lvl2'
		if diap(100, 150, score):
			return 'lvl3'
		if diap(150, 200, score):
			return 'lvl4'
		if diap(200, 300, score):
			return 'lvl5'
		if diap(300, 10e6, score):
			return 'lvl6'

def save_result(scores, name):
	extensions = ['xls', 'xlsx', 'xlsm', 'xlsb', 'xlt', 'xltx', 'xltm', 'xml']

	assert name is not None, "Save: отмена сохранения.\n"

	scores = scores.reset_index()

	if len(scores.columns) == 4:
		scores.columns = ['Название','Игры', 'Баллы', 'Ранг']
	else:
		scores.columns = ['Название','Игры', 'Баллы', 'Ранг', 'Доп.ранг']

	scores = scores.set_index('Название')
	if name.split('.')[-1] in extensions:
		scores.to_excel(name, "Лист1")
	else:
		scores.to_excel(name+".xlsx", "Лист1")

def test():
	games = ["test_data/excel_example (1).xlsx"]
	gf = extract_games(*games)
	print(gf)
	gf.to_excel("test.xlsx", "Лист1")
	of = extract_scores("test.xlsx")
	print(of)
	result = game_to_scores(gf, of)
	print(result)

if __name__ == '__main__':
	test()
	