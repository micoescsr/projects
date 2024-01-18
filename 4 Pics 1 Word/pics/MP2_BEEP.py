from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
import random
import json
import sys
import itertools
import winsound

class FourPicsOneWord():
    
    def __init__(self):
        super().__init__()
        self.gameFrame=Tk()
        self.gameFrame.title("Four Pictures One Word")
        self.gameFrame.geometry("600x600")
        self.gameFrame.configure(background="#1d222e")
        self.random=random
        self.level = 1
        self.coins = 100
        self.answer = ""
        self.picNum = 0
        self.player_count = 1

        #Exception Handling - Used as trial to see if the it will creeate a list properly and return a error message if it doesn't work
        #File Handling - Used to read the 'picList' file
        
        try:
            with open("picList.txt", "r") as f:
                self.picFiles = [line.strip().split(";")[1] for line in f.readlines()]
                print(self.picFiles)
        except Exception as e:
            print("An error occurred while reading the file")
            self.gameFrame.destroy()

        self.gameWidgets()
        self.rstButton()
        self.updtStatus()
        self.restartGame()
    
    #Menu Section
        
    def menuOption(self):
        self.menu_frame = Frame(self.status_label, width=350, height=70, bg="#1a1e27")
        self.menu_frame.place(relx=0.5, rely=0.475, anchor="center")
        self.menu_file = "widget_textures/menu.png"
        self.menu = PhotoImage(file=self.menu_file)
        self.menu_button = Button(self.menu_frame, image=self.menu, command=lambda: [self.menu_button.destroy(), self.menu_frame.destroy()], bg="#1a1e27", borderwidth=0)
        self.menu_button.image = self.menu
        self.menu_button.place(relx=0.5, rely=0.5, anchor="center")
        self.menu_button.destroy()
        self.menu_frame.destroy()

    def restartGame(self):
        self.level = 1
        self.submit_button.config(state=NORMAL)
        self.gameFrame.deiconify()
        self.rstButton()
        self.updtStatus()
        self.updtQuestion()

    def saveGame(self):
        self.picNum = self.level - 1
        self.saveFolder = "player_saved_data"
        os.makedirs(self.saveFolder, exist_ok=True)
        self.player_name = None
        for i in range(1, 101):
            if not os.path.exists(os.path.join(self.saveFolder, f"player{i}.json")):
                self.player_name = f"player{i}"
                break
        if self.player_name is None:
            print("Error: All player files already exist")
            return
        self.fileSave = filedialog.asksaveasfilename(
            initialdir="player_saved_data",
            initialfile=f"{self.player_name}.json",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if self.fileSave:
            with open(self.fileSave, "w") as f:
                self.data = {
                    "player_name": self.player_name,
                    "level": self.level,
                    "coins": self.coins,
                    "pic_num": self.picNum
                }
                json.dump(self.data, f)
            self.player_count += 1
        
    def loadGame(self):
        self.openFile = filedialog.askopenfilename(initialdir="savefile", title="Select saved game file", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if self.openFile:
            with open(self.openFile, "r") as f:
                self.data = json.load(f)
                self.level = self.data.get("level", 1)
                self.coins = self.data.get("coins", 0)
                self.picNum = self.data.get("pic_num", 0)
            self.pics.config(file=self.picFiles[self.picNum].lower() + ".png")
            self.updtStatus()
            self.updtQuestion()
            self.rstButton()
            self.hint_button.config(state=NORMAL)

    
    def exitGame(self):
        self.gameFrame.destroy()


    #Show Pictures
        
    def changePic(self):
        self.picNum = (self.picNum + 1) % len(self.picFiles)
        self.pics.config(file=self.picFiles[self.picNum].lower() + ".png")
        self.rstButton()
        self.updtStatus()


    #Keyboard and Button Functions
        
    def finalAnswer(self):
        winsound.PlaySound('sounds/submit.wav',1)
        if set(self.answer.lower()) == set(self.picFiles[self.picNum].lower()) and \
                all(x in self.picFiles[self.picNum].lower() for x in self.answer.lower()):
            self.coins += 10
            self.level += 1
            self.updtStatus()
            self.finishGame()
            self.changePic()
        
    def skipLevel(self):
        winsound.PlaySound('sounds/skip.wav',1)
        if self.coins >= 10:
            self.coins -= 10
            self.level += 1
            self.updtStatus()
            self.finishGame()
            self.changePic()
            self.updtQuestion()

    def useHint(self):
        if self.coins >= 2 and len(self.answer) < len(self.picFiles[self.picNum].lower()):
            self.hintLetter = self.random.choice([c for c in self.picFiles[self.picNum].lower() if c not in self.answer])
            self.answer += self.hintLetter
            self.coins -= 2
            self.updtQuestion()
            self.updtStatus()
            if len(self.answer) == len(self.picFiles[self.picNum].lower()):
                self.hint_button.config(state=DISABLED)
        elif self.coins < 2:
            self.hint_button.config(state=DISABLED)
        winsound.PlaySound('sounds/hint.wav',1)

    def buttonSelect(self, button):
        letter = button["text"].lower()
        if letter in self.picFiles[self.picNum].lower() and letter not in self.answer:
            self.answer += letter
            self.updtQuestion()
            winsound.PlaySound('sounds/button.wav',1)
            button.config(state=DISABLED)
        else:
            self.updtStatus()
            winsound.PlaySound('sounds/button.wav',1)
            button.config(state=DISABLED)


    #State of Button when Clicked
            
    def rstButton(self):
        self.answer = ""
        self.updtQuestion()
        self.letters = list(set(self.picFiles[self.picNum].upper()))
        while len(self.letters) < 12:
            self.new_letter = chr(random.randint(65, 90))
            if self.new_letter not in self.letters:
                self.letters.append(self.new_letter)
        random.shuffle(self.letters)
        for i in range(3):
            for j in range(4):
                index = i*4 + j
                if self.letters[index].lower() in self.picFiles[self.picNum]:
                    self.buttons[index].config(text=self.letters[index], command=lambda button=self.buttons[index]: self.buttonSelect(button), state=NORMAL)
                else:
                    self.buttons[index].config(text=self.letters[index], command=None, state=NORMAL)
        self.all_clicked = all([button["text"].lower() in self.picFiles[self.picNum].lower() for button in self.buttons if button["state"] == DISABLED])
        if self.all_clicked:
            self.hint_button.config(state=DISABLED)
        else:
            self.hint_button.config(state=NORMAL)


    #Update Coin Amount and Level No.
            
    def updtStatus(self):
        self.level_text.config(text=f"Level {self.level}")
        self.coins_label.config(text=f"{self.coins}")
        if self.coins >= 2:
            self.hint_button.config(state=NORMAL)
        else:
            self.hint_button.config(state=DISABLED)
        if self.coins >= 10 and self.level < 51:
            self.skip_button.config(state=NORMAL)
        else:
            self.skip_button.config(state=DISABLED)

    def updtQuestion(self):
        self.display = ""
        for c in self.picFiles[self.picNum]:
            if c.lower() in self.answer:
                self.display += c.upper() + " "
            else:
                self.display += "\u2B1B\ufe0f " 
        self.inputed_font = font.Font(family="Courier", size=15, weight="bold")
        self.inputed.config(text=self.display.strip(), font=self.inputed_font, padx=10, pady=10, bg="#1d222e", fg="#FFFFFF")

    def finishGame(self):
        if self.level == 51:
            winsound.PlaySound('sounds/victory.wav',1)
            self.gm_image = PhotoImage(file="widget_textures/background.png")
            self.gm_label = Label(self.gameFrame, image=self.gm_image)
            self.gm_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.victory = PhotoImage(file="widget_textures/victory.png")
            self.victory_icon = Label(image=self.victory, bg="#1d222e")
            self.victory_icon.place(relx=0.5, rely=0.475, anchor="center")
            self.victory_text = Label(text="You WON!", bg="#1d222e", font=("Courier", 25, "bold"), foreground="white")
            self.victory_text.place(relx=0.5, rely=0.25, anchor="center")
            self.credits = Label(text="Made by:\nMico Efraim Escosura\nKurt Alan Pasajol\nMaria Anne Phaula Briol\nCarlie Shaye Endaya", bg="#1d222e", font=("Courier", 12, "bold"), foreground="white")
            self.credits.place(relx=0.5, rely=0.75, anchor="center")
            for button in self.buttons:
                button.config(state=DISABLED)
            self.hint_button.config(state=DISABLED)
            self.skip_button.config(state=DISABLED)
            self.submit_button.config(state=DISABLED)

    #Widgets/Frames/Appearance
            
    def gameWidgets(self):
        self.gm_image = PhotoImage(file="widget_textures/background.png")
        self.gm_label = Label(self.gameFrame, image=self.gm_image)
        self.gm_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.status_label = Frame(self.gameFrame, width=900, height=50, bg="#1a1e27")
        self.status_label.pack(side="top", fill="both", expand=False)
        self.border_line = Frame(self.status_label, width=900, height=2, bg="#FFFFFF")
        self.border_line.pack(side="bottom", fill="both")

        self.save_button = Button(self.status_label, text="Save Game", command=self.saveGame, bg="#d4d4d4", font=("Courier", 10, "bold"))
        self.save_button.place(relx=0.35, rely=0.28, anchor="center")

        self.load_button = Button(self.status_label, text="Load Game", command=self.loadGame, bg="#d4d4d4", font=("Courier", 10, "bold"))
        self.load_button.place(relx=0.495, rely=0.28, anchor="center")

        self.exit_button = Button(self.status_label, text="Exit Game", command=self.exitGame, bg="#d4d4d4", font=("Courier", 10, "bold"))
        self.exit_button.place(relx=0.6418, rely=0.28, anchor="center")

        self.back_button = Button(self.status_label, text="Back", command=lambda: [self.menu_frame.destroy(), self.menu_button.destroy(), self.menuOption()], bg="#d4d4d4", font=("Courier", 10, "bold"))
        self.back_button.place(relx=0.5, rely=0.675, anchor="center")

        self.menu_frame = Frame(self.status_label, width=350, height=70, bg="#1a1e27")
        self.menu_frame.place(relx=0.5, rely=0.475, anchor="center")
        self.menu = PhotoImage(file="widget_textures/menu.png")
        self.menu_button = Button(self.menu_frame, image=self.menu, command=lambda: [self.menu_button.destroy(), self.menu_frame.destroy()], bg="#1a1e27", borderwidth=0)
        self.menu_button.place(relx=0.5, rely=0.5, anchor="center")

        self.level_text = Label(self.status_label, font=("Courier", 20, "bold"))
        self.level_text.configure(background="#1a1e27", foreground="white")
        self.level_text.pack(side="left", padx=5)

        self.coins_label = Label(self.status_label, font=("Courier", 18, "bold"))
        self.coins_label.configure(background="#1a1e27", foreground="white")
        self.coins_label.pack(side="right", padx=4)
        self.coin = PhotoImage(file="widget_textures/coin.png")
        self.coin_icon = Label(self.status_label, image=self.coin, width=40, height=40)
        self.coin_icon.configure(background="#1a1e27", foreground="white")
        self.coin_icon.pack(side="right", padx=0.1, pady=15)

        self.pic_frame = Frame(self.gameFrame, width=25)
        self.pic_frame.configure(background="#1d222e")
        self.pic_frame.place(relx=0.5, rely=0.480, anchor="center")
        self.pic_frame = Frame(self.gameFrame, width=250, height=250)
        self.pic_frame.configure(background="#1d222e")
        self.pic_frame.place(relx=0.5, rely=0.480, anchor="center")

        self.pics = PhotoImage(file=self.picFiles[self.picNum] + ".png")
        self.image_label = Label(self.pic_frame, image=self.pics)
        self.image_label.pack(side="top")

        self.inputed = Label(self.pic_frame, text="", font=("Courier", 20, "bold"),)
        self.inputed.pack(side="top", pady=10)

        self.keyboard_frame = Frame(self.gameFrame, width=440, height=400)
        self.keyboard_frame.configure(background="#1d222e")
        self.keyboard_frame.place(relx=0.5, rely=0.9, anchor="center")

        self.buttons = []
        for i in range(2):
            for j in range(6):
                index = i*4 + j
                button = Button(self.keyboard_frame, text="", width=3, height=1, font=("Courier", 16, "bold"), bg="#d4d4d4", anchor="center")
                button.grid(row=i, column=j, padx=4, pady=4, sticky="nsew")
                self.buttons.append(button)

        self.submit = PhotoImage(file="widget_textures/submit.png")
        self.submit_button = Button(image=self.submit, command=self.finalAnswer,  borderwidth=0, activebackground = "#1d222e")  
        self.submit_button.configure(background="#1d222e", foreground="#1d222e")
        self.submit_button.place(relx=0.115, rely=0.85)

        self.skip = PhotoImage(file="widget_textures/skip.png")
        self.skip_button = Button(image=self.skip, command=self.skipLevel, borderwidth=0, activebackground = "#1d222e") 
        self.skip_button.configure(background="#1d222e", foreground="#1d222e")
        self.skip_button.place(relx=0.8, rely=0.85)

        self.hint = PhotoImage(file="widget_textures/hint.png")
        self.hint_button = Button(image=self.hint, command=self.useHint, borderwidth=0, activebackground = "#1d222e") 
        self.hint_button.configure(background="#1d222e", foreground="#1d222e")
        self.hint_button.place(relx=0.775, rely=0.2)

        self.submit_button.config(width=50, height=50)
        self.skip_button.config(width=50, height=50)
        self.hint_button.config(width=50, height=50)

        self.finishGame()

def main():
    root = FourPicsOneWord()
    
if __name__=="__main__":
    main()
