"""
国际象棋人机对战程序
需要提前准备：
1. 安装依赖：pip install pygame python-chess
2. 下载Stockfish引擎：https://stockfishchess.org/download/
3. 创建img目录并放置棋子PNG素材（文件名格式：wP.png, bK.png等）
"""

import pygame
import chess
from chess import engine
import os

# 棋子图片尺寸
SQUARE_SIZE = 68
BOARD_SIZE = SQUARE_SIZE * 8

class ChessGame:
    def __init__(self, ai_color=chess.BLACK, engine_path="stockfish"):
        # 初始化棋盘和引擎
        self.board = chess.Board()
        self.ai_color = ai_color
        self.selected_square = None
        self.human_color = not ai_color
        self.game_over = False
        
        # 初始化引擎
        self.engine = engine.SimpleEngine.popen_uci(engine_path)
        
        # Pygame初始化
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
        if self.selected_square:
            col = chess.square_file(self.selected_square)
            row = 7 - chess.square_rank(self.selected_square)
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100)
            surface.fill((255, 255, 0))
            self.screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def make_ai_move(self):
        """AI走棋"""
        result = self.engine.play(self.board, engine.Limit(time=0.5))
        self.board.push(result.move)
        self.check_game_over()

    def handle_click(self, pos):
        """处理玩家点击"""
        if self.game_over or self.board.turn != self.human_color:
            return

        col = pos[0] // SQUARE_SIZE
        row = 7 - (pos[1] // SQUARE_SIZE)
        square = chess.square(col, row)

        # 选择棋子
        if not self.selected_square:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.human_color:
                self.selected_square = square

        # 移动棋子
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.check_game_over()
                if not self.game_over:
                    self.make_ai_move()
            self.selected_square = None

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
    # 使用前需要修改为你的Stockfish路径
    engine_path = "stockfish"  # Windows: "stockfish.exe", Mac/Linux: "stockfish"
    
    if not os.path.exists("img"):
        print("警告：缺少img目录和棋子图片！")
    
    game = ChessGame(ai_color=chess.BLACK, engine_path=engine_path)
    game.run()