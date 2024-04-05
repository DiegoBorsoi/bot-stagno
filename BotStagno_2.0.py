import win32gui #use: pip install pywin32
import win32api
import win32con
import sys
import time
import screenshotBG as sBG

import ctypes


def main():


    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)


    count = 0
    handlers = {}

    for x in titles:
        if(x != '')and((x.find('NosTale') != -1)or(x.find('Nostale') != -1)):
            hwnd = win32gui.FindWindow(None, x)
            handlers[hwnd] = x


    for x in list(handlers):
        print(str(count) + ' - ' + handlers[x] + ' (' + str(x) + ')')
        count+=1


    print('Seleziona il processo: ',end='')
    c = int(input())
    while (c < 0)or(c >= len(handlers)):
        print('Errore di inserimento.')
        print('Seleziona il processo: ',end='')
        c = int(input())

    print(list(handlers)[int(c)])

    botStagno(int(list(handlers)[int(c)]))


def botStagno(hwnd):

    c = 0
    while c == 0:

        print("Seleziona il livello della ricompensa(1-5): ", end='')

        liv = int(input())

        while (liv < 1)or(liv > 5):
            print('Input errato.')
            print("Seleziona il livello della ricompensa(1-5): ", end='')
            liv = int(input())

        livelli = { 1: (824,592), 2: (891,592), 3: (958,392), 4: (1025,592), 5: (1092,592)}

        '''
        position = (y << 16) + x

        pulsante: schermata game over
                    - ottieni la ricompensa - 1089, 588
                    - riprova - 828, 590
        pulsante: 5Lv - 1092, 592
        pulsante: ricompensa
                    - riprova - 904, 619
                    - stop - 1014, 619
        pulsante: inizia gioco - 956, 706
        '''

        print("Inserisci il numero di ricompense(minimo 1): ", end='')
        numRic = int(input())

        while (numRic < 1):
            print('Input errato.')
            print("Inserisci il numero di ricompense(minimo 1): ", end='')
            numRic = int(input())

        count = 1

        while True:

            time.sleep(1)
            #premi inizia gioco
            click(hwnd, 956, 706)

            print("Playing... " + str(count))
            ris = play(hwnd)

            if ris == 0:

                time.sleep(1)
                #premi ricompensa
                click(hwnd, 1089, 588)

                time.sleep(1)
                #premi la ricompensa del livello scelto
                click(hwnd, livelli[liv][0], livelli[liv][1])

                if count < numRic:
                    time.sleep(1)
                    #premi riprova
                    click(hwnd, 904, 619)
                    count += 1
                else:
                    time.sleep(1)
                    #premi stop
                    click(hwnd, 1014, 619)
                    break
            else:

                time.sleep(1)
                #premi riprova
                click(hwnd, 828, 590)

        print("Minigame concluso.")
        print("Ricominciare ?(0 = si/1 = no): ",end='')

        s = int(input())

        if s == 1:
            c = 1


