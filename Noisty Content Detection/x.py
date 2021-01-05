import PySimpleGUI as sg
import time
import os
from urllib.parse import urlparse,urljoin
import sys
import urllib.request
from bs4 import BeautifulSoup
import bs4
import re
from urllib.request import urlopen

d={}
score = [0,0,0,0,0]
temps = 0

def crawl():
    cnt=0
    while(len(urls) >0):
        print("--")
        templi=[]
        print("Current URL : ",urls[0])
        a = urllib.request.urlopen(urls[0])
        htmltext = a.read()
        headertext = str(a.info())
        soup = BeautifulSoup(htmltext)
        soup1 = BeautifulSoup(headertext)
        cnt=cnt+1
        f = open("html/"+str(cnt)+".html", "w+")
        f1 = open("header/"+str(cnt),"w+")
        f.write(soup.prettify())
        f1.write(soup1.prettify())
        f.close()
        f1.close()

        li = soup.findAll('a',href=True)  #A result set
        currentUrl=urls.pop(0)	

        for tag in li:
            tag['href'] = urljoin(currentUrl,tag['href'])  #if https:// is not there in the a href tag it pre-appends url
            if tag['href'] not in visited:	
                templi.append(tag['href'])
                urls.append(tag['href'])
                visited.append(tag['href'])
        print(currentUrl," has ",str(len(templi))," links.")
        for j in templi:
            print(j)
    print(len(visited), " sites are visited\n")
    for i in visited:
        print(i,"\n")

def check_phish(url):
    total_score=0
    final_score=0
    rev_ratio=0
    flag=0
    a=re.search(r'.+[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*',url)
    if(a!=None):
        final_score=0.90
        print("Final score : ",final_score)
        sys.exit(0)

    only_dom  = re.match(r"^(https?:\/\/)?(www.)?([\da-z\.-]+)\.([a-z\.]{2,6})(.*)\/?$",url)
              #sys.exit(0)

    if(only_dom!=None):
        print(only_dom.groups())
    else:
        print("No match")
    print("\nDomain Length");	
    print("--------------------")
    domain_length  = len(only_dom.group(3))
    print("domain length : ",domain_length)
    #-----calculating score------
    if(domain_length >= 1 and domain_length <= 4):
        score[0]=7
    elif(domain_length > 4 and domain_length<=7):
        score[0]=6
    elif(domain_length > 8 and domain_length<=10):
        score[0]=5
    elif(domain_length>10):
        score[0]=3

    print("\nURL length")
    print("--------------------")
    url_length = len(only_dom.group(3)) + len(only_dom.group(5))
    print("url length : ",url_length)
    #-----calculating score------
    if(url_length==domain_length):
        score[1]=2
    elif(url_length >= 100):
        score[1]=8
    elif(url_length > 40 and url_length <=100):
        score[1]=7
    elif(url_length >30 and url_length<=40):
        score[1]=6
    elif(url_length >20 and url_length<=30):
        score[1]=5
    elif(url_length >10 and url_length<=20):
        score[1]=4
    elif(url_length<=10):
        score[1]=3

    for i in set(only_dom.group(3)):
        d[i]=only_dom.group(3).count(i)
    print("\nUnique character ratio")
    print("--------------------")
    ratio=len(d)/len(only_dom.group(3))
    print(" Ratio : ",ratio)
    if(ratio>0 and ratio<=0.25):
        score[2]=8
    elif(ratio>0.25 and ratio<=0.40):
        score[2]=7
    elif(ratio>0.40 and ratio<=0.55):
        score[2]=6
    elif(ratio>0.55 and ratio<=0.70):
        score[2]=5
    elif(ratio>0.70 and ratio<=0.80):
        score[2]=4
    elif(ratio>0.80):
        score[2]=3

    print("\nBrand name presence")
    print("--------------------")

    brand_names = ["google","yahoo","g00gle","yah00","runescape","vogella","v0gella"]
    ignore_names = ["google-melange","google-styleguide","googlesciencefair","thinkwithgoogle","googleforentrepreneurs","withgoogle"]
    malicious_names = ["account","free","membs","membership","hacks","lottery","prize","money"]

    for i in brand_names:
        if(only_dom.group(3).find(i)!=-1):
            if(only_dom.group(3)==i):
                print("Not Phishing")
                sys.exit(0)
            regex1 = ".*\."+i+"\..*"
            regex3 = ".*\."+i
            if(re.match(regex1,only_dom.group(3)) or re.match(regex3,only_dom.group(3))):
                print("Not phishing")
                sys.exit(0)
            regex2 = ".*"+i+".*"
            if(re.match(regex2, only_dom.group(3))):
                flag=flag+1
                print("detected brand name")
    # FOR IGNORING NON-PHISHING SITES !!
            for j in ignore_names:
                regex2= ".*\."+j+"\..*"
                if(re.match(regex2,only_dom.group(3))):
                    print("Not phishing")
                    sys.exit(0)
            for k in malicious_names:
                if(only_dom.group(3).find(k)!=-1):
                    flag=flag+1
                    print("Suspected phishing")
    if(flag==1):
        score[3]=8
    elif(flag==2):
        score[3]=9
    elif(flag==3):
        score[3]=10
    elif(flag>3):
        score[3]=10	
    elif(flag==0):
        score[3]=3

    print("SCORE[3] : ",score[3])


    print("\nGlobal rank of website")
    print("---------------------------")

    try:
        str1 = bs4.BeautifulSoup(urlopen("http://www.alexa.com/siteinfo/"+ url).read(), "xml")		
    except urllib.URLError:
        print("URL error : ")	
    list_rank=re.findall(r"metrics-data align-vmiddle..([0-9,]*)<\/strong>",str(str1))
    if(len(list_rank)!=0):
        list_rank[0].strip('''metrics-data align-vmiddle">''')
        list_rank[0]=list_rank[0].replace(',','')       
        list_rank[0]=int(list_rank[0])
        print(list_rank[0])
        if(list_rank[0]>0 and list_rank[0]<50000):
            score[4]=1
        elif(list_rank[0]>=50000 and list_rank[0]<=100000):
            score[4]=2
        elif(list_rank[0]>100000):
            score[4]=8
        else:
            print("sorry invalid site name")
    else:
        print("No rank for this site")
        score[4]=10
