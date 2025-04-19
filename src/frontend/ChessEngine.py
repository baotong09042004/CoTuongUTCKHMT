# This class is responsible for storing all the information about the current state of a chess game.
# It will also be responsible for determining the valid moves at the current state and keep a move log.

class GameState():
    def __init__(self): 
        # bảng là một list 2 chiều 9x10 cho cờ tướng
        # thành phần thứ nhất đại diện cho màu của quân cờ, "b","r"
        # thành phân thứ hai đại diện cho loại quân cờ
        # "--" đại diện cho vị trí trống trên bàn cờ
        self.board = [
            ["b_rook", "b_horse", "b_elephant", "b_guard", "b_king", "b_guard", "b_elephant", "b_horse", "b_rook"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "b_cannon", "--", "--", "--", "--", "--", "b_cannon", "--"],
            ["b_pawn", "--", "b_pawn", "--", "b_pawn", "--", "b_pawn", "--", "b_pawn"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["r_pawn", "--", "r_pawn", "--", "r_pawn", "--", "r_pawn", "--", "r_pawn"],
            ["--", "r_cannon", "--", "--", "--", "--", "--", "r_cannon", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["r_rook", "r_horse", "r_elephant", "r_guard", "r_king", "r_guard", "r_elephant", "r_horse", "r_rook"]
        ]
        self.redToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.redToMove = not self.redToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    piece = self.board[r][c][2:]
                    self.getPieceMoves(r, c, moves)
        return moves

    def getPieceMoves(self, r, c, moves):
        piece = self.board[r][c][2:]
        if piece == "pawn":
            self.getPawnMoves(r, c, moves)
        elif piece == "rook":
            self.getRookMoves(r, c, moves)
        elif piece == "horse":
            self.getHorseMoves(r, c, moves)
        elif piece == "elephant":
            self.getElephantMoves(r, c, moves)
        elif piece == "guard":
            self.getGuardMoves(r, c, moves)
        elif piece == "king":
            self.getKingMoves(r, c, moves)
        elif piece == "cannon":
            self.getCannonMoves(r, c, moves)

    def getPawnMoves(self, r, c, moves):
        if self.redToMove:  # Quân tốt đỏ
            if r > 0 and self.board[r-1][c] == "--":  # Đi thẳng
                moves.append(Move((r, c), (r-1, c), self.board))
            if r <= 4:  # Đã qua sông
                if c > 0 and self.board[r][c-1][0] == 'b':  # Ăn quân đen bên trái
                    moves.append(Move((r, c), (r, c-1), self.board))
                if c < 8 and self.board[r][c+1][0] == 'b':  # Ăn quân đen bên phải
                    moves.append(Move((r, c), (r, c+1), self.board))
        else:  # Quân tốt đen
            if r < 9 and self.board[r+1][c] == "--":  # Đi thẳng
                moves.append(Move((r, c), (r+1, c), self.board))
            if r >= 5:  # Đã qua sông
                if c > 0 and self.board[r][c-1][0] == 'r':  # Ăn quân đỏ bên trái
                    moves.append(Move((r, c), (r, c-1), self.board))
                if c < 8 and self.board[r][c+1][0] == 'r':  # Ăn quân đỏ bên phải
                    moves.append(Move((r, c), (r, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
        enemyColor = "b" if self.redToMove else "r"
        for d in directions:
            for i in range(1, 10):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 10 and 0 <= endCol < 9:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getHorseMoves(self, r, c, moves):
        horseMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                     (1, -2), (1, 2), (2, -1), (2, 1)]
        enemyColor = "b" if self.redToMove else "r"
        for m in horseMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 10 and 0 <= endCol < 9:
                # Kiểm tra chướng ngại vật
                if m[0] == -2 or m[0] == 2:
                    if self.board[r + m[0]//2][c] == "--":
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--" or endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                else:
                    if self.board[r][c + m[1]//2] == "--":
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--" or endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))

    def getElephantMoves(self, r, c, moves):
        elephantMoves = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        enemyColor = "b" if self.redToMove else "r"
        for m in elephantMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 10 and 0 <= endCol < 9:
                # Kiểm tra chướng ngại vật
                if self.board[r + m[0]//2][c + m[1]//2] == "--":
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getGuardMoves(self, r, c, moves):
        guardMoves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemyColor = "b" if self.redToMove else "r"
        for m in guardMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 10 and 0 <= endCol < 9:
                # Kiểm tra phạm vi cung
                if (3 <= endRow <= 5) and (3 <= endCol <= 5):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        kingMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemyColor = "b" if self.redToMove else "r"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 10 and 0 <= endCol < 9:
                # Kiểm tra phạm vi cung
                if (3 <= endRow <= 5) and (3 <= endCol <= 5):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCannonMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemyColor = "b" if self.redToMove else "r"
        for d in directions:
            foundPiece = False
            for i in range(1, 10):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 10 and 0 <= endCol < 9:
                    endPiece = self.board[endRow][endCol]
                    if not foundPiece:
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        else:
                            foundPiece = True
                    else:
                        if endPiece != "--":
                            if endPiece[0] == enemyColor:
                                moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                else:
                    break

class Move():
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]