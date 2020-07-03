from fractions import Fraction
from tkinter import font
from threading import Thread
import argparse
import queue
import sys
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import threading
import time
import speech_recognition as s_r
from tkinter import *
from sympy import Eq, symbols, solve
import numpy as np
import matplotlib.pyplot as plt
from soundGraph import waveGraph
from math import *

expression = ""


# print(s_r.Microphone.list_microphone_names())
def record():
    try:
        t1 = threading.Thread(target=waveGraph)
        t2 = threading.Thread(target=speech_input)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()
    except:
        pass


def speech_input():
    global expression
    my_mic_device = s_r.Microphone(device_index=1)
    r = s_r.Recognizer()
    with my_mic_device as source:
        print("Nói phép tính, ví dụ: 1 + 1")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    expression = r.recognize_google(audio, language="vi-VN")
    print(expression)
    parseExpression()
    if "=" and "vẽ" in expression:
        equation.set(expression)
        expression = expression.replace(" ", "")
    elif "=" in expression:
        expression = expression.replace("=", "")
        equation.set(expression)
        expression = expression.replace(" ", "")
        equalpress()
    else:
        equation.set(expression)
        expression = expression.replace(" ", "")
    plt.close()


def parseExpression():
    global expression
    expression = expression.replace("cộng", "+")
    expression = expression.replace("trừ", "-")
    expression = expression.replace("chia", "/")
    expression = expression.replace("mũ", "**")
    expression = expression.replace("bình", "**2")
    # if "x" in expression:
    #     for i in range(0, len(expression)):
    #         if i > 0 and expression[i] == "x":
    #             if expression[i + 1] == "+" or expression[i + 1] == "-" or expression[i + 1] == "x" \
    #                     or expression[i + 1] == "/" or expression[i + 1] == "*" or expression[i + 1] == "(":
    #                 pass
    #             else:
    #                 expression = expression.replace("x", "*")
    #         if i > len(expression) - 1 and expression[i] == "x":
    #             if expression[i - 1] == "+" or expression[i - 1] == "-" or expression[i - 1] == "x" \
    #                     or expression[i - 1] == "/" or expression[i - 1] == "*" or expression[i - 1] == ")":
    #                 pass
    #             else:
    #                 expression = expression.replace("x", "*")
    expression = expression.replace("x", "*")
    expression = expression.replace("nhân", "*")
    expression = expression.replace("căn", "**(1/2)")
    expression = expression.replace("mở ngoặc", "(")
    expression = expression.replace("đóng ngoặc", ")")
    expression = expression.replace("không", "0")
    expression = expression.replace("một", "1")
    expression = expression.replace("hai", "2")
    expression = expression.replace("ba", "3")
    expression = expression.replace("bốn", "4")
    expression = expression.replace("năm", "5")
    expression = expression.replace("sáu", "6")
    expression = expression.replace("bảy", "7")
    expression = expression.replace("tám", "8")
    expression = expression.replace("chín", "9")

    # if "tỷ" in expression and "chục triệu" in expression:
    #     expression = expression.replace("tỷ", "0")
    # if "tỷ" in expression and "mươi triệu" in expression:
    #     expression = expression.replace("tỷ", "0")
    # elif "tỷ" in expression and "trăm triệu" in expression:
    #     expression = expression.replace("tỷ", "")
    # elif "tỷ" in expression and "triệu" in expression:
    #     expression = expression.replace("tỷ", "00")
    # else:
    #     expression = expression.replace("tỷ", "000000000")
    expression = expression.replace("lôgarit", "log")
    expression = expression.replace("logarit", "log")
    expression = expression.replace("số pi", "pi")
    expression = expression.replace("số p", "pi")
    expression = expression.replace("Phi", "pi")
    expression = expression.replace("phi", "pi")
    expression = expression.replace("bằng", "=")
    expression = expression.replace("triệu", "000000")
    expression = expression.replace("₫", "")
    expression = expression.replace("và", "&")
    expression = expression.replace("A", "a")
    expression = expression.replace("B", "b")
    expression = expression.replace("C", "c")
    expression = expression.replace("Xin", "sin(")
    expression = expression.replace("sin", "sin(")
    expression = expression.replace("*in", "sin(")
    expression = expression.replace("cos", "cos(")
    expression = expression.replace("code", "cos(")
    print(expression)