def play(hwnd):

    pesceGrande = False
    stage = 0
    finitoGiusto = False

    centri = { 1: (809, 549), 2: (810, 549), 3: (812, 549), 4: (827, 549), 5: (851, 549), 6: (881, 549), 7: (929, 549), 8: (990, 549) }

    while True:

        im = sBG.screenGrab(hwnd)

        #im = ImageGrab.Image.open("1_6-dx.png","r")

        pix = im.load()

        '''
        punteggio: 2xxxx - pos(angolo in basso a sx, ultimo "giallo"): 892, 363 - color: 198, 163, 0

        schermata game over : (angolo nero alto sinistra(interno)) pos 746, 457 - color 18, 18, 17
        '''

        # aspettando la schermata di game over
        if finitoGiusto:
            if pix[746, 457] != (18, 18, 17):
                continue
            else:
                time.sleep(0.5)
                return 0

        # raggiunti 20000 punti
        if pix[892, 363] == (198, 163, 0):
            print("Livello 5 raggiunto.")
            finitoGiusto = True
            continue

        # se si muore prima dei punti giusti
        if pix[746, 457] == (18, 18, 17):
            print("Livello 5 non raggiunto.")
            time.sleep(0.5)
            return 1


        '''
        -- pesci normali
        linea centrale prima della punta nera verso il basso
        down = 930,566 , 255, 237, 118
        sx = 816,508
        up = 980,460
        dx = 1101,508

        -- pesce bonus  -  8 stage
            controllo: sulla freccia nella punta nero a sx se verso l'alto
            centro preso in centro alto a sinistra
            colore: 5, 3, 0
            sx = x, y-13 . dx = x+14, y . giu = x+1, y+14 . su = x-13, y+1
         - 1
             centro = 809, 549
             su  = 809, 536
         - 2
             centro = 810, 549
             dx  = 824, 549
         - 3
             centro = 812, 549
             su  = 812, 536
         - 4
             centro = 827, 549
             sx  = 814, 550
         - 5
             centro = 851, 549
             giu = 852, 563
         - 6
             centro = 881, 549
             su  = 881, 536
         - 7
             centro = 929, 549
             sx  = 916, 550
         - 8
             centro = 990, 549
             giu = 991, 563

        '''


        # 733, 533 - (68, 163, 248)
        if pesceGrande :
            if pix[733, 533] != (0, 0, 0):
                pesceGrande = False
                time.sleep(0.5)
        else:
            if pix[733, 533] == (0, 0, 0):
                pesceGrande = True
                stage = 1
                time.sleep(0.3)
                continue

        if pesceGrande and stage == 9:
            pesceGrande = False
            time.sleep(0.5)


        if pesceGrande:      # pesce grande
            #print(stage)
            pgup = pix[centri[stage][0], centri[stage][1] - 13]
            pgdx = pix[centri[stage][0] + 14, centri[stage][1]]
            pgsx = pix[centri[stage][0] - 13, centri[stage][1] + 1]
            pgdo = pix[centri[stage][0] + 1, centri[stage][1] + 14]

            if pgsx == (0, 0, 0) or pgsx == (5, 3, 0):
                #print("sx")
                sendChar(hwnd, "sx")
                stage += 1
                time.sleep(0.1)
            elif pgdx == (0, 0, 0) or pgdx == (5, 3, 0):
                #print("dx")
                sendChar(hwnd, "dx")
                stage += 1
                time.sleep(0.1)
            elif pgup == (0, 0, 0) or pgup == (5, 3, 0):
                #print("up")
                sendChar(hwnd, "up")
                stage += 1
                time.sleep(0.1)
            elif pgdo == (0, 0, 0) or pgdo == (5, 3, 0):
                #print("down")
                sendChar(hwnd, "down")
                stage += 1
                time.sleep(0.1)

        else:               #pesci normali
            psx = pix[816, 508]
            pdx = pix[1101, 508]
            pup = pix[980, 460]
            pdo = pix[930, 566]

            if psx == (255, 237, 118):
                #print("sx")
                sendChar(hwnd, "sx", 0.45)
                time.sleep(0.07)
            elif pdx == (255, 237, 118):
                #print("dx")
                sendChar(hwnd, "dx", 0.45)
                time.sleep(0.07)
            elif pup == (255, 237, 118):
                #print("up")
                sendChar(hwnd, "up", 0.45)
                time.sleep(0.07)
            elif pdo == (255, 237, 118):
                #print("down")
                sendChar(hwnd, "down", 0.45)
                time.sleep(0.07)

def sendChar(hwnd, char, sleep = 0):
    if char == "up":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x26, 0)
        time.sleep(sleep)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x26, 0)
    elif char == "down":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x28, 0)
        time.sleep(sleep)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x28, 0)
    elif char == "dx":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x27, 0)
        time.sleep(sleep)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x27, 0)
    elif char == "sx":
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x25, 0)
        time.sleep(sleep)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x25, 0)

def click(hwnd, x, y):
    pos = (y << 16) + x
    win32api.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, pos)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 1, pos)
    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, pos)



if __name__ == '__main__':
    main()
