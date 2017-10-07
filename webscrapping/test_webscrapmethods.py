from scrapper import webscrapper
	
def testwebscrappermethod():
    phrase = webscrapper.get_page_spoof('http://economictimes.indiatimes.com/')
    assert len(phrase.split()) >= 10