def equationFunction(e):
    result = solve(e)
    print("Answer: ", result)
    return result


def equation2Function(e):
    eq1, eq2 = e.split("&")
    sol = solve((eq1, eq2))
    return sol


def equation3Function(e):
    eq1, eq2, eq3 = e.split("&")
    sol = solve((eq1, eq2, eq3))
    return sol


def my_equation(a, equationA):
    return eval(equationA)


def draw():
    global expression
    expression = equation.get()
    print(expression)
    GraphOfFunctions(expression)
    expression = ""


def floatToFraction():
    global expression
    expression = str(equation.get())
    f = Fraction(str(expression))
    equation.set(f)


def GraphOfFunctions(e):
    e.strip()
    e.rstrip()
    e.lstrip()
    e = e.replace("^", "**")
    e1, e2 = e.split('=')
    a = np.arange(-10, 10, 0.01)
    b = my_equation(a, e2)
    plt.figure("Graph")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.plot(a, b, 'red')
    plt.show()


def press(num):
    global expression
    expression = str(expression) + str(num)
    equation.set(expression)


def equalpress():
    global expression
    print(expression)
    if expression == "":
        expression = str(equation.get())
        parseExpression()
    if "vẽ" in expression:
        GraphOfFunctions(expression)
        expression = ""
    elif "a" in expression and "b" in expression and "c" in expression:
        total = equation3Function(expression)
        equation.set(total)
        expression = ""
    elif "a" in expression and "b" in expression:
        total = equation2Function(expression)
        equation.set(total)
        expression = ""
    elif "a" in expression:
        total = equationFunction(expression)
        equation.set(total)
        expression = ""
    else:
        print(expression)
        total = eval(expression)
        print(f"{total:,}")
        expression = total
        equation.set(f"{total:,}")


def clear():
    global expression
    expression = ""
    equation.set("")


def delete():
    global expression
    expression = expression[:-1]
    equation.set(expression)


gui = Tk()
gui.configure(background="grey")
gui.title("Voice Calculator")
gui.geometry("505x510+1200+200")
myFont = font.Font(size=20)
equation = StringVar()
expression_field = Entry(gui, textvariable=equation, font=myFont, fg='black', bg='grey', )
expression_field.grid(columnspan=4, ipadx=100, ipady=10)
equation.set('0')
button1 = Button(gui, text=' 1 ', fg='grey', bg='black',
                 command=lambda: press(1), height=1, width=7, font=myFont)
button1.grid(row=3, column=0)

button2 = Button(gui, text=' 2 ', fg='grey', bg='black',
                 command=lambda: press(2), height=1, width=7, font=myFont)
button2.grid(row=3, column=1)

button3 = Button(gui, text=' 3 ', fg='grey', bg='black',
                 command=lambda: press(3), height=1, width=7, font=myFont)
button3.grid(row=3, column=2)

button4 = Button(gui, text=' 4 ', fg='grey', bg='black',
                 command=lambda: press(4), height=1, width=7, font=myFont)
button4.grid(row=4, column=0)

button5 = Button(gui, text=' 5 ', fg='grey', bg='black',
                 command=lambda: press(5), height=1, width=7, font=myFont)
button5.grid(row=4, column=1)

button6 = Button(gui, text=' 6 ', fg='grey', bg='black',
                 command=lambda: press(6), height=1, width=7, font=myFont)
button6.grid(row=4, column=2)

button7 = Button(gui, text=' 7 ', fg='grey', bg='black',
                 command=lambda: press(7), height=1, width=7, font=myFont)
button7.grid(row=5, column=0)

button8 = Button(gui, text=' 8 ', fg='grey', bg='black',
                 command=lambda: press(8), height=1, width=7, font=myFont)
button8.grid(row=5, column=1)

button9 = Button(gui, text=' 9 ', fg='grey', bg='black',
                 command=lambda: press(9), height=1, width=7, font=myFont)
button9.grid(row=5, column=2)

button0 = Button(gui, text=' 0 ', fg='grey', bg='black',
                 command=lambda: press(0), height=1, width=7, font=myFont)
