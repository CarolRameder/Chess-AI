import random

value_piece = {
    "q": 9, "b": 3, "n": 3, "r": 5, "p": 1,"k": 0
}

#positional scoring the pieces
#too biased
pos_knight=[
    [1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,1],
    [1,2,3,3,3,3,2,1],
    [1,2,3,4,4,3,2,1],
    [1,2,3,4,4,3,2,1],
    [1,2,3,3,3,3,2,1],
    [1,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1]]
pos_rook=[
    [4,3,4,4,4,4,3,4],
    [4,4,4,4,4,4,4,4],
    [1,1,2,3,3,2,1,1],
    [1,2,3,4,4,3,2,1],
    [1,2,3,4,4,3,2,1],
    [1,1,2,2,2,2,1,1],
    [4,4,4,4,4,4,4,4],
    [4,3,4,4,4,4,3,4]]
pos_bishop=[
    [4,3,2,1,1,2,3,4],
    [3,4,3,2,2,3,4,3],
    [2,3,4,3,3,4,3,2],
    [1,2,3,4,4,3,2,1],
    [1,2,3,4,4,3,2,1],
    [2,3,4,3,3,4,3,2],
    [3,4,3,2,2,3,4,3],
    [4,3,2,1,1,2,3,4]]
pos_queen=[
    [1,1,1,3,1,1,1,1],
    [1,2,3,3,3,1,1,1],
    [1,4,3,3,3,4,2,1],
    [1,2,3,3,3,2,2,1],
    [1,2,3,3,3,2,2,1],
    [1,4,3,3,3,4,2,1],
    [1,1,2,3,3,1,1,1],
    [1,1,1,3,1,1,1,1]]
pos_wpawn=[
    [8,8,8,8,8,8,8,8],
    [8,8,8,8,8,8,8,8],
    [5,6,6,7,7,6,6,5],
    [2,3,3,5,5,3,3,2],
    [1,2,3,4,4,3,2,1],
    [1,1,2,3,3,2,1,1],
    [1,1,1,0,0,1,1,1],
    [0,0,0,0,0,0,0,0]]
pos_bpawn=[
    [0,0,0,0,0,0,0,0],
    [1,1,1,0,0,1,1,1],
    [1,1,2,3,3,2,1,1],
    [1,2,3,4,4,3,2,1],
    [2,3,3,5,5,3,3,2],
    [5,6,6,7,7,6,6,5],
    [8,8,8,8,8,8,8,8],
    [8,8,8,8,8,8,8,8]]

pos_scores={"n":pos_knight, "b":pos_bishop, "r":pos_rook, "wp":pos_wpawn, "bp":pos_bpawn, "q":pos_queen}

checkmate = 1000
stalemate = 0
DEPTH=4

#initial call
def ai(current, valid_moves):
    global next_move, eval_pos
    eval_pos=0
    next_move=None
    random.shuffle(valid_moves)
    #minmax(current, valid_moves, DEPTH, current.turn_white)
    if current.turn_white:
        initial_call=1
    else:
        initial_call = -1
    negamax_abprun(current, valid_moves, DEPTH, -checkmate, checkmate, initial_call)
    # print(eval_pos)

    return next_move

def findRand(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

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

def heuristic(current):
#castle bonus / king
#pawn chains
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
            sq=current.board[row][col]
            if sq != "--":
                #score positionally
                pos_score=0
                if sq[1]!='k':
                    if sq[1]=="p":
                        pos_score=pos_scores[sq][row][col]
                    else:
                        pos_score = pos_scores[sq[1]][row][col]
                if sq[0] == 'w':
                    score += value_piece[sq[1]] + pos_score*.2
                elif sq[0] == 'b':
                    score -= value_piece[sq[1]] + pos_score*.2

    return score