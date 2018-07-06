# modules
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


# urls
base_src	= "https://www.menicka.cz/"
target		= "https://www.menicka.cz/brno.html"


def url_find():
	''' Method for collecting urls '''

	r 		= requests.get(target)
	soup 	= bs(r.text, 'html.parser')
	find_div= soup.find_all('div', attrs={'class': 'nazev'})

	# collecting urls into all_data
	urls = []
	
	for item in find_div:
		try:
			urls.append(item.find('a')['href'])
			# all_data.append(item.find('a')['href'])
		except TypeError:
			pass

	
	# return all_data
	# collecting streets, postals and locality into address
	
	all_data = []

	for key in urls:
		#print('My key: {}, my value: {}' .format(key, all_data[key]))
		url = key
		#print(url)
		q 	= requests.get(url)
		# q.encoding='utf-8'
		sup = bs(q.content, 'html.parser')
		
		address = []
		
		name 		= sup.find_all('span', attrs = {'class': 'org'})
		street 		= sup.find_all('p', attrs = {'class': 'street-address'})
		postal_code = sup.find_all('span', attrs = {'class': 'postal-code'})
		locality	= sup.find_all('span', attrs = {'class': 'locality'})
		www			= sup.find_all('a', attrs={'class': 'url'})

		
		if len(www) == 0:
			continue
		
		address.append(www[0].get('href'))
		address.append(name[0].text)
		address.append(street[0].text)
		address.append(postal_code[0].text)
		address.append(locality[0].text)

		all_data.append(address)
		
	print(all_data)

	return all_data


def export_cls(all_data):
	''' exporting all_data into csv file '''

	df 			= pd.DataFrame(all_data, columns=['Url', 'Name', 'Street', 'Postal-code', 'Locality'])
	df.to_csv('all_data_rest.csv', index=False, encoding='utf-8')
	
all_data = url_find()
export_cls(all_data)

	


