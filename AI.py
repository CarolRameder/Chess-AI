import random

value_piece = {
    "q": 9, "b": 3, "n": 3, "r": 5, "p": 1,"k": 0
}
checkmate = 1000
stalemate = 0
DEPTH=3

def findRand(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def heuristic(current):
    if current.checkMate:
        if current.turn_white:
            return -checkmate
        else:
            return checkmate
    elif current.staleMate:
        return stalemate
    score = 0
    for row in current.board:
        for sq in row:
            if sq[0] == 'w':
                score += value_piece[sq[1]]
            elif sq[0] == 'b':
                score -= value_piece[sq[1]]
    return score

def greedy(current, valid_moves):
    if current.turn_white:
        turn = 1
    else:
        turn = -1

    op_minmax_score=checkmate
    best_playermove=None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        current.make_move(player_move)
        op_moves=current.get_valid_moves()
        if current.staleMate:
            op_maxscore=stalemate
        elif current.checkMate:
            op_maxscore=-checkmate
        else:
            op_maxscore=-checkmate
            for op_move in op_moves:
                current.make_move(op_move)
                current.get_valid_moves()
                if current.checkMate:
                    score=checkmate
                elif current.staleMate:
                    score=stalemate
                else:
                    score=-turn*heuristic(current.board)
                if score> op_maxscore:
                    op_maxscore=score
                current.undo_move()
        if op_maxscore < op_minmax_score:
            op_minmax_score=op_maxscore
            best_playermove=player_move
        current.undo_move()
    return best_playermove

#initial call
def ai(current, valid_moves):
    global next_move, eval_pos
    eval_pos=0
    next_move=None
    #minmax(current, valid_moves, DEPTH, current.turn_white)
    if current.turn_white:
        initial_call=1
    else:
        initial_call = -1
    negamax_abprun(current, valid_moves, DEPTH, -checkmate, checkmate, initial_call)
    # print(eval_pos)

    return next_move

def minmax(current, valid_moves, depth, white_turn):
    global next_move, eval_pos
    eval_pos+=1
    if depth==0:
        return heuristic(current)

    if white_turn:
        score_max=-checkmate
        for move in valid_moves:
            current.make_move(move)
            next_moves=current.get_valid_moves()
            score=minmax(current,next_moves,depth-1,False)
            if score>score_max:
                score_max=score
                if depth==DEPTH:
                    next_move=move
            current.undo_move()

        return score_max

    else:
        score_min=checkmate
        for move in valid_moves:
            current.make_move(move)
            next_moves=current.get_valid_moves()
            score=minmax(current,next_moves,depth-1,True)
            if score < score_min:
                score_min=score
                if depth==DEPTH:
                    next_move=move
            current.undo_move()
        return score_min

def negamax_abprun(current, valid_moves, depth, alpha, beta, white_turn):
    global next_move, eval_pos
    eval_pos+=1
    if depth==0:
        return white_turn*heuristic(current)

    #move order ??
    score_max= - checkmate
    for move in valid_moves:
        current.make_move(move)
        next_moves=current.get_valid_moves()
        score=-negamax_abprun(current, next_moves, depth-1, -beta, -alpha, -white_turn)
        if score>score_max:
            score_max=score
            if depth==DEPTH:
                next_move=move
        current.undo_move()
        if score_max>alpha:
            alpha=score_max
        if alpha>= beta:
            break

    return score_max