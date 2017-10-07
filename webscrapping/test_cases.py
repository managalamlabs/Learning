from scrapper import webscrapper

def multiples(x):
    return x*2

def test_function():
    assert multiples(2) == 5
	
def testwebscrappermethod():
    phrase = webscrapper.get_page_spoof('http://economictimes.indiatimes.com/')
    assert len(phrase.split()) >= 10