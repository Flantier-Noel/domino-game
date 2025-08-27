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

def create_domino(cnv, x1, y1, dom, visible=True, orient='vertical', switch=False, *arg, **kwarg):
    ids = []
    if orient == 'vertical' : 
        ids.append( cnv.create_rectangleRound(x1, y1, x1+23, y1+46, 2, fill='#ebe3d8', outline="#29272e") )
        ids.append( cnv.create_line(x1, y1+23, x1+23, y1+23, fill='#29272e') )
    if orient == 'horizontal' :
        ids.append( cnv.create_rectangleRound(x1, y1, x1+46, y1+23, 2, fill='#ebe3d8', outline='#29272e') )
        ids.append( cnv.create_line(x1+23, y1, x1+23, y1+23, fill='#29272e') )
    if visible :
        dots = [[],
                [(9, 9)],
                [(2, 2), (16, 16)],
                [(2, 2), (9, 9), (16, 16)],
                [(2, 2), (2, 16), (16, 2), (16, 16)],
                [(2, 2), (2, 16), (16, 2), (9, 9), (16, 16)],
                [(2, 2), (2, 9), (2, 16), (16, 2), (16, 9), (16, 16)]]

        v0, v1 = dom.val0, dom.val1
        if switch : v0, v1 = v1, v0

        for (dx, dy) in dots[v0]: ids.append( cnv.create_oval(x1+dx, y1+dy, x1+dx+5, y1+dy+5, fill='#29272e') )
        if orient == 'vertical' : 
            for (dx, dy) in dots[v1]: ids.append( cnv.create_oval(x1+dx, y1+dy+23, x1+dx+5, y1+dy+5+23, fill='#29272e') )
        if orient == 'horizontal' :
            for (dx, dy) in dots[v1]: ids.append( cnv.create_oval(x1+dx+23, y1+dy, x1+dx+5+23, y1+dy+5, fill='#29272e') ) 
            
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
    if N%2 == 0 : i = int( (x-width/2)//30 + N//2 )
    else : i = int( (x-width/2 + 15)//30 + N//2 )
    
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

    return choosen, dom_pl1, game.player1[choosen]

def place_pl1(event, game, cnv, dom, place_id, choosen, width, height, g_rep):
    x, y = event.x, event.y
    if place_id != None : cnv.delete(place_id)
    if choosen != -1 :
        if len(game.played) == 0 : 
            xc, yc = width/2, height/2
            if dom.val0 == dom.val1 :
                x1, y1, x2, y2 = xc-11.5, yc-23, xc+11.5, yc+23
                if x1 <= x <= x2 and y1 <= y <= y2 :
                    return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 1, 'B'
            else :
                x1, y1, x2, y2 = xc-23, yc-11.5, xc+23, yc+11.5
                if x1 <= x <= x2 and y1 <= y <= y2 :
                    return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 1, 'R'

        else :    
            [(xl, yl, orientl, doml), (xr, yr, orientr, domr)] = g_rep
            dposR = {'RR':(46, 0, 92, 23), 'RL':None , 'RU':(23, 23, 46, 69), 'RD':(23, 0, 46, -46), 'RB':(46, -11.5, 69, 34.5),
                    'LR':None, 'LL':(0, 0, -46, 23), 'LU':(0, 23, 23, 69), 'LD':(0, 0, 23, -46), 'LB':(0, -11.5, -23, 34.5),
                    'UR':(23, 23, 69, 46), 'UL':(0, 23, -46, 46), 'UU':(0, 46, 23, 92), 'UD':None, 'UB':(-11.5, 46, 34.5, 69),
                    'DR':(23, 0, 69, 23), 'DL':(0, 0, -46, 23), 'DU':None, 'DD':(0,0, 23, -46), 'DB':(-11.5, 0, 34.5, -23),
                    'BR':(23, 11.5, 69, 34.5), 'BL':(0, 11.5, -46, 34.5), 'BU':(11.5, 23, 34.5, 69), 'BD':(11.5, 0, 34.5, -46), 'BB':None}

            dposL = {'RR':(0, 0, -46, 23), 'RL':None , 'RU':(0, 23, 23, 69), 'RD':(0, 0, 23, -46), 'RB':(-23, -11.5, 0, 34.5),
                    'LR':None, 'LL':(46, 0, 92, 23) , 'LU':(23, 23, 46, 69), 'LD':(23, 0, 46, -46), 'LB':(46, -11.5, 69, 34.5),
                    'UR':(23, 0, 69, 23), 'UL':(0, 0, -46, 23), 'UU':(0,0, 23, -46), 'UD':None, 'UB':(-11.5, 0, 34.5, -23),
                    'DR':(23, 23, 69, 46), 'DL':(0, 23, -46, 46), 'DU':None, 'DD':(0, 46, 23, 92), 'DB':(-11.5, 46, 34.5, 69),
                    'BR':(23, 11.5, 69, 34.5), 'BL':(0, 11.5, -46, 34.5), 'BU':(11.5, 23, 34.5, 69), 'BD':(11.5, 0, 34.5, -46), 'BB':None}

            if dom.val0 == dom.val1 :
                if dom.val1 == domr.val1 :
                    if dposR[orientr+'B'] != None :
                        (x10, y10, x20, y20) = dposR[orientr+'B']
                        x1, y1, x2, y2 = x10+xr, y10+yr, x20+xr, y20+yr
                        if min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                            return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 1, 'B'
                if dom.val0 == doml.val0 :
                    if dposL[orientl+'B'] != None :
                        (x10, y10, x20, y20) = dposL[orientl+'B']
                        x1, y1, x2, y2 = x10+xl, y10+yl, x20+xl, y20+yl
                        if min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                            return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 0, 'B'

            for or2 in ['R', 'L', 'U', 'D']:
                if dom.val0 == domr.val1 or dom.val1 == domr.val1 :
                    if dposR[orientr+or2] != None :
                        (x10, y10, x20, y20) = dposR[orientr+or2]
                        x1, y1, x2, y2 = x10+xr, y10+yr, x20+xr, y20+yr
                        if min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                            return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 1, or2
                if dom.val0 == doml.val0 or dom.val1 == doml.val0 :
                    if dposL[orientl+or2] != None :
                        (x10, y10, x20, y20) = dposL[orientr+or2]
                        x1, y1, x2, y2 = x10+xl, y10+yl, x20+xl, y20+yl
                        if min(x1,x2) <= x <= max(x1,x2) and min(y1,y2) <= y <= max(y1,y2):
                            return cnv.create_rectangleRound(x1, y1, x2, y2, 2, outline='#ff2b2b', fill=''), (x1, y1, x2, y2), 0, or2

def play_Dom(dom, pos, orient, game, cnv, g_rep, height, width):
    if len(game.played) == 0 :
        xc, yc = width/2, height/2
        if dom.val0 == dom.val1 :
            cnv.create_domino(xc-11.5, yc-23, dom)
            g_rep = [(xc-11.5, yc-23, 'B', dom), (xc-11.5, yc-23, 'B', dom)]
        else :
            cnv.create_domino(xc-23, yc-11.5, dom, orient='horizontal')
            g_rep = [(xc-23, yc-11.5, 'R', dom), (xc-23, yc-11.5, 'R', dom)]
        game.play(dom, pos)
        return game, g_rep

    (x0, y0, orient0, dom0) = g_rep[pos]

    dposR = {'RR':(46, 0), 'RL':None , 'RU':(23, 23), 'RD':(23, -46), 'RB':(46, -11.5),
            'LR':None, 'LL':(-46, 0), 'LU':(0, 23), 'LD':(0, -46), 'LB':(-23, -11.5),
            'UR':(23, 23), 'UL':(-46, 23), 'UU':(0, 46), 'UD':None, 'UB':(-11.5, 46),
            'DR':(23, 0), 'DL':(-46, 0), 'DU':None, 'DD':(0, -46), 'DB':(-11.5, -23),
            'BR':(23, 11.5), 'BL':(-46, 11.5), 'BU':(11.5, 23), 'BD':(11.5, -46), 'BB':None}

    dposL = {'RR':(-46, 0), 'RL':None , 'RU':(0, -46), 'RD':(0, 23), 'RB':(-23, -11.5),
            'LR':None, 'LL':(46, 0) , 'LU':(23, -46), 'LD':(23, 23), 'LB':(46, -11.5),
            'UR':(-46, 0), 'UL':(23, 0), 'UU':(0, -46), 'UD':None, 'UB':(-11.5, 23),
            'DR':(-46, 23), 'DL':(23, 23), 'DU':None, 'DD':(0, 46), 'DB':(-11.5, 46),
            'BR':(23, 11.5), 'BL':(-46, 11.5), 'BU':(11.5, 23), 'BD':(11.5, -46), 'BB':None}

    if pos : (dx, dy) = dposL[orient0+orient]
    else : (dx, dy) = dposR[orient0+orient]

    if orient in ['R', 'L'] : orient_abs = 'horizontal'
    if orient in ['U', 'D'] : orient_abs = 'vertical'
    if orient == 'B' :
        if orient0 in ['R', 'L'] : orient_abs = 'vertical'
        if orient0 in ['U', 'D'] : orient_abs = 'horizontal'
    
    if pos :
        if dom.val0 == dom0.val1 : switch = False
        if dom.val1 == dom0.val1 : switch = True
    else :
        if dom.val0 == dom0.val0 : switch = True
        if dom.val1 == dom0.val0 : switch = False
    ids = cnv.create_domino(x0, y0, dom, orient=orient_abs, switch=switch)
    for item in ids : cnv.move(item, dx, dy)

    game.play(dom, pos)
    g_rep[pos] = (x0+dx, y0+dy, orient, dom.copy())
    return game, g_rep

def round(cnv, Nr, sc1, sc2):
    width, height = float(cnv['width']), float(cnv['height'])
    Nlayer = 2

    global game, g_rep
    game = _backEnd.Game()
    g_rep = [(), ()]
    if Nr == 1 :
        jid, (i, j) = game.greater_1stdom()
        game.current_play = jid
        game, g_rep = play_Dom(_backEnd.Domino(i,j), 0, '' , game, cnv, g_rep, height, width)

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

    global choosen, dom_choose
    choosen = -1
    dom_choose = None
    def choose_pl1_0(event):
        global choosen, dom_pl1, dom_choose, game, g_rep, id_sel, coord_sel, pos_sel, ort_sel
        if id_sel != None :
            print(choosen, game.player1[choosen])
            game, g_rep = play_Dom(game.player1[choosen], pos_sel, ort_sel , game, cnv, g_rep, height, width)
            id_sel = None ; choosen = -1
            display_pl1_0()

        if game.current_play == 1 :
            mvs = game.best_moves(Nlayer)
            dom, pos = mvs[0][0]
            _, _, orient0, _ = g_rep[pos] ## D should be modified ...
            play_Dom(dom, pos, orient0, game, cnv, g_rep, height, width)

        choosen, dom_pl1, dom_choose = choose_pl1(event, game, cnv, choosen, dom_pl1, width, height)

    display_pl2_0()
    display_pl1_0()

    global id_sel, coord_sel, pos_sel, ort_sel
    id_sel, coord_sel, pos_sel, ort_sel = None, None, None, None

    def select_pl1_0(event):
        global choosen, dom_choose, id_sel, coord_sel, pos_sel, ort_sel
        if choosen != -1 :
            u = place_pl1(event, game, cnv, dom_choose, id_sel, choosen, width, height, g_rep)
            if u != None : id_sel, coord_sel, pos_sel, ort_sel = u

    cnv.bind('<Button-1>', choose_pl1_0)
    cnv.bind('<Motion>', select_pl1_0)