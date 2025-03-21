"""
国际象棋人机对战程序（内置AI引擎）
需要提前准备：
1. 安装依赖：pip install pygame python-chess
2. 创建img目录并放置棋子PNG素材（文件名格式：wP.png, bK.png等）
"""

import pygame
import chess
import os
import math

# 棋盘参数
SQUARE_SIZE = 68
BOARD_SIZE = SQUARE_SIZE * 8

class ChessAIEngine:
    def __init__(self, depth=3):
        self.depth = depth  # 搜索深度
        
    def get_best_move(self, board):
        """获取最佳走棋"""
        best_move = None
        best_value = -math.inf
        
        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(board, self.depth-1, -math.inf, math.inf, False)
            board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
                
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing):
        """Minimax算法配合Alpha-Beta剪枝"""
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)
            
        if maximizing:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval







    def evaluate(self, board):
        # 棋子基础价值
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        # 位置价值表（示例：兵的中间位置加分）
        pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        score = 0
        
        # 棋子价值和位置评估
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # 基础价值
                value = piece_values[piece.piece_type]
                
                # 位置调整（根据不同棋子类型选择不同位置表）
                if piece.piece_type == chess.PAWN:
                    adjusted_value = pawn_table[square] if piece.color == chess.WHITE else pawn_table[63 - square]
                    value += adjusted_value
                
                # 颜色修正
                score += value if piece.color == chess.WHITE else -value
        
        # 局面特征评估（示例：）
        # 1. 中心控制（d4/d5/e4/e5格子是否有棋子）
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        for sq in center_squares:
            if board.piece_at(sq):
                score += 50 if board.color_at(sq) == chess.WHITE else -50
        
        # 2. 王的安全（根据王前兵是否完整）
        if board.has_kingside_castling_rights(chess.WHITE):
            score += 30
        if board.has_queenside_castling_rights(chess.WHITE):
            score += 30
        # 黑方同理...
        
        return score


class ChessGame:
    def __init__(self, ai_color=chess.BLACK):
        # 初始化棋盘
        self.board = chess.Board()
        self.ai_color = ai_color
        self.selected_square = None
        self.human_color = not ai_color
        self.game_over = False
        self.ai_engine = ChessAIEngine(depth=3)  # 使用内置AI引擎
        
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption("Chess AI")
        self.load_images()
        
        # 自动开始游戏
        if self.human_color != chess.WHITE:
            self.make_ai_move()

    def load_images(self):
        """加载棋子图片"""
        self.pieces = {}
        pieces = ["pawn", "night", "bishop", "rook", "queen", "king"]
        colors = ["w", "b"]
        
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece[0].upper()}"
                try:
                    img = pygame.image.load(f"img/{color}{piece[0].upper()}.png")
                except:
                    img = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    img.fill((255, 0, 255))  # 错误时显示粉色方块
                self.pieces[key] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

    def draw_board(self):
        """绘制棋盘和棋子"""
        # 绘制棋盘背景
        colors = [(238, 238, 210), (118, 150, 86)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

        # 绘制棋子
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)
                color = "w" if piece.color else "b"
                piece_type = piece.symbol().upper()
                self.screen.blit(self.pieces[f"{color}{piece_type}"],
                               (col * SQUARE_SIZE, row * SQUARE_SIZE))

        # 绘制选中高亮
        if self.selected_square != None : 
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100)
            surface.fill((255, 255, 0))
            self.screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def make_ai_move(self):
        """AI走棋"""
        if not self.game_over and self.board.turn == self.ai_color:
            best_move = self.ai_engine.get_best_move(self.board)
            self.board.push(best_move)
            self.check_game_over()



    def handle_click(self, pos):
        """处理玩家点击（包含升变逻辑）"""
        if self.game_over or self.board.turn != self.human_color:
            return

        col = pos[0] // SQUARE_SIZE
        row = 7 - (pos[1] // SQUARE_SIZE)
        square = chess.square(col, row)

        # 选择棋子阶段
        if self.selected_square==None :
            piece = self.board.piece_at(square)
            if piece and piece.color == self.human_color:
                self.selected_square = square

        # 移动棋子阶段
        else:
            from_piece = self.board.piece_at(self.selected_square)
            move = chess.Move(self.selected_square, square)
            
            # 检测兵升变条件
            if from_piece and from_piece.piece_type == chess.PAWN:
                target_rank = chess.square_rank(square)
                if (self.human_color == chess.WHITE and target_rank == 7) or \
                (self.human_color == chess.BLACK and target_rank == 0):
                    # 显示升变选择菜单
                    move = self.handle_promotion(move)
            
            if move in self.board.legal_moves:
                self.board.push(move)
                self.check_game_over()
                if not self.game_over:
                    self.make_ai_move()
            self.selected_square = None









    def handle_promotion(self, move):
        """显示升变选择界面"""
        # 创建选择菜单
        promotion_pieces = [
            (chess.QUEEN, "Q"),
            (chess.ROOK, "R"),
            (chess.BISHOP, "B"),
            (chess.KNIGHT, "N")
        ]
        
        # 在棋盘上方绘制选择框
        menu_width = SQUARE_SIZE * 4
        menu_height = SQUARE_SIZE
        menu_x = (chess.square_file(move.to_square) * SQUARE_SIZE) - 1.5 * SQUARE_SIZE
        menu_y = 50 if self.board.turn == chess.WHITE else BOARD_SIZE - 50 - menu_height
        
        # 绘制背景
        menu_surface = pygame.Surface((menu_width, menu_height))
        menu_surface.fill((200, 200, 200))
        
        # 绘制选项
        for i, (piece_type, symbol) in enumerate(promotion_pieces):
            rect = pygame.Rect(i*SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(menu_surface, (150, 150, 150), rect)
            
            # 显示棋子图标
            color = "w" if self.board.turn == chess.WHITE else "b"
            piece_key = f"{color}{symbol}"
            menu_surface.blit(self.pieces[piece_key], (i*SQUARE_SIZE, 0))
        
        # 显示菜单并获取选择
        self.screen.blit(menu_surface, (menu_x, menu_y))
        pygame.display.flip()
        
        # 等待玩家选择
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height:
                        index = int((x - menu_x) // SQUARE_SIZE) #式转换为整数
                        return chess.Move(move.from_square, move.to_square, promotion=promotion_pieces[index][0])


    def check_game_over(self):
        """检查游戏结束状态"""
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            print(f"Checkmate! {winner} wins!")
            self.game_over = True
        elif self.board.is_stalemate():
            print("Draw by stalemate!")
            self.game_over = True
        elif self.board.is_insufficient_material():
            print("Draw by insufficient material!")
            self.game_over = True

    def run(self):
        """主游戏循环"""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine.quit()
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.screen.fill((0, 0, 0))
            self.draw_board()
            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    if not os.path.exists("img"):
        print("警告：缺少img目录和棋子图片！")
    
    game = ChessGame(ai_color=chess.BLACK)
    game.run()