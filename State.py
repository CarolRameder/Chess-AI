from Move import Move

class CastleRights:
    """
    Class for representing a castle move
    """

    def __init__(self, wks, bks, wqs, bqs):
        """
        Constructor method for castle representation
        :parameter wks - white king side
        :parameter bks - black king side
        :parameter wqs - white queen side
        :parameter bqs - black queen side
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class GameState:
    """
    Class to represent the current state of the board
    """

    def __init__(self):
        """
        Constructor method
        """
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "bp", "--", "--", "--", "--"],
        #     ["wk", "wp", "bp", "--", "--", "--", "--", "br"],
        #     ["--", "wr", "--", "--", "--", "bp", "--", "bk"],
        #     ["--", "--", "--", "--", "wp", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "wp", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"]
        # ]
        self.turn_white = True
        self.moveLog = []
        self.wKingPos = (7, 4)
        self.bKingPos = (0, 4)

        #advanced version
        self.inCheck=False
        self.pins = []
        self.checks = []

        #ends
        self.checkMate = False
        self.staleMate = False

        #rights
        self.enpas_pos = ()
        self.enpas_log=[self.enpas_pos]
        self.cr_castle_r = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.cr_castle_r.wks, self.cr_castle_r.bks,
                                             self.cr_castle_r.wqs, self.cr_castle_r.bqs)]

    def make_move(self, move, check_valid=True):
        """
        Check valid indicates if the move is generated for check validation and pins, or it's a real move
        :parameter move - object representing the move to be made
        :parameter check_valid - flag for validity of the move based on actual use in the game
        """
        self.board[move.sr][move.sc] = "--"
        self.board[move.er][move.ec] = move.pieceMoved
        self.moveLog.append(move)
        self.turn_white = not self.turn_white
        if move.pieceMoved == 'wk':
            self.wKingPos = (move.er, move.ec)
        elif move.pieceMoved == 'bk':
            self.bKingPos = (move.er, move.ec)

        if move.isEnpassantMove:
            self.board[move.sr][move.ec] = "--"

        if move.pieceMoved[1] == 'p' and abs(move.sr - move.er) == 2:
            self.enpas_pos = ((move.er + move.sr) // 2, move.ec)
        else:
            self.enpas_pos = ()

        if move.isPawnPromotion and not check_valid:
            promoted_piece = "a"
            while promoted_piece not in ('q', 'r', 'b', 'n'):
                promoted_piece = input("Promote to q, r, b, or n: ")
            self.board[move.er][move.ec] = move.pieceMoved[0] + promoted_piece

        # castle
        if move.castle:
            if move.ec - move.sc == 2:
                self.board[move.er][move.ec - 1] = self.board[move.er][move.ec + 1]
                self.board[move.er][move.ec + 1] = '--'
            else:
                self.board[move.er][move.ec + 1] = self.board[move.er][move.ec - 2]
                self.board[move.er][move.ec - 2] = '--'

        self.enpas_log.append(self.enpas_pos)
        # castle rights on rook, king move
        self.update_castle_rights(move)
        self.castleRightsLog.append(CastleRights(self.cr_castle_r.wks, self.cr_castle_r.bks,
                                                 self.cr_castle_r.wqs, self.cr_castle_r.bqs))

    def update_castle_rights(self, move):
        """
        Method to update the castle move posibilities for both colours
        :parameter move - the move performed to be cheked against
        """
        #deleting the right to castle on moving k/r
        #King
        if move.pieceMoved == 'wk':
            self.cr_castle_r.wks = False
            self.cr_castle_r.wqs = False
        elif move.pieceMoved == 'bk':
            self.cr_castle_r.bks = False
            self.cr_castle_r.bqs = False

        #Rook
        #moved
        elif move.pieceMoved == 'wr':
            if move.sr == 7:
                if move.sc == 0:
                    self.cr_castle_r.wqs = False
                elif move.sc == 7:
                    self.cr_castle_r.wks = False
        elif move.pieceMoved == 'br':
            if move.sr == 0:
                if move.sc == 0:
                    self.cr_castle_r.bqs = False
                elif move.sc == 7:
                    self.cr_castle_r.bks = False

        #captured
        if move.pieceCaptured=='wr':
            if move.er==7:
                if move.ec==0:
                    self.cr_castle_r.wqs=False
                elif move.ec==7:
                    self.cr_castle_r.wks=False
        elif move.pieceCaptured=='br':
            if move.er==0:
                if move.ec==0:
                    self.cr_castle_r.bqs=False
                elif move.ec==7:
                    self.cr_castle_r.bks=False

    def undo_move(self):
        """
        Method for undoing the moves made during the game
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.sr][move.sc] = move.pieceMoved
            self.board[move.er][move.ec] = move.pieceCaptured
            self.turn_white = not self.turn_white

            # king pos
            if move.pieceMoved == 'wk':
                self.wKingPos = (move.sr, move.sc)
            elif move.pieceMoved == 'bk':
                self.bKingPos = (move.sr, move.sc)

            # enpassant
            if move.isEnpassantMove:
                self.board[move.er][move.ec] = "--"
                self.board[move.sr][move.ec] = move.pieceCaptured

            self.enpas_log.pop()
            self.enpas_pos=self.enpas_log[-1]

            # castle rights
            self.castleRightsLog.pop()
            upd_rights = self.castleRightsLog[-1]
            self.cr_castle_r=CastleRights(upd_rights.wks, upd_rights.bks, upd_rights.wqs, upd_rights.bqs)

            # castle moves
            if move.castle:
                if move.ec - move.sc == 2:
                    self.board[move.er][move.ec + 1] = self.board[move.er][move.ec - 1]
                    self.board[move.er][move.ec - 1] = '--'
                else:
                    self.board[move.er][move.ec - 2] = self.board[move.er][move.ec + 1]
                    self.board[move.er][move.ec + 1] = '--'

            self.checkMate = False
            self.staleMate = False

    def square_under_attack(self, r, c):
        """
        Checking if a certain square is under attack
        :param r: row of the square
        :param c: column of the square
        :return: boolean if the square is under attack
        """""
        self.turn_white = not self.turn_white
        opp_moves = self.get_all_possible_moves()
        self.turn_white = not self.turn_white
        for move in opp_moves:
            if move.er == r and move.ec == c:
                return True
        return False

    def in_check(self):
        """
        Method for checking if the any of the kings are in check
        """
        if self.turn_white:
            return self.square_under_attack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.square_under_attack(self.bKingPos[0], self.bKingPos[1])

    def search_checks_pins(self):
        pins=[]
        checks=[]
        inCheck=False
        if self.turn_white:
            enemy="b"
            ally="w"
            sr=self.wKingPos[0]
            sc=self.wKingPos[1]
        else:
            enemy = "w"
            ally = "b"
            sr = self.bKingPos[0]
            sc = self.bKingPos[1]

        dir = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(dir)):
            d=dir[j]
            pos_pin=()
            for i in range(1,8):
                er=sr+d[0]*i
                ec=sc+d[1]*i
                if 0 <= er < 8 and 0 <= ec < 8:
                    end_piece=self.board[er][ec]
                    if end_piece[0] == ally and end_piece[1]!='k':
                        if pos_pin==():
                            pos_pin=(er,ec,d[0],d[1])
                        else:
                            break
                    elif end_piece[0]==enemy:
                        type=end_piece[1]
                        #5 type theory 7.(m14)
                        if(0<=j<=3 and type =="r") or \
                                (4<=j<=7 and type =="b") or \
                                (i==1 and type=="p" and ((enemy=='w'and 6<=j<=7) or (enemy=='b' and 4<=j<=5))) or \
                                (type=='q') or (i==1 and type=='k'):
                            if pos_pin==():
                                inCheck=True
                                checks.append((er,ec,d[0],d[1]))
                                break
                            else:
                                pins.append(pos_pin)
                                break
                        else:
                            break
                else:
                    break
        #check knights
        k_dir = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in k_dir:
            er = sr + m[0]
            ec = sc + m[1]
            if 0<= er < 8 and 0 <= ec < 8:
                end_piece=self.board[er][ec]
                if end_piece[0] == enemy and end_piece[1]=='n':
                    inCheck=True
                    checks.append((er,ec,m[0],m[1]))
        return inCheck, pins, checks

    def get_valid_moves(self):
        """
        Method for computing all valid moves
        :return moves - a list of Move objects with all the valid moves
        """
        moves=[]
        self.inCheck, self.pins, self.checks=self.search_checks_pins()
        if self.turn_white:
            kingR=self.wKingPos[0]
            kingC=self.wKingPos[1]
        else:
            kingR = self.bKingPos[0]
            kingC = self.bKingPos[1]
        if self.inCheck:
            if len(self.checks)==1:
                moves=self.get_all_possible_moves()
                check=self.checks[0]
                checkR=check[0]
                checkC=check[1]
                pieceChecking=self.board[checkR][checkC]
                validSqs=[]
                if pieceChecking[1]=='n':
                    validSqs=[(checkR,checkC)]
                else:
                    for i in range(1,8):
                        validSq=(kingR+check[2]*i, kingC+check[3]*i)
                        validSqs.append(validSq)
                        if validSq[0]== checkR and validSq[1]==checkC:
                            break

                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != 'k':
                        if not (moves[i].er, moves[i].ec) in validSqs:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(kingR,kingC, moves)
        else:
            moves=self.get_all_possible_moves()

        return moves

    def get_all_possible_moves(self):
        """
        Method for getting a list of all the possible moves based on the rules of chess
        :return moves
        """
        moves = []
        for i in range(8):
            for j in range(8):
                color = self.board[i][j][0]
                if (color == 'b' and not self.turn_white) or (color == 'w' and self.turn_white):
                    p_type = self.board[i][j][1]
                    if p_type == 'r':
                        self.get_rook_moves(i, j, moves)
                    elif p_type == 'k':
                        self.get_king_moves(i, j, moves)
                    elif p_type == 'q':
                        self.get_queen_moves(i, j, moves)
                    elif p_type == 'p':
                        self.get_pawn_moves(i, j, moves)
                    elif p_type == 'b':
                        self.get_bishop_moves(i, j, moves)
                    elif p_type == 'n':
                        self.get_knight_moves(i, j, moves)
        return moves

    def get_rook_moves(self, i, j, moves):
        """
        Method for computing all the moves based on rock piece movement
        :parameter i - row on which the rock is
        :parameter j - column on which the rock is
        :parameter moves - list of all the possible moves
        """
        pinned=False
        pin_dir=()
        for k in range(len(self.pins)-1,-1,-1):
            if self.pins[k][0]==i and self.pins[k][1]==j:
                pinned=True
                pin_dir=(self.pins[k][2], self.pins[k][3])
                if self.board[i][j][1]!='q':
                    self.pins.remove(self.pins[k])
                break

        # the rook can move in 4 directions
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

        # player's turn are important de determine what pieces they can capture
        if self.turn_white:
            oponent_colour = 'b'
        else:
            oponent_colour = 'w'

        # all 4 directions are covered as long as the fields are empty
        for d in directions:
            for m in range(1, 8):
                er = i + d[0] * m
                ec = j + d[1] * m
                if 0 <= er < 8 and 0 <= ec < 8:  # check if the table ends
                    if not pinned or pin_dir==d or pin_dir == (-d[0], -d[1]):
                        # the landing square may be empty
                        if self.board[er][ec] == '--':
                            moves.append(Move((i, j), (er, ec), self.board))
                        # oponent_colour piece that may be captured
                        elif self.board[er][ec][0] == oponent_colour:
                            moves.append(Move((i, j), (er, ec), self.board))
                            break
                        # own piece
                        else:
                            break
                else:
                    break

    def get_king_moves(self, i, j, moves):
        """
        Method for computing all the moves based on king piece movement
        :parameter i - row on which the king is
        :parameter j - column on which the king is
        :parameter moves - list of all possible moves
        """
        row = (-1, -1, -1, 0, 0, 1, 1, 1)
        col = (-1, 0, 1, -1, 1, -1, 0, 1)

        if self.turn_white:
            ally = 'w'
        else:
            ally = 'b'

        for d in range(8):
            er = i + row[d]
            ec = j + col[d]
            if 0 <= er < 8 and 0 <= ec < 8:
                # empty
                if self.board[er][ec][0] != ally:
                    if ally=='w':
                        self.wKingPos = (er, ec)
                    else:
                        self.bKingPos = (er, ec)
                    inCheck, pins, checks=self.search_checks_pins()
                    if not inCheck:
                        moves.append(Move((i, j), (er, ec), self.board))
                    if ally=='w':
                        self.wKingPos = (i, j)
                    else:
                        self.bKingPos = (i, j)

    def get_castle_moves(self, r, c, moves):
        """
        Method for computing all castle moves
        :parameter r - row on which the move is being performed
        :parameter c - column on which the move is being performed
        :parameter moves - list of all possible moves
        """
        if self.square_under_attack(r, c):
            return

        #king side
        #checking previous rights and player turn
        if (self.cr_castle_r.wks and self.turn_white) or (self.cr_castle_r.bks and not self.turn_white):
            if self.board[r][c + 2] == '--' and self.board[r][c + 1] == '--':
                if self.square_under_attack(r, c + 2) is False and self.square_under_attack(r, c + 1) is False:
                    moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

        #queen side
        if (self.turn_white and self.cr_castle_r.wqs) or (not self.turn_white and self.cr_castle_r.bqs):
            if self.board[r][c - 2]== '--' and self.board[r][c - 1] == '--' and self.board[r][c - 3] == '--':
                if self.square_under_attack(r, c - 1) is False and self.square_under_attack(r, c - 2) is False:
                    moves.append(Move((r, c), (r, c - 2), self.board, castle=True))

    def get_bishop_moves(self, i, j, moves):
        """
        Method for computing all the moves based on king piece movement
        :param i: row on which the bishop is
        :param j: column on which the bishop is
        :param moves: list of all possible moves
        """
        pinned = False
        pin_dir = ()
        for k in range(len(self.pins) - 1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                pinned = True
                pin_dir = (self.pins[k][2], self.pins[k][3])
                self.pins.remove(self.pins[k])
                break
        directions = ((-1, 1), (1, -1), (1, 1), (-1, -1))
        if self.turn_white:
            oponent = 'b'
        else:
            oponent = 'w'

        for d in directions:
            for m in range(1, 8):
                cri = i + d[0] * m
                crj = j + d[1] * m
                if 0 <= cri <= 7 and 0 <= crj <= 7:
                    # empty
                    if not pinned or pin_dir == d or pin_dir == (-d[0], -d[1]):
                        if self.board[cri][crj][0] == '-':
                            moves.append(Move((i, j), (cri, crj), self.board))

                    # oponent
                        elif self.board[cri][crj][0] == oponent:
                            moves.append(Move((i, j), (cri, crj), self.board))
                            break
                    # piesa mea
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, i, j, moves):
        """
        Method for computing all the moves based on quenn piece movement
        :param i: row on which the queen is
        :param j: column on which the queen is
        :param moves: list of all the moves possible
        """
        self.get_rook_moves(i, j, moves)
        self.get_bishop_moves(i, j, moves)

    def get_knight_moves(self, i, j, moves):
        """
        Method for computing all the moves based on knight piece movement
        :param i: row on which knight is
        :param j: column on which knight is
        :param moves: list of all possible moves
        """
        pinned = False
        for k in range(len(self.pins) - 1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                pinned = True
                self.pins.remove(self.pins[k])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        if self.turn_white:
            ally = 'w'
        else:
            ally = 'b'

        for m in directions:
            er = i + m[0]
            ec = j + m[1]
            if 0 <= er < 8 and 0 <= ec < 8:
                # empty
                if not pinned:
                    ep=self.board[er][ec]
                    if ep[0] != ally:
                        moves.append(Move((i, j), (er, ec), self.board))

    def get_pawn_moves(self, i, j, moves):
        """
        Method for computing all the moves based on pawn piece movement
        :param i: row on which the pawn is
        :param j: column on which the pawn is
        :param moves: list of all the moves possible
        """
        pin=False
        pin_dir=()
        for k in range(len(self.pins)-1,-1,-1):
            if self.pins[k][0]== i and self.pins[k][1]==j:
                pin=True
                pin_dir=(self.pins[k][2], self.pins[k][3])
                self.pins.remove(self.pins[k])
                break

        if self.turn_white:
            move_dir=-1
            sr=6
            enemy='b'
            kingr, kingc=self.wKingPos
        else:
            move_dir=1
            sr=1
            enemy='w'
            kingr, kingc = self.bKingPos

        # one&two squares moves
        if self.board[i +move_dir][j] == "--":
            if not pin or pin_dir==(move_dir,0):
                moves.append(Move((i, j), (i+move_dir, j), self.board))
                if i == sr and self.board[i+2*move_dir][j] == "--":
                    moves.append(Move((i, j), (i+2*move_dir, j), self.board))

        # capturing
        # left
        if j >= 1:
            if not pin or pin_dir == (move_dir, -1):
                if self.board[i+move_dir][j-1][0]==enemy:
                    moves.append(Move((i, j), (i+move_dir, j - 1), self.board))
                # enpass discover check
                if (i+move_dir, j - 1) == self.enpas_pos:
                    attP=blockP=False
                    if kingr==i:
                        if kingc<j:
                            inside=range(kingc+1, j-1)
                            outside=range(j+1,8)
                        else:
                            inside=range(kingc-1,j,-1)
                            outside=range(j-2,-1,-1)
                        for k in inside:
                            endpos=self.board[i][k]
                            if endpos!="--":
                                blockP=True
                        for k in outside:
                            endpos = self.board[i][k]
                            if endpos[0]==enemy and (endpos[1]=='r' or endpos[1]=='q'):
                                attP=True
                            elif endpos!="--":
                                blockP=True
                    if not attP or blockP:
                        moves.append(Move((i, j), (i+move_dir, j - 1), self.board, enpassant=True))
        #right
        if j <= 6:
            if not pin or pin_dir == (move_dir, 1):
                if self.board[i + move_dir][j+1][0] == enemy:
                    moves.append(Move((i, j), (i+move_dir, j + 1), self.board))
                #enpass discover check
                if (i+move_dir, j + 1) == self.enpas_pos:
                    attP = blockP = False
                    if kingr == i:
                        if kingc < j:
                            inside = range(kingc + 1, j)
                            outside = range(j + 2, 8)
                        else:
                            inside = range(kingc - 1, j+1, -1)
                            outside = range(j - 1, -1, -1)
                        for k in inside:
                            endpos = self.board[i][k]
                            if endpos != "--":
                                blockP = True
                        for k in outside:
                            endpos = self.board[i][k]
                            if endpos[0] == enemy and (endpos[1] == 'r' or endpos[1] == 'q'):
                                attP = True
                            elif endpos != "--":
                                blockP = True
                    if not attP or blockP:
                        moves.append(Move((i, j), (i+move_dir, j + 1), self.board, enpassant=True))