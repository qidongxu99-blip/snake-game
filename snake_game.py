"""
贪吃蛇小游戏 - Snake Game (tkinter 版)
使用 Python 内置 tkinter，无需安装任何依赖
操作：方向键控制方向，吃食物加分，撞墙或撞自己游戏结束
      游戏结束后按空格重新开始
"""

import tkinter as tk
import random

# ==================== 配置 ====================
CELL = 20              # 每格像素
COLS = 30              # 列数
ROWS = 30              # 行数
WIDTH = CELL * COLS    # 画布宽
HEIGHT = CELL * ROWS   # 画布高
SPEED = 120            # 帧间隔(毫秒)
MIN_SPEED = 50

BG = "#1a1a2e"
SNAKE_HEAD = "#00e676"
SNAKE_BODY = "#69f0ae"
FOOD = "#ff1744"


class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()

        self.score_var = tk.StringVar()
        self.score_label = tk.Label(self.root, textvariable=self.score_var,
                                    font=("Courier", 14, "bold"),
                                    fg="white", bg=BG)
        self.score_label.pack(fill="x")

        # 键盘
        self.root.bind("<Up>", lambda e: self.change_dir("up"))
        self.root.bind("<Down>", lambda e: self.change_dir("down"))
        self.root.bind("<Left>", lambda e: self.change_dir("left"))
        self.root.bind("<Right>", lambda e: self.change_dir("right"))
        self.root.bind("<space>", lambda e: self.restart())

        self.reset()
        self.root.mainloop()

    def reset(self):
        cx = COLS // 2
        cy = ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.speed = SPEED
        self.game_over = False
        self.spawn_food()
        self.update_score()
        self.draw()
        self.root.after(self.speed, self.tick)

    def change_dir(self, d):
        opp = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if d != opp.get(self.direction):
            self.next_direction = d

    def spawn_food(self):
        empty = set()
        for x in range(COLS):
            for y in range(ROWS):
                empty.add((x, y))
        for seg in self.snake:
            empty.discard(seg)
        self.food = random.choice(list(empty))

    def tick(self):
        if self.game_over:
            return

        self.direction = self.next_direction

        hx, hy = self.snake[0]
        if self.direction == "up":
            hy -= 1
        elif self.direction == "down":
            hy += 1
        elif self.direction == "left":
            hx -= 1
        elif self.direction == "right":
            hx += 1

        new_head = (hx, hy)

        # 撞墙
        if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
            self.end_game()
            return

        # 撞自己
        if new_head in self.snake:
            self.end_game()
            return

        # 移动
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.speed = max(MIN_SPEED, self.speed - 3)
            self.spawn_food()
            self.update_score()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(self.speed, self.tick)

    def draw(self):
        self.canvas.delete("all")
        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            px = x * CELL
            py = y * CELL
            self.canvas.create_rectangle(px, py, px + CELL, py + CELL,
                                         fill=color, outline="")
        fx, fy = self.food
        self.canvas.create_oval(fx * CELL, fy * CELL,
                                 fx * CELL + CELL, fy * CELL + CELL,
                                 fill=FOOD, outline="")

    def update_score(self):
        self.score_var.set("  Score: {}    Speed: {}ms".format(self.score, self.speed))

    def end_game(self):
        self.game_over = True
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 30,
                                 text="GAME OVER", fill="#ff1744",
                                 font=("Courier", 36, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20,
                                 text="Score: {}".format(self.score), fill="white",
                                 font=("Courier", 24, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 70,
                                 text="Press SPACE to restart", fill="#888888",
                                 font=("Courier", 16, "normal"))

    def restart(self):
        if self.game_over:
            self.reset()


if __name__ == "__main__":
    SnakeGame()