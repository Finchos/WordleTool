import customtkinter as ctk
import re
from solver import Solver

# Globální nastavení vzhledu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wordle Solver")
        self.geometry("450x730")

        self.engine = Solver()

        self.current_active_row = 0
        self.current_active_col = 0
        self.is_game_over = False

        # UPPER PART (Grid)

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(pady=20)

        self.tiles = []
        for row in range(6):
            row_tiles = []
            for col in range(5):
                tile = ctk.CTkFrame(self.grid_frame, width=55, height=55, fg_color="gray", corner_radius=5,
                                    border_width=0, border_color="white")
                tile.grid(row=row, column=col, padx=5, pady=5)
                tile.grid_propagate(False)

                lbl = ctk.CTkLabel(tile, text="", font=("Arial", 28, "bold"), text_color="white")
                lbl.place(relx=0.5, rely=0.5, anchor="center")

                tile.bind("<Button-1>", lambda event, f=tile: self.change_color(f))
                lbl.bind("<Button-1>", lambda event, f=tile: self.change_color(f))

                row_tiles.append((tile, lbl))
            self.tiles.append(row_tiles)

        # Info & Button

        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.pack(pady=10, fill="x", padx=40)

        self.optimal_label = ctk.CTkLabel(self.middle_frame, text="Type First Word", font=("Arial", 18, "bold"))
        self.optimal_label.pack(side="left")

        self.eval_button = ctk.CTkButton(self.middle_frame, text="Evaluate", width=120, command=self.evaluate_action)
        self.eval_button.pack(side="right")

        # Scrolling List of Answers

        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Possible Answers")
        self.scroll_frame.pack(pady=10, padx=40, fill="both", expand=True)

        self.answer_labels = []
        self.update_answers_list(["(Enter first word)"])


        self.bind_all("<Key>", self.handle_keypress)
        self.update_active_tile_highlight()


    # UI Functions (view and controll)

    def handle_keypress(self, event):
        if self.is_game_over or self.current_active_row > 5:
            return

        key = event.char
        keysym = event.keysym

        if re.match(r'^[a-zA-Z]$', key):
            if self.current_active_col < 5:
                tile_frame, tile_label = self.tiles[self.current_active_row][self.current_active_col]
                tile_label.configure(text=key.upper())
                self.update_active_tile_highlight(remove=True)
                self.current_active_col += 1
                self.update_active_tile_highlight()

        elif keysym == "BackSpace":
            if self.current_active_col == 5:
                self.update_active_tile_highlight(remove=True)
                self.current_active_col -= 1
                tile_frame, tile_label = self.tiles[self.current_active_row][self.current_active_col]
                tile_label.configure(text="")
                self.update_active_tile_highlight()
            elif self.current_active_col > 0:
                self.update_active_tile_highlight(remove=True)
                self.current_active_col -= 1
                tile_frame, tile_label = self.tiles[self.current_active_row][self.current_active_col]
                tile_label.configure(text="")
                self.update_active_tile_highlight()

        elif keysym == "Return" or keysym == "Enter":
            if self.current_active_col == 5:
                self.evaluate_action()

    def update_active_tile_highlight(self, remove=False):
        if self.current_active_row > 5 or self.current_active_col > 4:
            return
        tile_frame, _ = self.tiles[self.current_active_row][self.current_active_col]
        if remove:
            tile_frame.configure(border_width=0, fg_color=tile_frame.cget("fg_color"))
        else:
            tile_frame.configure(border_width=2, fg_color="#333333")

    def change_color(self, tile_frame):
        current_color = tile_frame.cget("fg_color")
        yellow = "#b59f3b"
        green = "#538d4e"
        gray = "gray"

        if current_color == gray or current_color == "#333333":
            new_color = yellow
        elif current_color == yellow:
            new_color = green
        else:
            new_color = gray

        tile_frame.configure(fg_color=new_color)

    def update_answers_list(self, words_list):
        for lbl in self.answer_labels:
            lbl.destroy()
        self.answer_labels.clear()

        display_limit = 200
        for word in words_list[:display_limit]:
            lbl = ctk.CTkLabel(self.scroll_frame, text=word.upper(), font=("Arial", 16))
            lbl.pack(anchor="w", pady=2, padx=10)
            self.answer_labels.append(lbl)

        info_text = f"Possible Answers ({len(words_list)})"
        if len(words_list) > display_limit:
            info_text += " - first 200"
        self.scroll_frame.configure(label_text=info_text)

    # Solver DATA

    def evaluate_action(self):
        if self.current_active_col != 5:
            return

        word_ui = ""
        colors_ui = []
        color_map = {"gray": 0, "#333333": 0, "#b59f3b": 1, "#538d4e": 2}

        for col in range(5):
            tile_frame, tile_label = self.tiles[self.current_active_row][col]
            word_ui += tile_label.cget("text").lower()
            bg_color = tile_frame.cget("fg_color")
            colors_ui.append(color_map.get(bg_color, 0))

        W = tuple(word_ui)
        S = tuple(colors_ui)

        remaining_answers = self.engine.process_turn(W, S)

        self.update_answers_list(sorted(list(remaining_answers)))

        if len(remaining_answers) == 0:
            self.optimal_label.configure(text="Tajenka nenalezena", text_color="red")
        elif len(remaining_answers) == 1:
            win_word = list(remaining_answers)[0].upper()
            self.optimal_label.configure(text=f"Solution: {win_word}", text_color="#538d4e")
        else:
            self.optimal_label.configure(text="Calculating...", text_color="#b59f3b")
            self.update()

            best_word = self.engine.pick_optimal_word()

            self.optimal_label.configure(text=f"Optimal Word: {best_word.upper()}", text_color="white")

        self.update_active_tile_highlight(remove=True)
        self.current_active_row += 1
        self.current_active_col = 0

        if self.current_active_row > 5:
            self.is_game_over = True
        else:
            self.update_active_tile_highlight()


if __name__ == "__main__":
    app = ToolApp()
    app.mainloop()