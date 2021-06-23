import numpy as np
from AI_States import AI_states
import random

state_to_score_hasmap = {}
value_piece = {
    "q": 900, "b": 330, "n": 320, "r": 500, "p": 100, "k": 0
}

# positional scoring the pieces
pos_wking_mid = np.array([
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]])
pos_wking_fin = np.array([
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]])
pos_wknight = np.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 11, 15, 15, 11, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -34, -30, -30, -30, -34, -50]])
pos_wrook = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]])
pos_wbishop = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]])
pos_wqueen = np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]])
pos_wpawn = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 34, 34, 20, 10, 10],
    [5, 5, 10, 27, 27, 10, 5, 5],
    [0, 0, 0, 23, 23, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -23, -23, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]])

pos_bking_mid = np.array([[20, 30, 10, 0, 0, 10, 30, 20],
                          [20, 20, 0, 0, 0, 0, 20, 20],
                          [-10, -20, -20, -20, -20, -20, -20, -10],
                          [-20, -30, -30, -40, -40, -30, -30, -20],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30],
                          [-30, -40, -40, -50, -50, -40, -40, -30]])
pos_bking_fin = np.array([[-50, -30, -30, -30, -30, -30, -30, -50],
                          [-30, -30, 0, 0, 0, 0, -30, -30],
                          [-30, -10, 20, 30, 30, 20, -10, -30],
                          [-30, -10, 30, 40, 40, 30, -10, -30],
                          [-30, -10, 30, 40, 40, 30, -10, -30],
                          [-30, -10, 20, 30, 30, 20, -10, -30],
                          [-30, -20, -10, 0, 0, -10, -20, -30],
                          [-50, -40, -30, -20, -20, -30, -40, -50]])
pos_bknight = np.array([[-50, -34, -30, -30, -30, -34, -40, -50],
                        [-40, -20, 0, 5, 5, 0, -20, -40],
                        [-30, 5, 11, 15, 15, 11, 5, -30],
                        [-30, 0, 15, 20, 20, 15, 0, -30],
                        [-30, 5, 15, 20, 20, 15, 5, -30],
                        [-30, 0, 10, 15, 15, 10, 0, -30],
                        [-40, -20, 0, 0, 0, 0, -20, -40],
                        [-50, -40, -30, -30, -30, -30, -40, -50]])
pos_brook = np.array([[0, 0, 0, 5, 5, 0, 0, 0, ],
                      [-5, 0, 0, 0, 0, 0, 0, -5, ],
                      [-5, 0, 0, 0, 0, 0, 0, -5, ],
                      [-5, 0, 0, 0, 0, 0, 0, -5, ],
                      [-5, 0, 0, 0, 0, 0, 0, -5, ],
                      [-5, 0, 0, 0, 0, 0, 0, -5, ],
                      [5, 10, 10, 10, 10, 10, 10, 5, ],
                      [0, 0, 0, 0, 0, 0, 0, 0, ]])
pos_bbishop = np.array([[-20, -10, -10, -10, -10, -10, -10, -20],
                        [-10, 5, 0, 0, 0, 0, 5, -10],
                        [-10, 10, 10, 10, 10, 10, 10, -10],
                        [-10, 0, 10, 10, 10, 10, 0, -10],
                        [-10, 5, 5, 10, 10, 5, 5, -10],
                        [-10, 0, 5, 10, 10, 5, 0, -10],
                        [-10, 0, 0, 0, 0, 0, 0, -10],
                        [-20, -10, -10, -10, -10, -10, -10, -20]])
pos_bqueen = np.array([[-20, -10, -10, -5, -5, -10, -10, -20],
                       [-10, 0, 5, 0, 0, 0, 0, -10],
                       [-10, 5, 5, 5, 5, 5, 0, -10],
                       [0, 0, 5, 5, 5, 5, 0, -5],
                       [-5, 0, 5, 5, 5, 5, 0, -5],
                       [-10, 0, 5, 5, 5, 5, 0, -10],
                       [-10, 0, 0, 0, 0, 0, 0, -10],
                       [-20, -10, -10, -5, -5, -10, -10, -20]])
pos_bpawn = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                      [5, 10, 10, -23, -23, 10, 10, 5],
                      [5, -5, -10, 0, 0, -10, -5, 5],
                      [0, 0, 0, 23, 23, 0, 0, 0],
                      [5, 5, 10, 27, 27, 10, 5, 5],
                      [10, 10, 20, 34, 34, 20, 10, 10],
                      [50, 50, 50, 50, 50, 50, 50, 50],
                      [0, 0, 0, 0, 0, 0, 0, 0]])

pos_scores = {"wn": pos_wknight, "wb": pos_wbishop, "wr": pos_wrook, "wp": pos_wpawn, "wq": pos_wqueen,
              "wk": pos_wking_mid,
              "bn": pos_bknight, "bb": pos_bbishop, "br": pos_brook, "bp": pos_bpawn, "bq": pos_bqueen,
              "bk": pos_bking_mid}

