#Developer: Eros Di Pede
#Application Name: Web Crawler
#Development began: May 15th, 2018

from bs4 import BeautifulSoup 
import requests

#work around for switch statements used to return header codes
def statusCodeHandler(code):
    switch = {
        400: ' (Bad Request)',
        401: ' (Unauthorized)',
        403: ' (Forbidden)',
        404: ' (Page not found)',
        500: ' (Internal Sever Error)',
        502: ' (Bad Gateway)',
        503: ' (Service Unavailable)',
        504: ' (Gateway Timeout)'
    }
    return switch.get(code) if (switch.get(code) != None) else 1

#work around for switch statements used to choose what the user wants to do
def inputHandler(input):
    #checks if the user wants to quit
    if (input == "quit"):
        return 0
    switch = {
        'link check': testAnchors
    }
    return (switch.get(input))

#returns the anchors in the web page
def grabAnchors(url):
    bf = BeautifulSoup(url, 'html.parser')
    #gets all the anchor tags on the page
    anchors = bf.find_all('a')
    #returns the anchor array, or 0 if no anchor tags found
    return anchors if (len(anchors) > 0) else None

#tests all the hrefs on the page
def testAnchors(url):
    print("Beginning Link Check!")
    anchors = grabAnchors(url)
    #ensures there are tags to work with
    if (anchors != None):
        #iterate through tags
        for ref in anchors:
             #gets the href element from the anchor tags
             try:
                 link = ref.get('href').replace("http://","").replace("https://","")
             except (AttributeError):
                 print("No href found!")
             #ensures that it isnt a blank href   
             if (len(link) != 0): link = "http://" + link           
             else: 
                 continue 
             try: #prints what is returned from the page
                 if (statusCodeHandler(requests.head(link).status_code) != 1):
                     print(link + ' returns ' + str(requests.head(link).status_code) + statusCodeHandler(requests.head(link).status_code))
                 else: 
                     print(link + ' returns ' + str(requests.head(link).status_code))
             except (requests.ConnectionError, requests.exceptions.InvalidURL) as e: #unable to connect to link
                 print("Failed to connect to " + link)
    
    else: print("No anchor tags found!") #no anchor tags found on the page
    print("Link Check Complete!")

#main function
def main():
    loop = True;
    while (loop):
        #communicates with user
        print("Hello, I'm a Web Crawler, please input a URL")
        #gets input
        url = (input().lower())
        #checks if user wants to quit
        html = url;
        if (url == "quit"):
            print("See ya later!")
            loop = False
        else:
            try:  
                #gets html from page
                html = requests.get(url)
                #ensures that the request was successful
                html.raise_for_status()
            #catchs exceptions
            except (requests.exceptions.RequestException) as e:
                print("Invalid URL, try adding http:// to the beginning of the URL!")
                continue
            print("Now, what can I do for you?" )
            print("Possible commands: \n link check - checks all the anchor tags for valid urls\n quit - quits the application" )
            job = inputHandler(input().lower())
            
            #ensures a function is returned
            if (job != None):
                #checks if user wants to quit
                if (job == 0): 
                    print("Bye bye for now!")
                    loop = False
                #calls function returned
                job(html.text)
            #invalid input
            else:
                print("Not a valid function! Try again! \n")
main()