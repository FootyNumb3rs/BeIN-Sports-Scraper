from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import pprint as pp
import pandas as pd




def scrape_table(table):
	table_rows = table.find_elements_by_tag_name('tr')
	data = [scrape_row(row) for row in table_rows]
	return(data)


def scrape_row(row):
	attrs = row.find_elements_by_tag_name('td')
	data = [attr.text for attr in attrs]
	return(data)


def find_symbol(team_name):
	#(team_name)
	indx = symbols['teamName'].str.contains(team_name)
	print('{} :::: {}'.format(team_name,symbols.loc[indx,'teamName']))
	try:
		return(symbols.loc[indx,'crestURI'].tolist()[0])
	except:
		return('Noneee')

symbols = pd.read_csv('symbols.csv',header=0)

driver = webdriver.Chrome()



# Pulling 

LEAGUES = dict(zip(['laliga','serie-a','ligue-1','premier-league','bundesliga'],
				   ['La Liga','Serie A','Ligue 1','Premier League','Bundesliga']))
fin = []
for lg in LEAGUES.keys():
	driver.get('http://www.beinsports.com/us/{}/statistics'.format(lg))
	form = driver.find_elements_by_css_selector("form.ranking-category")[1]
	select = Select(form.find_element_by_tag_name('select'))
	select.select_by_visible_text('Assists')
	# Desired Stats
	pandas_header = ['Pos','Name','GP','Team','Stat']
	STATS = ['goals','assists','chances_created']
	STATS = dict(zip(STATS,['Goals','Assists','Ch. Created']))
	for st in STATS.keys():
		select.select_by_value(st)
		table = driver.find_element_by_css_selector('div.'+st)
		dff = pd.DataFrame(scrape_table(table)[1:],columns=pandas_header)
		dff['Statname'] = STATS[st]
		dff['League'] = LEAGUES[lg]
		dff['ABBR'] = 'FCB'
		dff['CREST'] = 'http://upload.wikimedia.org/wikipedia/de/d/de/Getafe_CF.svg'
		dff['Name'] = dff['Name'].str.split().str[-1]
		fin.append(dff)
datas = pd.concat(fin)
driver.close()



#datas = pd.read_csv('super_table5.csv',header=0)

## Applying Crests
datas['CREST'] = datas['Team'].apply(find_symbol)

## Reseting index
datas.reset_index(inplace=True,drop=True)

# Saving 
datas.to_csv('super_table5.csv',index=False)