button0.grid(row=6, column=0)

plus = Button(gui, text=' + ', fg='grey', bg='black',
              command=lambda: press("+"), height=1, width=7, font=myFont)
plus.grid(row=3, column=3)

minus = Button(gui, text=' - ', fg='grey', bg='black',
               command=lambda: press("-"), height=1, width=7, font=myFont)
minus.grid(row=4, column=3)

multiply = Button(gui, text=' * ', fg='grey', bg='black',
                  command=lambda: press("*"), height=1, width=7, font=myFont)
multiply.grid(row=5, column=3)

divide = Button(gui, text=' / ', fg='grey', bg='black',
                command=lambda: press("/"), height=1, width=7, font=myFont)
divide.grid(row=6, column=3)

equal = Button(gui, text=' = ', fg='grey', bg='black',
               command=equalpress, height=1, width=7, font=myFont)
equal.grid(row=6, column=2)

clear = Button(gui, text='Clr', fg='blue', bg='black',
               command=clear, height=1, width=7, font=myFont)
clear.grid(row=2, column=3)

delete = Button(gui, text='Del', fg='green', bg='black',
                command=delete, height=1, width=7, font=myFont)
delete.grid(row=2, column=2)

Decimal = Button(gui, text='.', fg='grey', bg='black',
                 command=lambda: press('.'), height=1, width=7, font=myFont)
Decimal.grid(row=6, column=1)

Record = Button(gui, text='Re', fg='red', bg='black',
                command=record, height=1, width=7, font=myFont)
Record.grid(row=2, column=0)

buttonDraw = Button(gui, text=' Draw ', fg='yellow', bg='black',
                    command=draw, height=1, width=7, font=myFont)
buttonDraw.grid(row=2, column=1)

buttonX = Button(gui, text=' ^ ', fg='grey', bg='black',
                 command=lambda: press("**"), height=1, width=7, font=myFont)
buttonX.grid(row=7, column=0)

buttonY = Button(gui, text=' √ ', fg='grey', bg='black',
                 command=lambda: press("**(1/2)"), height=1, width=7, font=myFont)
buttonY.grid(row=7, column=1)

buttonZ = Button(gui, text=' ( ', fg='grey', bg='black',
                 command=lambda: press("("), height=1, width=7, font=myFont)
buttonZ.grid(row=7, column=2)

buttonClose = Button(gui, text=' ) ', fg='grey', bg='black',
                     command=lambda: press(")"), height=1, width=7, font=myFont)
buttonClose.grid(row=7, column=3)

buttonA = Button(gui, text=' a ', fg='grey', bg='black',
                 command=lambda: press("a"), height=1, width=7, font=myFont)
buttonA.grid(row=8, column=0)

buttonB = Button(gui, text=' b ', fg='grey', bg='black',
                 command=lambda: press("b"), height=1, width=7, font=myFont)
buttonB.grid(row=8, column=1)

buttonC = Button(gui, text=' c ', fg='grey', bg='black',
                 command=lambda: press("c"), height=1, width=7, font=myFont)
buttonC.grid(row=8, column=2)

buttonSeperate = Button(gui, text=' & ', fg='grey', bg='black',
                        command=lambda: press("&"), height=1, width=7, font=myFont)
buttonSeperate.grid(row=8, column=3)

buttonSin = Button(gui, text=' sin ', fg='grey', bg='black',
                   command=lambda: press("sin"), height=1, width=7, font=myFont)
buttonSin.grid(row=9, column=0)

buttonCos = Button(gui, text=' cos ', fg='grey', bg='black',
                   command=lambda: press("cos"), height=1, width=7, font=myFont)
buttonCos.grid(row=9, column=1)

buttonFraction = Button(gui, text=' <=> ', fg='grey', bg='black',
                        command=floatToFraction, height=1, width=7, font=myFont)
buttonFraction.grid(row=9, column=2)

buttonLog = Button(gui, text=' log ', fg='grey', bg='black',
                   command=lambda: press("log"), height=1, width=7, font=myFont)
buttonLog.grid(row=9, column=3)

if __name__ == "__main__":
    try:
        gui.mainloop()
    except:
        pass
