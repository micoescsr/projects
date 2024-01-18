from tkinter import *
import random

#=========================================================

class Window(Frame):
    def __init__(self, master=None):
        self.master = master
        self.init_window()
        self.master.geometry('524x450')

    def init_window(self):
        self.master.title('Simple Color Game')
        self.v = StringVar()
        self.v.set(None)

#============= COLOR BUTTONS =============================
        #YELLOW
        yellow_button = Radiobutton(self.master, text='YELLOW', width=10, height=1, font='Times 14 bold', variable=self.v, value='yellow', bg='yellow')
        yellow_button.place(x=50, y=50)

        #GREEN
        green_button = Radiobutton(self.master, text='GREEN', width=10, height=1, font='Times 14 bold', variable=self.v, value='green', bg='darkolivegreen3')
        green_button.place(x=190, y=50)

        #BLUE
        blue_button = Radiobutton(self.master, text='BLUE', width=10, height=1, font='Times 14 bold', variable=self.v, value='blue', bg='lightskyblue')
        blue_button.place(x=331, y=50)

        #PINK
        pink_button = Radiobutton(self.master, text='PINK', width=10, height=1, font='Times 14 bold', variable=self.v, value='pink', bg='pink')
        pink_button.place(x=50, y=83)

        #RED
        red_button = Radiobutton(self.master, text='RED', width=10, height=1, font='Times 14 bold', variable=self.v, value='red', bg='firebrick2')
        red_button.place(x=190, y=83)

        #ORANGE
        orng_button = Radiobutton(self.master, text='ORANGE', width=10, height=1, font='Times 14 bold', variable=self.v, value='orange', bg='orange1')
        orng_button.place(x=331, y=83)
#============================================================

        self.Label_1 = Label(self.master, bg='black', width=19, height=15)
        self.Label_1.place(x=50, y=135)
        self.Label_Two = Label(self.master, bg='black', width=19, height=15)
        self.Label_Two.place(x=190, y=135)
        self.Label_Three = Label(self.master, bg='black', width=19, height=15)
        self.Label_Three.place(x=330, y=135)

        self.plyr_Coin = 100

        self.spin_size = Spinbox(self.master, from_=1, to=self.plyr_Coin, width=5)
        self.spin_size.place(x=240, y=380)

        self.betLabel = Label(self.master, text='BET', font='Times 10')
        self.betLabel.place(x=200, y=378)

        self.coin_Label = Label(self.master, text=f'Coins: {str(self.plyr_Coin)}', font='Times 10')
        self.coin_Label.place(x=100, y=378)

        self.roll_button = Button(self.master, text='ROLL!', font='Times 10', width=8, command=self.play_game)
        self.roll_button.place(x=340, y=376)

#============================================================

    def play_game(self):
        color_select = self.v.get()
        bet_quantity = int(self.spin_size.get())

        if color_select is None:
            self.update_label("Choose Color First")
            return

        if bet_quantity > self.plyr_Coin:
            self.update_label("Invalid Bet")
            return

        self.plyr_Coin -= bet_quantity
        self.coin_Label.configure(text=f'Coins: {str(self.plyr_Coin)}')

        color_list = ['yellow', 'darkolivegreen3', 'lightskyblue', 'pink', 'firebrick2', 'orange1']
        random.shuffle(color_list)

        self.Label_1.configure(bg=color_list[0])
        self.Label_Two.configure(bg=color_list[1])
        self.Label_Three.configure(bg=color_list[2])

        if color_select == color_list[0]:
            self.plyr_Coin += bet_quantity * 2
            self.update_label("You Won!")
        elif color_select == color_list[1]:
            self.plyr_Coin += int(bet_quantity * 1.5)
            self.update_label("You Won!")
        elif color_select == color_list[2]:
            self.plyr_Coin += int(bet_quantity * 1.2)
            self.update_label("You Won!")
        else:
            self.update_label("You Lose!")

        self.coin_Label.configure(text=f'Coins: {str(self.plyr_Coin)}')

    def update_label(self, message):
        self.roll_button.configure(text=message)
        self.master.after(2000, lambda: self.roll_button.configure(text='ROLL!'))

root = Tk()
app = Window(root)
root.mainloop()