checkmate = 99999999
stalemate = 0

f = open("config.txt", "r")
f.readline()
f.readline()
DEPTH=int(f.readline())

def findRand(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def greedy(current, valid_moves):
    if current.turn_white:
        turn = 1
    else:
        turn = -1

    op_minmax_score = checkmate
    best_playermove = None
    for player_move in valid_moves:
        current.make_move(player_move)
        op_moves = current.get_valid_moves()
        if current.staleMate:
            op_maxscore = stalemate
        elif current.checkMate:
            op_maxscore = -checkmate
        else:
            op_maxscore = -checkmate
            for op_move in op_moves:
                current.make_move(op_move)
                current.get_valid_moves()
                if current.checkMate:
                    score = checkmate
                elif current.staleMate:
                    score = stalemate
                else:
                    score = -turn * heuristic(current.board)
                if score > op_maxscore:
                    op_maxscore = score
                current.undo_move()
        if op_maxscore < op_minmax_score:
            op_minmax_score = op_maxscore
            best_playermove = player_move
        current.undo_move()
    return best_playermove

def minimax(current, valid_moves, depth, white_turn):
    global next_move, eval_pos
    eval_pos += 1
    if depth == 0:
        return heuristic(current)

    if white_turn:
        score_max = -checkmate
        for move in valid_moves:
            current.make_move(move)
            next_moves = current.get_valid_moves()
            score = minimax(current, next_moves, depth - 1, False)
            if score > score_max:
                score_max = score
                if depth == DEPTH:
                    next_move = move
            current.undo_move()

        return score_max

    else:
        score_min = checkmate
        for move in valid_moves:
            current.make_move(move)
            next_moves = current.get_valid_moves()
            score = minimax(current, next_moves, depth - 1, True)
            if score < score_min:
                score_min = score
                if depth == DEPTH:
                    next_move = move
            current.undo_move()
        return score_min

def negamax_abprun(current, valid_moves, depth, alpha, beta, white_turn):
    global next_move, eval_pos

    eval_pos += 1
    if depth == 0:
        return white_turn * heuristic(current)

    #taking the already computed value from the transpostion table, if available
    # curr_hash = hash(current) * white_turn
    # if curr_hash in state_to_score_hasmap:
    #     temp_score = state_to_score_hasmap[curr_hash].score
    #     next_move=state_to_score_hasmap[curr_hash].next_move
    #     #print(temp_score)
    #     #print(next_move)
    #     return temp_score

    score_max = - checkmate
    for move in valid_moves:
        current.make_move(move)
        next_moves = current.get_valid_moves()
        score = -negamax_abprun(current, next_moves, depth - 1, -beta, -alpha, -white_turn)
        if score > score_max:
            score_max = score
            if depth == DEPTH:
                next_move = move
        current.undo_move()
        if score_max > alpha:
            alpha = score_max
        if alpha >= beta:
            break

    #populating the transposition table
    # if next_move:
    #     curr_hash = hash(current) * white_turn
    #     if curr_hash not in state_to_score_hasmap:
    #         current_ai_state = AI_states(current, white_turn,score_max,next_move)
    #         state_to_score_hasmap[curr_hash] = current_ai_state

    return score_max

def heuristic(current):
    # pawn chains
    if current.checkMate:
        if current.turn_white:
            return -checkmate
        else:
            return checkmate
    elif current.staleMate:
        return stalemate

    score = 0
    for row in range(len(current.board)):
        for col in range(len(current.board[row])):
            sq = current.board[row][col]
            if sq != "--":
                # score positionally
                if sq[1]!="k":
                    pos_score = pos_scores[sq][row][col]
                    if sq[0] == 'w':
                        score = score + value_piece[sq[1]] + pos_score
                    elif sq[0] == 'b':
                        score = score - value_piece[sq[1]] - pos_score
                else:
                    if len(current.moveLog)<80:
                        if sq[0] == 'w':
                            score = score + pos_wking_mid[row][col]
                        elif sq[0] == 'b':
                            score = score - pos_bking_mid[row][col]
                    else:
                        if sq[0] == 'w':
                            score = score + pos_wking_fin[row][col]
                        elif sq[0] == 'b':
                            score = score - pos_bking_fin[row][col]

    #print(score)
    return score

# initial call
def ai(current, valid_moves):
    global next_move, eval_pos
    eval_pos = 0
    next_move = None
    if current.turn_white:
        initial_call = 1
    else:
        initial_call = -1

    negamax_abprun(current, valid_moves, DEPTH, -checkmate, checkmate, initial_call)
    #minimax(current, valid_moves, DEPTH, initial_call)
    print(eval_pos)
    return next_move