# src/frontend/AIEngine.py
import random
import ChessChineseEngine

# Giá trị cơ bản của các quân cờ
PIECE_SCORES = {
    "king": 10000,
    "guard": 200,
    "elephant": 200,
    "rook": 900,
    "horse": 400,
    "cannon": 450,
    "pawn": 100
}

# Bảng giá trị vị trí cho các quân cờ
KING_SCORES = [
    [0, 0, 0, 15, 20, 15, 0, 0, 0],
    [0, 0, 0, 10, 10, 10, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 10, 10, 10, 0, 0, 0],
    [0, 0, 0, 15, 20, 15, 0, 0, 0]
]

ROOK_SCORES = [
    [150, 160, 150, 160, 150, 160, 150, 160, 150],
    [160, 170, 160, 160, 150, 160, 160, 170, 160],
    [170, 180, 170, 170, 160, 170, 170, 180, 170],
    [170, 190, 200, 220, 240, 220, 200, 190, 170],
    [180, 220, 210, 240, 250, 240, 210, 220, 180],
    [180, 220, 210, 240, 250, 240, 210, 220, 180],
    [180, 220, 210, 240, 250, 240, 210, 220, 180],
    [170, 190, 200, 220, 240, 220, 200, 190, 170],
    [170, 180, 170, 190, 250, 190, 170, 180, 170],
    [160, 170, 160, 150, 150, 150, 160, 170, 160]
]

GUARD_SCORES = [
    [0, 0, 0, 30, 0, 30, 0, 0, 0],
    [0, 0, 0, 0, 22, 0, 0, 0, 0],
    [0, 0, 0, 30, 0, 30, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 30, 0, 30, 0, 0, 0],
    [0, 0, 0, 0, 22, 0, 0, 0, 0],
    [0, 0, 0, 30, 0, 30, 0, 0, 0]
]

ELEPHANT_SCORES = [
    [0, 0, 30, 0, 0, 0, 30, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [20, 0, 0, 0, 35, 0, 0, 0, 20],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 25, 0, 0, 0, 25, 0, 0],
    [0, 0, 25, 0, 0, 0, 25, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [20, 0, 0, 0, 35, 0, 0, 0, 20],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 30, 0, 0, 0, 30, 0, 0]
]

HORSE_SCORES = [
    [60, 70, 75, 70, 60, 70, 75, 70, 60],
    [70, 75, 75, 70, 50, 70, 75, 75, 70],
    [80, 80, 90, 90, 80, 90, 90, 80, 80],
    [80, 90, 100, 100, 90, 100, 100, 90, 80],
    [90, 100, 100, 110, 100, 110, 100, 100, 90],
    [90, 110, 110, 120, 100, 120, 110, 110, 90],
    [90, 100, 120, 130, 110, 130, 120, 100, 90],
    [90, 100, 120, 125, 120, 125, 120, 100, 90],
    [80, 110, 125, 90, 70, 90, 125, 110, 80],
    [70, 80, 90, 80, 70, 80, 90, 80, 70]
]

CANNON_SCORES = [
    [80, 90, 80, 70, 60, 70, 80, 90, 80],
    [80, 90, 80, 70, 65, 70, 80, 90, 80],
    [90, 100, 80, 80, 70, 80, 80, 100, 90],
    [90, 100, 90, 90, 110, 90, 90, 100, 90],
    [90, 100, 90, 110, 130, 110, 90, 100, 90],
    [90, 110, 90, 110, 130, 110, 90, 110, 90],
    [90, 110, 90, 110, 130, 110, 90, 110, 90],
    [100, 120, 90, 80, 80, 80, 90, 120, 100],
    [110, 125, 100, 70, 60, 70, 100, 125, 110],
    [125, 130, 100, 70, 60, 70, 100, 130, 125]
]

PAWN_SCORES = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [10, 0, 10, 0, 15, 0, 10, 0, 10],
    [10, 0, 15, 0, 15, 0, 15, 0, 10],
    [15, 20, 20, 20, 20, 20, 20, 20, 15],
    [20, 25, 25, 30, 30, 30, 25, 25, 20],
    [25, 30, 30, 40, 40, 40, 30, 30, 25],
    [25, 30, 40, 50, 60, 50, 40, 30, 25],
    [10, 10, 10, 20, 25, 20, 10, 10, 10]
]

CHECKMATE = 1000
STALEMATE = 0

nextMove = None


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None

    depth = 3 if len(validMoves) < 30 else 2
    orderedMoves = moveOrdering(gs, validMoves)
    findMoveNegaMaxAlphaBeta(gs, orderedMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.redToMove else -1, depth)
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, maxDepth):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    orderedMoves = moveOrdering(gs, validMoves)

    for move in orderedMoves:
        gs.makeMove(move)
        score = -findMoveNegaMaxAlphaBeta(
            gs, gs.getValidMoves(), depth - 1, -beta, -alpha, -turnMultiplier, maxDepth)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            if depth == maxDepth:
                nextMove = move

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        return -CHECKMATE if gs.redToMove else CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(10):
        for col in range(9):
            piece = gs.board[row][col]
            if piece != "--":
                piece_type = piece[2:]
                base_score = PIECE_SCORES.get(piece_type, 0)
                position_score = getPositionScore(piece, row, col)
                if piece.startswith('r_'):
                    score += base_score + position_score
                else:
                    score -= base_score + position_score
    return score


def getPositionScore(piece, row, col):
    piece_type = piece[2:]
    is_red = piece.startswith('r_')
    if is_red:
        row = 9 - row

    if piece_type == 'king':
        return KING_SCORES[row][col]
    elif piece_type == 'guard':
        return GUARD_SCORES[row][col]
    elif piece_type == 'elephant':
        return ELEPHANT_SCORES[row][col]
    elif piece_type == 'rook':
        return ROOK_SCORES[row][col]
    elif piece_type == 'horse':
        return HORSE_SCORES[row][col]
    elif piece_type == 'cannon':
        return CANNON_SCORES[row][col]
    elif piece_type == 'pawn':
        return PAWN_SCORES[row][col]
    return 0


def moveOrdering(gs, validMoves):
    moveScores = []
    for move in validMoves:
        moveScore = 0
        if move.pieceCaptured != "--":
            moveScore += PIECE_SCORES.get(move.pieceCaptured[2:], 0)
        if is_move_safe(gs, move):
            moveScore += 50
        moveScores.append((moveScore, move))
    moveScores.sort(key=lambda x: x[0], reverse=True)
    return [move for _, move in moveScores]


def is_move_safe(gs, move):
    gs.makeMove(move)
    opponent_moves = gs.getValidMoves()
    is_safe = True
    for opp_move in opponent_moves:
        if opp_move.endRow == move.endRow and opp_move.endCol == move.endCol:
            is_safe = False
            break
    gs.undoMove()
    return is_safe
