#Developer: Eros Di Pede
#Application Name: Web Crawler
#Development began: May 15th, 2018

from bs4 import BeautifulSoup 
import requests
import time
logName = time.strftime("%Y%m%d-%H%M%S") + ".txt"
logFile = open(logName,"w")
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
def testAnchors(markup,url):
    brokenCounter = 0
    failedCounter = 0
    print("Beginning Link Check!")
    logFile.write("Beginning Link Check!")
    anchors = grabElements(markup,'a')
    #ensures there are tags to work with
    if (anchors != None):
        #iterate through tags
        for ref in anchors:
             #gets the href element from the anchor tags
             link = ""
             try:
                 #print(ref.get('href'))
                 link = ref.get('href').replace("http://","").replace("https://","")
             except (AttributeError):
                 print("No href found for " + str(ref) + "\n")
                 logFile.write("No href found for " + str(ref) + "\n")
             #ensures that it isnt a blank href  
             if (len(link) > 0):
                 if (link[0] == "#"): continue
                 elif (link[0] != "/"): link = "http://" + link 
                 elif (link[0] == "/"): link = "http://" + url.replace("http://","").replace("https://","") + link
                 else: continue 
             else: continue
         
             #prints what is returned from the page
             try:
                 if (statusCodeHandler(requests.head(link).status_code) != 1):
                     print(link + ' returns ' + str(requests.head(link).status_code) + statusCodeHandler(requests.head(link).status_code) + "\n")
                     logFile.write(link + ' returns ' + str(requests.head(link).status_code) + statusCodeHandler(requests.head(link).status_code) + "\n")
                     brokenCounter+=1
                 else: 
                     logFile.write(link + ' returns ' + str(requests.head(link).status_code) + "\n")
                     print(link + ' returns ' + str(requests.head(link).status_code) + "\n")
             except (requests.ConnectionError, requests.exceptions.InvalidURL) as e: #unable to connect to link
                 print("Failed to connect to " + link + "\n")
                 logFile.write("Failed to connect to " + link + "\n")
                 failedCounter+=1
    #no anchor tags found on the page
    else: 
        print("No anchor tags found!") 
        logFile("No anchor tags found!")
    print((str(len(anchors)) if (anchors != None) else "0") + " anchor tags found, " + str(brokenCounter) + " broken links found, failed to connect to " + str(failedCounter))
    logFile.write((str(len(anchors)) if (anchors != None) else "0") + " anchor tags found, " + str(brokenCounter) + " broken links found, failed to connect to " + str(failedCounter) + "\n")
    print("Link Check Complete!")
    logFile.write("Link Check Complete!")

def testElements(markup,url):
    missingAtt = 0
    print("What element do you wanna test") 
    logFile.write("What element do you wanna test\n")
    element = input().lower().replace("<","").replace(">","")
    logFile.write(element + "\n")
    elements = grabElements(markup,element)
    if (elements != None):
        print("What attribute do you wanna check for? (enter none to just search for elements)")
        logFile.write("What attribute do you wanna check for? (enter none to just search for elements)\n")
        attribute = input().lower()
        logFile.write(attribute + "\n")
        for element in elements:
            if (element != None):
                if (attribute == "none"):
                    print("Element found " + str(element))
                    logFile.write("Element found " + str(element) + "\n")
                else:
                    if (element.get(attribute) != None): missingAtt += 1
                    logFile.write("Attribute found for " + str(element) + "\n" if (element.get(attribute) != None) else 
                                 "No " + attribute + " found for " + str(element) + "\n")
                    print("Attribute found for " + str(element) + "\n" if (element.get(attribute) != None) else 
                          "No " + attribute + " found for " + str(element) + "\n")
        print(str(len(elements)) + " found, " + str(missingAtt) + " missing attribute, if provided")
        logFile.write(str(len(elements)) + " found, " + str(missingAtt) + " missing attribute, if provided\n")
    else:
        print("No elements of type " + element + " found")
        logFile("No elements of type " + element + " found\n")
        
#main function
def main():
    loop = True;
    while (loop):
        try:
            #communicates with user
            print("Hello, I'm a Web Crawler, please input a URL")
            logFile.write("Hello, I'm a Web Crawler, please input a URL\n")
            #gets input
            url = (input().lower())
            logFile.write(url + " /n")
            #checks if user wants to quit
            html = url;
            if (url == "quit"):
                print("See ya later!")
                logFile.write("Quit\n")
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
                    logFile.write("Invalid URL, try adding http:// to the beginning of the URL, or maybe you're offline!\n")
                    continue
                logFile.write("Now, what can I do for you?" )
                print("Now, what can I do for you?" )
                logFile.write("Possible commands: \n link check - checks all the anchor tags for valid urls\n element check - searchs page for an element, and can check if an attribute is present \n quit - quits the application\n")
                print("Possible commands: \n link check - checks all the anchor tags for valid urls\n element check - searchs page for an element, and can check if an attribute is present \n quit - quits the application" )

                job = inputHandler(input().lower())
                
    			  #ensures a function is returned
                if (job != None):
                    #checks if user wants to quit
                    if (job == 0): 
                        print("Bye bye for now!")
                        logFile.write("Quit\n")
                        break;
                    #calls function returned
                    job(html.text,url)
                #invalid input
                else:
                    logFile.write("Not a valid function! Try again!\n")
                    print("Not a valid function! Try again! \n")
        except (KeyboardInterrupt) as e: 
            print("Bye for now!")
            logFile.write("Program closed\n")
            break;
    logFile.close();
main()