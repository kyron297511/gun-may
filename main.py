from tkinter import *
import game


class Launcher(Tk):
    def __init__(self):
        super().__init__()       
        
        self.title("Gun Mayhem Launcher")

        # canvas = Canvas(width=531, height=76)
        # canvas.grid(row=0, column=0)
        # self.title = PhotoImage(file="assets/launcher/title.gif")
        # canvas.create_image(0, 0, anchor=NW, image=self.title)

        color_options = [
            "Black",
            "Blue",
            "Green",
            "Red",
            "Yellow",
        ]

        Label(text="Enter the name for Player 1:").grid(row=0, column=0)
        Label(text="Enter the name for Player 2:").grid(row=1, column=0)
        self.player_1_name_input = Entry()
        self.player_2_name_input = Entry()
        self.player_1_name_input.insert(10, "Player 1")
        self.player_2_name_input.insert(10, "Player 2")
        self.player_1_name_input.grid(row=0, column=1)
        self.player_2_name_input.grid(row=1, column=1)

        self.player_1_color_variable = StringVar()
        self.player_1_color_variable.set(color_options[0])

        self.player_2_color_variable = StringVar()
        self.player_2_color_variable.set(color_options[0])

        Label(text="Choose the color for Player 1:").grid(row=2, column=0)
        self.player_1_color_input = OptionMenu(
            self, self.player_1_color_variable, *color_options)
        self.player_1_color_input.grid(row=2, column=1, sticky="w")
        self.player_1_color_input.configure(width=15)

        Label(text="Choose the color for Player 2:").grid(row=3, column=0)
        self.player_2_color_input = OptionMenu(
            self, self.player_2_color_variable, *color_options)
        self.player_2_color_input.grid(row=3, column=1, sticky="w")
        self.player_2_color_input.configure(width=15)

        Button(text="Launch", command=self.run_game).grid(
            row=4, column=0, sticky="e")

        Button(text="Exit", command=self.quit).grid(
            row=4, column=1, sticky="w")

    def get_input(self):
        player_1_name = self.player_1_name_input.get()
        player_2_name = self.player_2_name_input.get()
        player_1_color = self.player_1_color_variable.get().lower()
        player_2_color = self.player_2_color_variable.get().lower()

        return player_1_name, player_2_name, player_1_color, player_2_color

    def run_game(self):
        args = self.get_input()
        self.destroy()  # close launcher

        # new game
        g = game.Game(*args)
        while g.running:
            g.new()
        g.quit()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.mainloop()
