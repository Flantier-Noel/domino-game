import tkinter 
from math import cos, sin, pi
import _backEnd

def create_rectangleRound(cnv, x1, y1, x2, y2, rad, *args, **kwargs):
    Nresol = 20
    pts_lu = [(x1+rad+rad*cos(pi*k/Nresol/2), y1+rad-rad*sin(pi*k/Nresol/2)) for k in range(Nresol, 2*Nresol)]
    pts_ld = [(x1+rad+rad*cos(pi*k/Nresol/2), y2-rad-rad*sin(pi*k/Nresol/2)) for k in range(2*Nresol, 3*Nresol)]
    pts_rd = [(x2-rad+rad*cos(pi*k/Nresol/2), y2-rad-rad*sin(pi*k/Nresol/2)) for k in range(3*Nresol, 4*Nresol)]
    pts_ru = [(x2-rad+rad*cos(pi*k/Nresol/2), y1+rad-rad*sin(pi*k/Nresol/2)) for k in range(4*Nresol, 5*Nresol)]
    pts = pts_lu + pts_ld + pts_rd +pts_ru
    return cnv.create_polygon(pts, *args, **kwargs)
tkinter.Canvas.create_rectangleRound = create_rectangleRound

def create_domino(cnv, x1, y1, dom, visible=True, *arg, **kwarg):
    ids = []
    ids.append( cnv.create_rectangleRound(x1, y1, x1+23, y1+46, 2, fill='#ebe3d8', outline='#000') )
    ids.append( cnv.create_line(x1, y1+23, x1+23, y1+23, fill='#000') )
    if visible :
        dots = [[],
                [(9, 9)],
                [(2, 2), (16, 16)],
                [(2, 2), (9, 9), (16, 16)],
                [(2, 2), (2, 16), (16, 2), (16, 16)],
                [(2, 2), (2, 16), (16, 2), (9, 9), (16, 16)],
                [(2, 2), (2, 9), (2, 16), (16, 2), (16, 9), (16, 16)]]

        v0 = dom.val0
        for (dx, dy) in dots[v0]: ids.append( cnv.create_oval(x1+dx, y1+dy, x1+dx+5, y1+dy+5, fill='#000') )
        v1 = dom.val1
        for (dx, dy) in dots[v1]: ids.append( cnv.create_oval(x1+dx, y1+dy+23, x1+dx+5, y1+dy+5+23, fill='#000') )
        return ids
tkinter.Canvas.create_domino = create_domino

