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

def let_play():
    root = tkinter.Tk()
    width, height = 800, 500
    cnv = tkinter.Canvas(root, width=width, height=height, bg = '#663d01')
    rad = 10
    cnv.create_rectangleRound(rad, rad, width-rad*0.7, height-rad*0.7, rad, fill='#076e01')

    game = _backEnd.Game()

    global dom_pl2
    dom_pl2 = []
    def display_pl2():
        global dom_pl2
        N = len(game.player2)
        for cnv_id in dom_pl2 : cnv.delete(cnv_id)
        dom_pl2 = []
        if N%2 == 0 :
            for i in range(-N//2, N//2) : dom_pl2.append( cnv.create_domino(width/2 + i*30, -10, None, visible=False) )
        else :
            for i in range(-N//2, N//2) : dom_pl2.append( cnv.create_domino(width/2 + i*30 + 15, -10, None, visible=False) )

    global dom_pl1
    dom_pl1 = []
    def display_pl1():
        global dom_pl1
        N = len(game.player1)
        for cnv_id_lst in dom_pl1 :
            for cnv_id in cnv_id_lst : cnv.delete(cnv_id)
        dom_pl1 = []
        if N%2 == 0 :
            for i in range(-N//2, N//2) : dom_pl1.append( cnv.create_domino(width/2 + i*30, height-46, game.player1[i+N//2]) )
        else :
            for i in range(-N//2, N//2) : dom_pl1.append( cnv.create_domino(width/2 + i*30 + 15, height-46, game.player1[i+N//2+1]) )

    global choosen
    choosen = -1
    def choose_pl1(event):
        global choosen, dom_pl1
        N = len(game.player1)
        x, y = event.x, event.y
        print(x, y)
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

    display_pl2()
    display_pl1()

    cnv.bind('<Button-1>', choose_pl1)

    cnv.pack()
    root.mainloop()
