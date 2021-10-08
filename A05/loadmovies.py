def createTable():
	sql = """
	CREATE TABLE crew (
		mid VARCHAR(10),
		directors TEXT,
		writers	TEXT
	)
	"""
	
	cnx.query(sql)
	
def longer(a,b):
	if len(a) > len(b):
		return True
	return False
	
if __name__=='__main__':
	createTable();
	
	files = glob.glob('datasets.imdbws.com/*.tsv')
	
	for file in files:
		print(file)
		if file == 'datasets.imdbws.com/title.crew.tsv':
			longest1 = 0
			longest2 = 0
			
			with open(file, newline='\n') as tsvfile:
				movieData = csv.reader(tsvfile, delimiter='\t')
				next(movieData)
				for 