def display_pl1(game, cnv, dom_pl1, width, height):
    N = len(game.player1)
    for cnv_id_lst in dom_pl1 :
        for cnv_id in cnv_id_lst : cnv.delete(cnv_id)
    dom_pl1 = []
    if N%2 == 0 :
        for i in range(-N//2, N//2) : dom_pl1.append( cnv.create_domino(width/2 + i*30, height-46, game.player1[i+N//2]) )
    else :
        for i in range(-N//2, N//2) : dom_pl1.append( cnv.create_domino(width/2 + i*30 + 15, height-46, game.player1[i+N//2+1]) )
    return dom_pl1


def display_pl2(game, cnv, dom_pl2, width):
    N = len(game.player2)
    for cnv_id in dom_pl2 : cnv.delete(cnv_id)
    dom_pl2 = []
    if N%2 == 0 :
        for i in range(-N//2, N//2) : dom_pl2.append( cnv.create_domino(width/2 + i*30, -10, None, visible=False) )
    else :
        for i in range(-N//2, N//2) : dom_pl2.append( cnv.create_domino(width/2 + i*30 + 15, -10, None, visible=False) )
    return dom_pl2

def choose_pl1(event, game, cnv, choosen, dom_pl1, width, height):
    N = len(game.player1)
    x, y = event.x, event.y
    if N%2 == 0 :
        i = int( (x-width/2)//30 + N//2 )
    if 0 <= i < N and y >= height-46 :
        for j in range(len(dom_pl1)):
            cnv_ids = dom_pl1[j]
            for ids in cnv_ids :
                if i != choosen :
                    if j == i :
                        if choosen == -1 : cnv.move(ids, 0, -5)
                        else :  cnv.move(ids, 0, -10)
                    else :
                        if choosen == -1 : cnv.move(ids, 0, 5)
                        elif j == choosen : cnv.move(ids, 0, 10)
        choosen = i
    elif choosen != -1 :
        for j in range(len(dom_pl1)):
            cnv_ids = dom_pl1[j]
            for ids in cnv_ids :
                if j == choosen : cnv.move(ids, 0, 5)
                else : cnv.move(ids, 0, -5)
        choosen = -1

    return choosen, dom_pl1

def place_pl1(event, game, cnv, dom, place_id, choosen, width, height, g_rep):
    [(xl, yl, orientl, doml), (xr, yr, orientr, domr)] = g_rep
    x, y = event.x, event.y
    if place_id != None : cnv.delete(place_id)
    if choosen :
        dposR = {'RR':(46, 0, 92, 23), 'RL':None , 'RU':(23, 23, 46, 69), 'RD':(23, 0, 46, -46), 'RB':(46, -11.5, 69, 34.5),
                'LR':None, 'LL':(0, 0, -46, 23), 'LU':(0, 23, 23, 69), 'LD':(0, 0, 23, -46), 'LB':(0, -11.5, -23, 34.5),
                'UR':(23, 23, 69, 46), 'UL':(0, 23, -46, 46), 'UU':(0, 46, 23, 92), 'UD':None, 'UB':(-11.5, 46, 34.5, 69),
                'DR':(23, 0, 69, 23), 'DL':(0, 0, -46, 23), 'DU':None, 'DD':(0,0, 23, -46), 'DB':(-11.5, 0, 34.5, -23),
                'BR':(23, 11.5, 69, 34.5), 'BL':(0, 11.5, -46, 34.5), 'BU':(11.5, 23, 34.5, 69), 'BD':(11.5, 0, 34.5, -46), 'BB':None}

        dposL = {'RR':(0, 0, -46, 23), 'RL':None , 'RU':(0, 23, 23, 69), 'RD':(0, 0, 23, -46), 'RB':(-23, -11.5, 0, 34.5),
                'LR':None, 'LL':(46, 0, 92, 23) , 'LU':(23, 23, 46, 69), 'LD':(23, 0, 46, -46), 'LB':(46, -11.5, 69, 34.5),
                'UR':(23, 0, 69, 23), 'UL':(0, 0, -46, 23), 'UU':(0,0, 23, -46), 'UD':None, 'UB':(-11.5, 0, 34.5, -23),
                'DR':(23, 23, 69, 46), 'DL':(0, 23, -46, 46), 'DU':None, 'DD':(0, 46, 23, 92), 'DB':(-11.5, 46, 34.5, 69),
                'BR':(23, 11.5, 69, 34.5), 'BL':(0, 11.5, -46, 34.5), 'BU':(11.5, 23, 34.5, 69), 'BD':(11.5, 0, 34.5, -46), 'BB':None} ## B_ ?

        if dom.val0 == dom.val1 :
            if dom.val1 == domr.val1 :
                if dposR[orientr+'B'] != None :
                    (x1, y1, x2, y2) = dposR[orientr+'B']
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return cnv.create_rectangeRound(x1, y1, x2, y2, 2, outline='#f00'), (x1, y1, x2, y2), 1, 'B'
            if dom.val0 == doml.val0 :
                if dposL[orientl+'B' != None] :
                    (x1, y1, x2, y2) = dposL[orientl+'B']
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return cnv.create_rectangeRound(x1, y1, x2, y2, 2, outline='#f00'), (x1, y1, x2, y2), 0, 'B'


        for or2 in ['R', 'L', 'U', 'D']:
            if dom.val0 == domr.val1 or dom.val1 == domr.val1 :
                if dposR[orientr+or2] != None :
                    (x1, y1, x2, y2) = dposR[orientr+or2]
                    if x1 <= x <= x2 and y1 <= y <= y2:
                        return cnv.create_rectangeRound(x1, y1, x2, y2, 2, outline='#f00'), (x1, y1, x2, y2), 1, or2
            if dom.val0 == doml.val0 or dom.val1 == doml.val0 :
                if dposL[orientl+or2] != None :
                    (x1, y1, x2, y2) = dposL[orientr+or2]
                    if x1 <= x <= x2 and y1 <= y <= y2 :
                        return cnv.create_rectangeRound(x1, y1, x2, y2, 2, outline='#f00'), (x1, y1, x2, y2), 0, or2


def display_dom(dom, pos, orient, cnv, g_rep):
    _, x0, y0 = g_rep[pos]
    cnv.create_domino()

def play_Dom(dom, pos, game, cnv, g_rep, height, width):
    if len(game.played)==0 :
        xc, yc = width/2, height/2
        display_dom(dom, pos, 1, cnv, g_rep)
        g_rep = [(dom.val0, xc-23, yc+12.5), (dom.val1, xc+23, yc+12.5)]
    game.play(dom, pos)

def round(Nr, sc1, sc2):
    game = _backEnd.Game()
    g_rep = [(), ()]
    if Nr == 1 :
        jid, (i, j) = game.greater_1stdom()
        game.current_play = jid
        play_Dom(_backEnd.Domino(i,j), 0, game, cnv, g_rep)

    root = tkinter.Tk()
    width, height = 800, 500
    cnv = tkinter.Canvas(root, width=width, height=height, bg = '#663d01')
    rad = 10
    cnv.create_rectangleRound(rad, rad, width-rad*0.7, height-rad*0.7, rad, fill='#076e01')

    global dom_pl1
    dom_pl1 = []
    def display_pl1_0():
        global dom_pl1
        dom_pl1 = display_pl1(game, cnv, dom_pl1, width, height)

    global dom_pl2
    dom_pl2 = []
    def display_pl2_0():
        global dom_pl2
        dom_pl2 = display_pl2(game, cnv, dom_pl2, width)

    global choosen
    choosen = -1
    def choose_pl1_0(event):
        global choosen, dom_pl1
        choosen, dom_pl1 = choose_pl1(event, game, cnv, choosen, dom_pl1, width, height)

    display_pl2_0()
    display_pl1_0()

    cnv.bind('<Button-1>', choose_pl1_0)

    cnv.pack()
    root.mainloop()
