#!/usr/bin/env python3

import requests, bs4, os

url = 'http://xkcd.com'                     # starting url
os.makedirs('xkcd', exist_ok = True)        # store comics in ./xkcd
while not url.endswith('#'):
    # Download the page.
    print('Downloading the page %s...' %url)
    res = requests.get(url)
    res.raise_for_status()
    
    soup = bs4.BeautifulSoup(res.text, "html.parser")      # You create a BeautifulSoup object from the text of the downloaded page.
    
    
    
    # Find the URL of the comic image
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        #Grab the src link for the first element found
        comicUrl = 'http:' + comicElem[0].get('src')      #The comicUrl will have a value like 'http://imgs.xkcd.com/comics/heartbleed_explanation.png'?which you might have noticed looks a lot like a file path.
        # Download the image
        print('Downloading the image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()
        
        
        # Save the image to ./xkcd
        # Remember from earlier in this chapter that to save files you?ve downloaded
        # using Requests, you need to loop over the return value of the iter_content() method.
        imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    # Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]      # Afterward, the selector 'a[rel="prev"]' identifies the <a> element with the rel
                                                    # attribute set to prev, and you can use this <a> element?s href attribute to get
                                                    # the previous comic?s URL, which gets stored in url.
    url = 'http://xkcd.com' + prevLink.get('href')
    
print('Done')
        
