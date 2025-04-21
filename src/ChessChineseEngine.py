
class GameState:
    def __init__(self):
        """
        Khởi tạo trạng thái ban đầu của bàn cờ.
        
        Quy ước:
        - Màu quân: 'r' (đỏ), 'b' (đen)
        - Tên quân: king (tướng), guard (sĩ), elephant (tượng), 
                   rook (xe), cannon (pháo), horse (mã), pawn (tốt)
        - "--" đại diện cho ô trống
        """
        # Khởi tạo bàn cờ 9x10
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
        
        # Ánh xạ tên quân cờ tới hàm di chuyển tương ứng
        self.moveFunctions = {
            'pawn': self.getPawnMoves,      # Tốt
            'rook': self.getRookMoves,      # Xe
            'horse': self.getHorseMoves,    # Mã
            'elephant': self.getElephantMoves,  # Tượng
            'guard': self.getGuardMoves,    # Sĩ
            'king': self.getKingMoves,      # Tướng
            'cannon': self.getCannonMoves   # Pháo
        }

        # Trạng thái game
        self.redToMove = True              # Đỏ đi trước
        self.moveLog = []                  # Lịch sử nước đi
        self.redKingLocation = (9, 4)      # Vị trí tướng đỏ
        self.blackKingLocation = (0, 4)    # Vị trí tướng đen
        self.checkMate = False             # Chiếu hết
        self.staleMate = False             # Hòa cờ

    def makeMove(self, move):
        """
        Thực hiện một nước đi và cập nhật trạng thái bàn cờ.
        
        Args:
            move: Đối tượng Move chứa thông tin về nước đi
        """
        # Di chuyển quân cờ
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        
        # Lưu nước đi vào lịch sử
        self.moveLog.append(move)
        
        # Cập nhật vị trí tướng nếu tướng di chuyển
        if move.pieceMoved == 'r_king':
            self.redKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'b_king':
            self.blackKingLocation = (move.endRow, move.endCol)
            
        # Kiểm tra nếu tướng bị ăn
        if move.pieceCaptured == 'b_king':
            print("Đỏ thắng bằng cách ăn tướng!")
        elif move.pieceCaptured == 'r_king':
            print("Đen thắng bằng cách ăn tướng!")
        
        # Đổi lượt đi
        self.redToMove = not self.redToMove

    def undoMove(self):
        """Hoàn tác nước đi gần nhất."""
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove
            
            # Cập nhật lại vị trí tướng
            if move.pieceMoved == 'r_king':
                self.redKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'b_king':
                self.blackKingLocation = (move.startRow, move.startCol)
            
            # Reset trạng thái kết thúc game
            self.checkMate = False
            self.staleMate = False

    def getValidMoves(self):
        """
        Lấy tất cả các nước đi hợp lệ cho người chơi hiện tại.
        Một nước đi hợp lệ là nước đi không để tướng bị chiếu và không để hai tướng đối mặt.
        
        Returns:
            list: Danh sách các nước đi hợp lệ
        """
        # 1. Lấy tất cả nước đi có thể
        moves = self.getAllPossibleMoves()
        
        # 2. Kiểm tra từng nước đi
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            
            # Kiểm tra hai tướng có đối mặt không
            if self._kingsAreFacing():
                moves.remove(moves[i])
            else:
                # Kiểm tra nước đi có gây chiếu tướng không
                self.redToMove = not self.redToMove
                if self.inCheck():
                    moves.remove(moves[i])
                self.redToMove = not self.redToMove
            
            self.undoMove()

        # 3. Kiểm tra kết thúc game
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
                print(f"{'Đỏ' if self.redToMove else 'Đen'} bị chiếu hết!")
            else:
                self.staleMate = True
                print("Hòa do hết nước đi!")

        return moves

    def _kingsAreFacing(self):
        """
        Kiểm tra xem hai tướng có đối mặt nhau không.
        
        Returns:
            bool: True nếu hai tướng đối mặt, False nếu không
        """
        # Nếu hai tướng không cùng cột thì không đối mặt
        if self.redKingLocation[1] != self.blackKingLocation[1]:
            return False
            
        col = self.redKingLocation[1]
        startRow = min(self.redKingLocation[0], self.blackKingLocation[0])
        endRow = max(self.redKingLocation[0], self.blackKingLocation[0])
        
        # Kiểm tra có quân nào ở giữa hai tướng không
        for row in range(startRow + 1, endRow):
            if self.board[row][col] != "--":
                return False
        return True
            
    def inCheck(self):
        """
        Kiểm tra xem người chơi hiện tại có đang bị chiếu không.
        
        Returns:
            bool: True nếu đang bị chiếu, False nếu không
        """
        if self.redToMove:
            return self._isSquareUnderAttack(*self.redKingLocation)
        else:
            return self._isSquareUnderAttack(*self.blackKingLocation)

    def _isSquareUnderAttack(self, r, c):
        """
        Kiểm tra xem một ô có thể bị tấn công bởi quân đối phương không.
        
        Args:
            r (int): Hàng của ô cần kiểm tra
            c (int): Cột của ô cần kiểm tra
            
        Returns:
            bool: True nếu ô có thể bị tấn công, False nếu không
        """
        self.redToMove = not self.redToMove
        oppMoves = self.getAllPossibleMoves()
        self.redToMove = not self.redToMove
        
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        """
        Lấy tất cả các nước đi có thể cho người chơi hiện tại,
        không tính đến việc tướng có bị chiếu hay không.
        
        Returns:
            list: Danh sách các nước đi có thể
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    piece = self.board[r][c][2:]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def _isValidSquare(self, r, c):
        """Kiểm tra xem tọa độ (r,c) có nằm trong bàn cờ không."""
        return 0 <= r < 10 and 0 <= c < 9

    def _isInPalace(self, r, c, isRed):
        """Kiểm tra xem tọa độ (r,c) có nằm trong cung không."""
        if isRed:
            return 7 <= r <= 9 and 3 <= c <= 5
        else:
            return 0 <= r <= 2 and 3 <= c <= 5

    def getPawnMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân tốt.
        
        Luật di chuyển:
        1. Tốt đỏ đi lên, tốt đen đi xuống
        2. Khi chưa qua sông, tốt chỉ đi thẳng 1 ô
        3. Khi đã qua sông, tốt có thể đi thẳng hoặc ngang 1 ô
        """
        directions = []
        if self.redToMove:  # Tốt đỏ
            directions.append((-1, 0))  # Đi lên
            if r <= 4:  # Đã qua sông
                directions.extend([(0, -1), (0, 1)])  # Thêm đi ngang
        else:  # Tốt đen
            directions.append((1, 0))  # Đi xuống
            if r >= 5:  # Đã qua sông
                directions.extend([(0, -1), (0, 1)])  # Thêm đi ngang

        enemyColor = 'b' if self.redToMove else 'r'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if self._isValidSquare(endRow, endCol):
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getRookMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân xe.
        Xe đi thẳng theo các hướng dọc ngang không giới hạn số ô.
        """
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Lên, trái, xuống, phải
        enemyColor = 'b' if self.redToMove else 'r'
        
        for d in directions:
            for i in range(1, 10):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if not self._isValidSquare(endRow, endCol):
                    break
                
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    break
                else:
                    break

    def getHorseMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân mã.
        Mã di chuyển theo hình chữ L và có thể bị cản.
        """
        directions = [(-2, -1), (-2, 1), (-1, 2), (1, 2),
                     (2, -1), (2, 1), (-1, -2), (1, -2)]
        allyColor = 'r' if self.redToMove else 'b'
        
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if not self._isValidSquare(endRow, endCol):
                continue
                
            # Kiểm tra chân ngựa
            if abs(d[0]) == 2:  # Đi ngang 2
                if self.board[r + d[0]//2][c] != "--":
                    continue
            else:  # Đi dọc 2
                if self.board[r][c + d[1]//2] != "--":
                    continue
                    
            endPiece = self.board[endRow][endCol]
            if endPiece == "--" or endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))

    def getElephantMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân tượng.
        Tượng đi chéo 2 ô và không được qua sông.
        """
        directions = [(-2, -2), (-2, 2), (2, 2), (2, -2)]
        allyColor = 'r' if self.redToMove else 'b'
        
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if not self._isValidSquare(endRow, endCol):
                continue
                
            # Kiểm tra mắt tượng
            midRow = r + d[0]//2
            midCol = c + d[1]//2
            if self.board[midRow][midCol] != "--":
                continue
                
            # Kiểm tra qua sông
            if self.redToMove and endRow < 5:
                continue
            if not self.redToMove and endRow > 4:
                continue
                
            endPiece = self.board[endRow][endCol]
            if endPiece == "--" or endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))

    def getGuardMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân sĩ.
        Sĩ đi chéo 1 ô và chỉ được đi trong cung.
        """
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        allyColor = 'r' if self.redToMove else 'b'
        
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if not self._isValidSquare(endRow, endCol):
                continue
                
            # Kiểm tra trong cung
            if not self._isInPalace(endRow, endCol, self.redToMove):
                continue
                
            endPiece = self.board[endRow][endCol]
            if endPiece == "--" or endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))

    def getKingMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân tướng.
        Tướng đi thẳng 1 ô và chỉ được đi trong cung.
        Đặc biệt xử lý trường hợp hai tướng đối diện.
        """
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        allyColor = 'r' if self.redToMove else 'b'
        
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if not self._isValidSquare(endRow, endCol):
                continue
                
            # Kiểm tra trong cung
            if not self._isInPalace(endRow, endCol, self.redToMove):
                continue
                
            # Kiểm tra tướng đối diện
            if endCol == c:  # Cùng cột
                enemyKingRow = self.blackKingLocation[0] if self.redToMove else self.redKingLocation[0]
                enemyKingCol = self.blackKingLocation[1] if self.redToMove else self.redKingLocation[1]
                
                if c == enemyKingCol:  # Cùng cột với tướng đối phương
                    hasPieceBetween = False
                    startRow = min(endRow, enemyKingRow)
                    endRowCheck = max(endRow, enemyKingRow)
                    
                    for rowCheck in range(startRow + 1, endRowCheck):
                        if self.board[rowCheck][c] != "--":
                            hasPieceBetween = True
                            break
                            
                    if not hasPieceBetween:
                        continue
            
            endPiece = self.board[endRow][endCol]
            if endPiece == "--" or endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCannonMoves(self, r, c, moves):
        """
        Tạo tất cả nước đi có thể cho quân pháo.
        Pháo đi như xe khi không ăn quân, và cần 1 quân làm giá để ăn quân.
        """
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Lên, trái, xuống, phải
        enemyColor = 'b' if self.redToMove else 'r'
        
        for d in directions:
            hasScreen = False  # Đã gặp quân làm giá chưa
            for i in range(1, 10):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if not self._isValidSquare(endRow, endCol):
                    break
                    
                endPiece = self.board[endRow][endCol]
                if not hasScreen:
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        hasScreen = True
                else:
                    if endPiece != "--":
                        if endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            # Debug log cho việc chiếu tướng
                            if endPiece == f"{enemyColor}_king":
                                print(f"DEBUG: Pháo tại ({r},{c}) có thể chiếu tướng tại ({endRow},{endCol}) qua quân giá!")
                        break

class Move:
    def __init__(self, startSq, endSq, board):
        """
        Khởi tạo một nước đi.
        
        Args:
            startSq (tuple): Tọa độ ô bắt đầu (row, col)
            endSq (tuple): Tọa độ ô kết thúc (row, col)
            board (list): Trạng thái bàn cờ hiện tại
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """So sánh hai nước đi."""
        if isinstance(other, Move):
            return (self.startRow == other.startRow and 
                    self.startCol == other.startCol and 
                    self.endRow == other.endRow and 
                    self.endCol == other.endCol)
        return False

    def getChessNotation(self):
        """Chuyển đổi nước đi sang ký hiệu cờ tướng."""
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """Chuyển đổi tọa độ thành ký hiệu cờ tướng."""
        return str(c) + str(9-r)
