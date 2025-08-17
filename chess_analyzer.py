# Simple Chess Analyzer with GUI
# Requirements: pip install python-chess pillow
# Download Stockfish: https://stockfishchess.org/download/

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import chess, chess.engine, chess.pgn

SQUARE = 60
LIGHT, DARK = "#EEEED2", "#769656"

class SimpleChessAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Chess Analyzer")
        self.board = chess.Board()
        self.engine = None

        # Canvas for board
        self.canvas = tk.Canvas(self, width=8*SQUARE, height=8*SQUARE)
        self.canvas.pack()
        self.draw_board()

        # Menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open PGN", command=self.open_pgn)
        file_menu.add_command(label="Select Stockfish", command=self.select_engine)
        file_menu.add_command(label="Analyze Position", command=self.analyze)
        menu.add_cascade(label="File", menu=file_menu)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                color = LIGHT if (r+c)%2==0 else DARK
                x0, y0 = c*SQUARE, r*SQUARE
                self.canvas.create_rectangle(x0,y0,x0+SQUARE,y0+SQUARE, fill=color)
        for sq, piece in self.board.piece_map().items():
            r, c = divmod(sq, 8)
            char = piece.symbol().upper() if piece.color else piece.symbol()
            self.canvas.create_text(c*SQUARE+30, (7-r)*SQUARE+30, text=char, font=("Arial",32))

    def open_pgn(self):
        f = filedialog.askopenfilename(filetypes=[("PGN","*.pgn")])
        if not f: return
        with open(f) as p:
            game = chess.pgn.read_game(p)
        self.board = game.board()
        for mv in game.mainline_moves():
            self.board.push(mv)
        self.draw_board()

    def select_engine(self):
        path = filedialog.askopenfilename(title="Select Stockfish")
        if path:
            self.engine = chess.engine.SimpleEngine.popen_uci(path)
            messagebox.showinfo("Engine", "Stockfish loaded!")

    def analyze(self):
        if not self.engine:
            messagebox.showwarning("Engine", "Load Stockfish first!")
            return
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=12))
        score = info["score"].pov(self.board.turn)
        messagebox.showinfo("Analysis", f"Eval: {score}")

if __name__ == "__main__":
    app = SimpleChessAnalyzer()
    app.mainloop()
