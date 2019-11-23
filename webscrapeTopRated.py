import json
from bs4 import BeautifulSoup
import requests
import urllib.request 
import time

imagesDict = {
	"lips" : "https://www.sephora.com/shop/lips-makeup?searchTerm=lip&sortBy=BEST_SELLING",
	"shadow" : "https://www.sephora.com/shop/eyeshadow?sortBy=BEST_SELLING", 
	"liner" : "https://www.sephora.com/shop/eyeliner?sortBy=BEST_SELLING", 
	"brows" : "https://www.sephora.com/shop/eyebrow-makeup-pencils?sortBy=BEST_SELLING", 
	"contour" : "https://www.sephora.com/shop/contour-palette-brush?sortBy=BEST_SELLING",
	"highlight" : "https://www.sephora.com/shop/luminizer-luminous-makeup?sortBy=BEST_SELLING", 
	"blush" : "https://www.sephora.com/shop/blush?sortBy=BEST_SELLING"
}

def getTopProducts(product):
	link = imagesDict[product]
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	children = list(soup.children)
	body = list(children[2].children)
	body = list(body[1].children)
	body = list(body[0].children)
	body = list(body[1].children)
	body = list(body[0].children)
	body = list(body[0].children)
	body = list(body[0].children)
	body = list(body[0].children)
	body = list(body[1].children)
	body = list(body[1].children)
	body = list(body[2].children)
	body = list(body[0].children)
	body = list(body[0].children)
	body = list(body[0].children)
	# commence for loop here
	targets = []
	imageTargets = []
	for i in body:
		for j in list(i.children):
			targets += [j["href"]]
			for k in list(j.children):
				l = list(k.children)
				# for m in range(len(l)):
				# 	print()
				o = list(list(l[0].children)[0].children)
				imageTargets += o
	images = []
	for imDiv in imageTargets:
		children = list(imDiv.children)
		try:
			images += ["https://sephora.com" + children[0]["src"]]
		except:
			continue
	print(images)

	class AppURLopener(urllib.request.FancyURLopener):
	    version = "Mozilla/5.0"

	opener = AppURLopener()

	for link in range(len(images)):
		txt = open('/Users/sanalakdawala/Documents/CMU/Year 1/Semester 2/15-112 Fundamentals of Programming/Term Project/Top Products/%s/%s.jpg' % (product, link), "wb")
		response = opener.open(images[link])
		txt.write(response.read())
	
	txt.close()

	print(targets)	
	return targets

getTopProducts("lips")