#-------calculation of final score--------------

    for i in score:
        total_score=total_score+i
    final_score=total_score/50
    temps = final_score
    print("\nPercentage: ",(final_score*100))

    if(final_score>=0.50):
        print("\n----------More than 50 percent---------")
        print("--> Checking for password fields")
        str2 = bs4.BeautifulSoup(urlopen(url).read(),"xml")
        str2=str(str2)
        if(str2.find('''type="password"''')!=-1):
            print("::: Password fields present")
            rev_ratio = (total_score+9)/60
            print("--> Revised final percent : ",rev_ratio*100)
            flag=1
            tempa = rev_ratio*100
            strcon = str(tempa)
            foo = open("tempa.txt", "w+")
            foo.write(strcon)
            foo.close()
        else:
            flag=0
            print("::: No password fields")
            rev_ratio = final_score
            print("--> Revised final percent : ",rev_ratio*100)
            tempa = rev_ratio*100
            strcon = str(tempa)
            foo = open("tempa.txt", "w+")
            foo.write(strcon)
            foo.close()
    print("Conclusion")
    print("--------------------")
    
    if(final_score>=0.55):
        if(flag==1):
            pa='lvla'
        elif(flag==0):
            pa='lvla'
    else:
        pa='lvlb'    
    fo = open("temp.txt", "w+")
    fo.write(pa)
    fo.close()
        
sg.ChangeLookAndFeel('DarkBlue')

layout = [[sg.Text('',size=(100,2))],
           [sg.Text('MALICIOUS WEB TOOL',size=(100, 1), font=("Helvetica", 30),text_color='White',justification='center')],
           [sg.Text('',size=(100,10))],
           [sg.Text('Loading',font=("Helvetica", 10),text_color='White')],
           [sg.ProgressBar(1, orientation='h', size=(200, 20), key='progress',bar_color=('#0bb791', 'Grey'),style='alt')],
          ]

window = sg.Window('MALICIOUS WEB TOOL', layout, location=(50,50), size=(800,350), keep_on_top=True).Finalize()
progress_bar = window.FindElement('progress')
progress_bar.UpdateBar(0, 5)
time.sleep(.5)
progress_bar.UpdateBar(1, 5)
time.sleep(.5)
progress_bar.UpdateBar(2, 5)
time.sleep(.5)
progress_bar.UpdateBar(3, 5)
time.sleep(.5)
progress_bar.UpdateBar(4, 5)
time.sleep(.5)
progress_bar.UpdateBar(5, 5)
time.sleep(.5)
window.Close()

sg.ChangeLookAndFeel('DarkBlue')

layouta = [[sg.Text('',size=(100,2))],
           [sg.Text('MALICIOUS WEB TOOL',size=(100, 1), font=("Helvetica", 30),text_color='White',justification='center')],
           [sg.Text('',size=(100,2))],
           [sg.Text('Enter URL',text_color='White', size=(21, 1), auto_size_text=False, justification='center'), sg.InputText('',text_color='White',size=(80, 1))],
           [sg.Text('',size=(100,1))],
           [sg.Text('Enter Path of Rule File',text_color='White', size=(21, 1), auto_size_text=False, justification='center'), sg.InputText('D:/Project/',text_color='White',size=(80, 1))],
           [sg.Text('',size=(100,1))],
           [sg.Text('Enter Rule File Name',text_color='White', size=(21, 1), auto_size_text=False, justification='center'), sg.InputText('yararules',text_color='White',size=(80, 1))],
           [sg.Text('',size=(100,1))],
           [sg.Text('',size=(38,2)),sg.Submit()],
           [sg.Text('',size=(100,1))],
           ]

windowa = sg.Window('MALICIOUS WEB TOOL', layouta, default_element_size=(100, 2), location=(50,50), size=(800,350))

while True:                             # The Event Loop
    event, values = windowa.read() 
    print(event, values)
    x = values
    y = x[0]
    z = x[1]+x[2]
    url = str(y)
    check_phish(url)
    try:
        url=str(y)
        urls = [url]
        visited = [url]
        templi=[]
        crawl()
    except Exception:
        #exec(open('yaramain.py').read())
        fo = open("temp.txt", "r+")
        pa = fo.read(4)
        fo.close()
        if(pa=='lvla'):
            if(temps>=0.5):
                foo = open("tempa.txt", "r+")
                pb = foo.read(10)
                foo.close()
                result = "MOST PROBABLY A MALICIOUS WEBSITE: " + pb + "%"
            else:
                foo = open("tempa.txt", "r+")
                pb = foo.read(10)
                foo.close()
                result = "MOST PROBABLY A MALICIOUS WEBSITE: " + pb + "%"
        elif(pa=='lvlb'):
            result = "SAFE WEBSITE"
    time.sleep(5)
    sg.Popup("RESULT : ", result)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

windowa.close()
