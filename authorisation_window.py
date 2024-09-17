from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle

window = tk.Tk()
window.title('Добро пожаловать!')
window.geometry('450x252')
window.resizable(False, False)
window.iconphoto(True, tk.PhotoImage(file = 'C:/Users/User/Desktop/pythonProject/files/images/Tanks_icon.png'))

background = tk.PhotoImage(file = 'C:/Users/User/Desktop/pythonProject/files/images/Background_log.png')
canvas = tk.Canvas(window, width = 450, height = 250)
canvas.create_image(225, 125, anchor = 'center', image = background)
canvas.place(x = 0, y = 0)

def registration():

    regwindow = tk.Toplevel(window)
    regwindow.title('Регистрируйся и играй!')
    regwindow.geometry('450x252')
    regwindow.resizable(False, False)

    def save():
        logpass_save = {}
        logpass_save[reglogentry.get()] = regpassentry.get()
        data = open('C:/Users/User/Desktop/pythonProject/files/Database.txt', 'ab')
        pickle.dump(logpass_save, data)
        print(data)
        data.close()
        messagebox.showinfo('Успешно!', 'Вы успешно зарегистрировались в игре!')
        regwindow.destroy()   

    background = tk.PhotoImage(file = 'C:/Users/User/Desktop/pythonProject/files/images/Background_log.png')
    canvas = tk.Canvas(regwindow, width = 450, height = 250)
    canvas.create_image(225, 125, anchor = 'center', image = background)
    canvas.place(x = 0, y = 0)

    reglabel = tk.Label(regwindow, text = 'Регистрация в игре "Tanks"', font = 'Calibri 15 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 7)
    reglabel.place(x = 100, y = 5)

    regloglabel = tk.Label(regwindow, text = 'Придумайте логин:', font = 'Calibri 12 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 5)
    regloglabel.place(x = 155, y = 50)

    reglogentry = tk.Entry(regwindow, text = '', font = 'Calibri 12 bold italic', width = 30, relief = 'ridge', borderwidth = 5, bg = 'gray20', fg = 'orange')
    reglogentry.place(x = 102, y = 85)

    regpasslabel = tk.Label(regwindow, text = 'Придумайте пароль:', font = 'Calibri 12 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 5)
    regpasslabel.place(x = 150, y = 125)

    regpassentry = tk.Entry(regwindow, text = '', show = '*', font = 'Calibri 12 bold italic', width = 30, relief = 'ridge', borderwidth = 5, bg = 'gray20', fg = 'orange')
    regpassentry.place(x = 102, y = 160)

    regenterbutton = tk.Button(regwindow, text = 'Создать аккаунт!', font = 'Calibri 15 bold', relief = 'ridge', borderwidth = 5, bg = 'orange', fg = 'black', command = lambda: save())
    regenterbutton.place(x = 142, y = 200)
    
    canvas.mainloop()
    
def enter():
    x = []
    with open('C:/Users/User/Desktop/pythonProject/files/Database.txt', 'rb') as fr:
        try:
            while True:
                x.append(pickle.load(fr))
        except EOFError:
            pass
    print(x)
    check = 0
    for el in x:
        if logentry.get() in el:
            if passentry.get() == el[logentry.get()]:
                print(el)
                print(el[logentry.get()])
                check += 1
                break
    if check == 1:
        print(el[logentry.get()])
        messagebox.showinfo('Приветствую вас!', 'Добро пожаловать в игру!')
    else:
        messagebox.showerror('Ошибка!', 'Неправильно введены логин и(или) пароль!')

greeting = tk.Label(window, text = 'Добро пожаловать в игру  "Tanks"', font = 'Calibri 15 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 7)
greeting.place(x = 67, y = 5)

loglabel = tk.Label(window, text = 'Введите логин:', font = 'Calibri 12 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 5)
loglabel.place(x = 170, y = 50)

logentry = tk.Entry(window, text = '', font = 'Calibri 12 bold italic', width = 30, relief = 'ridge', borderwidth = 5, bg = 'gray20', fg = 'orange')
logentry.place(x = 102, y = 85)

passlabel = tk.Label(window, text = 'Введите пароль:', font = 'Calibri 12 bold', bg = 'black', fg = 'orange', relief = 'ridge', borderwidth = 5)
passlabel.place(x = 165, y = 125)

passentry = tk.Entry(window, text = '', show = '*', font = 'Calibri 12 bold italic', width = 30, relief = 'ridge', borderwidth = 5, bg = 'gray20', fg = 'orange')
passentry.place(x = 102, y = 160)

enterbutton = tk.Button(window, text = "Войти", font = 'Calibri 15 bold', relief = 'ridge', borderwidth = 5, bg = 'orange', fg = 'black', command = lambda: enter())
enterbutton.place(x = 85, y = 200)

enterbutton = tk.Button(window, text = "У меня нет аккаунта...", font = 'Calibri 15 bold', relief = 'ridge', borderwidth = 5, bg = 'orange', fg = 'black', command = registration)
enterbutton.place(x = 163, y = 200)

window.mainloop()

