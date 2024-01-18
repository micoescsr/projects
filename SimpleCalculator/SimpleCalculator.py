from tkinter import *

#window is just an identifier
class window(Frame):#palaging may "self" as an identifier
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title('Simple Calculator')
        self.first_number_entry = Entry(self,width=20)
        self.second_number_entry = Entry(self,width=20)

        #label is used to display number
        lblFirstnum = Label(self,text='First Number:')
        lblSecnum = Label(self,text='Second Number:')
        self.result_label = Label(self,text='Result',width=20)

        add_button = Button(self,text='+',width=7,command=self.getSum)
        subtract_button = Button(self,text='-',width=7,command=self.getDiff)
        multiply_button = Button(self,text='x',width=7,command=self.getProd)
        divide_button = Button(self,text='/',width=7,command=self.getQuo)

        lblFirstnum.grid(row=0,column=0,pady=3,columnspan=3)
        self.first_number_entry.grid(row=0,column=3,columnspan=2)
        lblSecnum.grid(row=1,column=0,pady=3,columnspan=3)
        self.second_number_entry.grid(row=1,column=3,columnspan=2)

        add_button.grid(row=2,column=0,pady=3)
        subtract_button.grid(row=2,column=1,pady=3)
        multiply_button.grid(row=2,column=3,pady=3)
        divide_button.grid(row=2,column=4,pady=3)
        self.result_label.grid(row=3,column=0,columnspan=5)

        self.pack()

    def getSum(self):
        num1 = self.first_number_entry.get()
        num2 = self.second_number_entry.get()
        a = int(num1) + int(num2)
        self.result_label.config(text=f'Sum: {a}')

    def getDiff(self):
        num1 = self.first_number_entry.get()
        num2 = self.second_number_entry.get()
        b = int(num1) - int(num2)
        self.result_label.config(text=f'Difference: {b}')

    def getProd(self):
        num1 = self.first_number_entry.get()
        num2 = self.second_number_entry.get()
        c = int(num1) * int(num2)
        self.result_label.config(text=f'Product: {c}')

    def getQuo(self):
        num1 = self.first_number_entry.get()
        num2 = self.second_number_entry.get()
        d = int(num1) / int(num2)
        self.result_label.config(text=f'Division: {d}')


def main():
    root = Tk()
    root.geometry('300x150')
    app = window(root)
    root.mainloop()

main()
