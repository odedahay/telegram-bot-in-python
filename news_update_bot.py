from bs4 import BeautifulSoup
import requests

def get_news():
	url='http://www.straitstimes.com/container/custom-landing-page/breaking-news'
	res=requests.get(url)

	while(res.status_code!=200):
		try:
			res=requests.get('url')
		except:
			pass

	soup = BeautifulSoup(res.text,'lxml')
	top_news = soup.find_all('span', {'class':'story-headline'})

	return top_news
