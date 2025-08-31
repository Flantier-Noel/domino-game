import random

class Domino() :
    class NoneDomino():
        def __init__(self):
            self.val0, self.val1 = None, None
        def __hash__(self): return hash(None)
        def __repr__(self): return 'NoneDomino'
        def __eq__(self, item): return isinstance(item, Domino.NoneDomino)
        def __gt__(self, item): return True
        def __lt__(self, item): return True

    def __init__(self, val0, val1):
        self.val0 = val0
        self.val1 = val1

    def __hash__(self):
        return hash((self.val0, self.val1))

    def __repr__(self):
        return str((self.val0, self.val1))

    def __eq__(self, dom):
        dir0 = (self.val0 == dom.val0 and self.val1 == dom.val1)
        dir1 = (self.val0 == dom.val1 and self.val1 == dom.val0)
        return (dir0 or dir1)

    def __gt__(self, dom):
        if self.val1 == dom.val0 : return True
        if self.val0 == dom.val0 :
            self.val0, self.val1 = self.val1, self.val0
            return True
        return False

    def __lt__(self, dom):
        if self.val0 == dom.val1 : return True
        if self.val1 == dom.val1 :
            self.val0, self.val1 = self.val1, self.val0
            return True
        return False

    def __int__(self):
        return self.val0 + self.val1
    
    def copy(self):
        return Domino(self.val0, self.val1)

class Game():
    def __init__(self):
        self.avail_doms = {Domino(i,j):True for i in range(7) for j in range(7) if i<=j}
        dom = list(self.avail_doms.keys())
        random.shuffle(dom)
        self.player1, self.player2 = dom[:8], dom[8:16]
        for d in self.player2: self.avail_doms[d] = False
        self.played = {}
        self.range = [0,0]
        self.current_play = 0

    def copy(self):
        game_copy = Game()
        game_copy.avail_doms   = self.avail_doms.copy()
        game_copy.player1      = self.player1.copy()
        game_copy.player2      = self.player2.copy()
        game_copy.played       = self.played.copy()
        game_copy.range        = self.range.copy()
        game_copy.current_play = self.current_play
        return game_copy

    def greater_1stdom(self):
        for i in range(6, -1, -1):
            for j in range(i, -1, -1):
                if Domino(i, j) in self.player1 : return 0, (i,j)
                if Domino(i, j) in self.player2 : return 1, (i,j)

    def play(self, dom, relat_pos):
        if isinstance(dom, Domino.NoneDomino) : 
            self.current_play = (self.current_play + 1)%2
            return True
        player = [self.player1, self.player2][self.current_play]
        if dom in player :
            ind = player.index(dom)
            if len(self.played)==0 or (relat_pos == 0 and dom > self.played[self.range[0]]) or (relat_pos == 1 and dom < self.played[self.range[1]]) :
                    self.avail_doms[dom] = False
                    self.current_play = (self.current_play + 1)%2
                    self.range[relat_pos] += 2*relat_pos-1
                    if len(self.played)==0 : self.range[(relat_pos+1)%2] += 2*relat_pos-1
                    self.played[self.range[relat_pos]] = dom
                    if self.current_play == 1 : self.player1.pop(ind)
                    else : self.player2.pop(ind)
                    return True
            else : return False
        else : return False

    def rate(self):
        avail_doms = sorted([int(dom) for dom in self.avail_doms.keys() if dom in self.avail_doms.keys() and self.avail_doms[dom]])
        p1_val_max = sum(avail_doms[:len(self.player2)])
        p1_val_min = sum(avail_doms[len(self.player2):])  # min([int(dom) for dom in self.avail_doms.keys() if self.avail_doms[dom]])
        p2_val = sum([int(dom) for dom in self.player2])
        return (p1_val_min + len(self.player2) + 1)/(p1_val_max + len(self.player2) + p2_val + 1)

    def all_moves(self, Nlayer):
        if Nlayer == 1 :
            moves = []
            for dom in self.player2 :
                for pos in range(2):
                    if len(self.played)==0 or (pos == 0 and dom > self.played[self.range[0]]) or (pos == 1 and dom < self.played[self.range[1]]) :
                        moves.append([(dom, pos)])
            if len(moves) == 0 : return [[(Domino.NoneDomino(), -1)]]
            return moves

        moves_p2 = []
        for dom_p2 in self.player2 :
            for pos_p2 in range(2):
                game_copy = self.copy()
                valid = game_copy.play(dom_p2, pos_p2)
                if valid : moves_p2.append((dom_p2, pos_p2, game_copy))
        if len(moves_p2) == 0 : moves_p2.append((Domino.NoneDomino(), -1, self.copy()))

        moves = []
        for (dom2, pos2, game) in moves_p2 :
            moves_p1 = []
            for dom_p1 in game.avail_doms.keys():
                for pos_p1 in range(2):
                    game_copy = game.copy()
                    valid = game_copy.play(dom_p1, pos_p1)
                    if valid : moves_p1.append((dom2, pos2, game_copy))
            if len(moves_p1) == 0 : moves_p2.append((Domino.NoneDomino(), -1, game.copy()))
            for (dom1, pos1, game) in moves_p1 :
                next_moves = game.all_moves(Nlayer-1)
                for mvs in next_moves :
                    mvs = mvs.copy()
                    mvs = [(dom2, pos2), (dom1, pos1)]+mvs
                    moves.append(mvs)

        return moves

    def best_moves(self, Nlayer):
        moves = self.all_moves(Nlayer)
        def sort_fun(lst):
            game_copy = self.copy()
            for mv in lst : game_copy.play(*mv)
            return game_copy.rate() 
        moves.sort(key = sort_fun)
        return moves[::-1]