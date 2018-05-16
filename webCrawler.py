#Developer: Eros Di Pede
#Application Name: Web Crawler
#Development began: May 15th, 2018

from bs4 import BeautifulSoup 
import requests
#pseudo switch statements
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
    switch = {
        'link check': testAnchors,
        'element check': testElements
    }
    return (switch.get(input) if (input != "quit") else 0)

#returns the anchors in the web page
def grabElements(url,element):
    bf = BeautifulSoup(url, 'html.parser')
    #gets all the anchor tags on the page
    elements = bf.find_all(element)
    #returns the anchor array, or 0 if no anchor tags found
    return elements if (len(elements) > 0) else None

#tests all the hrefs on the page
def testAnchors(url):
    print("Beginning Link Check!")
    anchors = grabElements(url,'a')
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

def testElements(url):
    print("What element do you wanna test") 
    element = input().lower().replace("<","").replace(">","")
    elements = grabElements(url,element)
    if (elements != None):
        print("What attribute do you wanna check for? (enter none to just search for elements)")
        attribute = input().lower()
        for element in elements:
            if (element != None):
                if (attribute == "none"):
                    print("Element found " + str(element))
                else:
                    print("Attribute found for " + str(element) if (element.get(attribute) != None) else 
                          "No " + attribute + " found for " + str(element))
    else:
        print("No elements of type " + element + " found")
        
#main function
def main():
    loop = True;
    while (loop):
        try:
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
                    print("Invalid URL, try adding http:// to the beginning of the URL, or maybe you're offline!")
                    continue
                print("Now, what can I do for you?" )
                print("Possible commands: \n link check - checks all the anchor tags for valid urls\n element check - searchs page for an element, and can check if an attribute is present \n quit - quits the application" )

                job = inputHandler(input().lower())
                
    			  #ensures a function is returned
                if (job != None):
                    #checks if user wants to quit
                    if (job == 0): 
                        print("Bye bye for now!")
                        break;
                    #calls function returned
                    job(html.text)
                #invalid input
                else:
                    print("Not a valid function! Try again! \n")
        except (KeyboardInterrupt) as e: 
            print("Bye for now!")
            break;
main()