import PySimpleGUI as sg
import time
import crawler
import yaramain
import detect
import os

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
    exec(open('detect.py').read())
    try:
        exec(open('crawler.py').read())
    except Exception:
        #exec(open('yaramain.py').read())
        fo = open("temp.txt", "r+")
        pa = fo.read(4)
        fo.close()
        if(pa=='lvla'):
            result = "MOST PROBABLY A MALICIOUS WEBSITE"
        elif(pa=='lvlb'):
            result = "SAFE WEBSITE"
    os.remove("temp.txt")    
    time.sleep(5)
    sg.Popup("RESULT : ", result)
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

windowa.close()
