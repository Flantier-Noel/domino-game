import tkinter
import _frontEnd

def play():
    pl1_sc, pl2_sc = 0, 0
    Nr = 1

    root = tkinter.Tk()
    width, height = 800, 500
    cnv = tkinter.Canvas(root, width=width, height=height, bg = '#663d01')
    rad = 10
    cnv.create_rectangleRound(rad, rad, width-rad*0.7, height-rad*0.7, rad, fill='#076e01')

    _frontEnd.round(cnv, Nr, pl1_sc, pl2_sc)

    cnv.pack()
    root.mainloop()