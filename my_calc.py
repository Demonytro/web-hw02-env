from tkinter import *
from tkinter import messagebox
import tkinter


def main():
    my_calc = tkinter.Tk()

    my_calc.geometry("225x230")
    my_calc.title("Calculator")
    my_calc.maxsize(225, 230)
    my_calc.minsize(225, 230)

    entry = Entry(my_calc, width=16, borderwidth=3, relief=RIDGE)
    entry.grid(pady=10, row=0, sticky="w", padx=15)

    def delete():
        i = entry.get()
        entry.delete(first=len(i) - 1, last="end")

    def final_result():
        if entry.get() == "":
            pass
        elif entry.get()[0] == "0":
            entry.delete(0, "end")
        else:
            res = entry.get()
            try:
                res = eval(res)
            except ZeroDivisionError:
                messagebox.showerror("Error", "You can't divide by 0")
            else:
                cal_clear()
                entry.insert("end", res)

    def cal_clear():
        entry.delete(0, "end")

    char_clean = Button(my_calc, text="C", width=2, command=cal_clear, bg="blue", fg="white", relief=RIDGE,
                        justify="center")
    char_result = Button(my_calc, text="=", width=10, command=final_result, bg="blue", fg="white", borderwidth=3,
                         relief=RIDGE)

    char_nine = Button(my_calc, text="9", width=2, command=lambda: entry.insert("end", "9"), borderwidth=3,
                       relief=RIDGE)
    char_eight = Button(my_calc, text="8", width=2, command=lambda: entry.insert("end", "8"), borderwidth=3,
                        relief=RIDGE)
    char_seven = Button(my_calc, text="7", width=2, command=lambda: entry.insert("end", "7"), borderwidth=3,
                        relief=RIDGE)
    char_six = Button(my_calc, text="6", width=2, command=lambda: entry.insert("end", "6"), borderwidth=3, relief=RIDGE)
    char_five = Button(my_calc, text="5", width=2, command=lambda: entry.insert("end", "5"), borderwidth=3,
                       relief=RIDGE)
    char_four = Button(my_calc, text="4", width=2, command=lambda: entry.insert("end", "4"), borderwidth=3,
                       relief=RIDGE)
    char_three = Button(my_calc, text="3", width=2, command=lambda: entry.insert("end", "3"), borderwidth=3,
                        relief=RIDGE)
    char_two = Button(my_calc, text="2", width=2, command=lambda: entry.insert("end", "2"), borderwidth=3, relief=RIDGE)
    char_one = Button(my_calc, text="1", width=2, command=lambda: entry.insert("end", "1"), borderwidth=3, relief=RIDGE)
    char_zero = Button(my_calc, text="0", width=2, command=lambda: entry.insert("end", "0"), borderwidth=3,
                       relief=RIDGE)
    char_double_zero = Button(my_calc, text="00", width=2, command=lambda: entry.insert("end", "00"), borderwidth=3,
                              relief=RIDGE)

    char_plus = Button(my_calc, text="+", width=2, command=lambda: entry.insert("end", "+"), borderwidth=3,
                       relief=RIDGE)
    char_minus = Button(my_calc, text="-", width=2, command=lambda: entry.insert("end", "-"), borderwidth=3,
                        relief=RIDGE)
    char_multiply = Button(my_calc, text="*", width=2, command=lambda: entry.insert("end", "*"), borderwidth=3,
                           relief=RIDGE)
    char_divide = Button(my_calc, text="/", width=2, command=lambda: entry.insert("end", "/"), borderwidth=3,
                         relief=RIDGE)

    char_dot = Button(my_calc, text=".", width=2, command=lambda: entry.insert("end", "."), borderwidth=3, relief=RIDGE)
    char_modulus = Button(my_calc, text="%", width=2, command=lambda: entry.insert("end", "%"), borderwidth=3,
                          relief=RIDGE)
    char_delete = Button(my_calc, text="del", width=2, command=delete, borderwidth=3, relief=RIDGE)

    char_clean.grid(row=0, sticky="w", padx=125)
    char_result.grid(row=5, sticky="w", padx=15, pady=5)

    char_nine.grid(row=1, sticky="w", padx=75)
    char_eight.grid(row=1, sticky="w", padx=45)
    char_seven.grid(row=1, sticky="w", padx=15)
    char_six.grid(row=2, sticky="w", padx=75, pady=5)
    char_five.grid(row=2, sticky="w", padx=45, pady=5)
    char_four.grid(row=2, sticky="w", padx=15, pady=5)
    char_three.grid(row=3, sticky="w", padx=75, pady=5)
    char_two.grid(row=3, sticky="w", padx=45, pady=5)
    char_one.grid(row=3, sticky="w", padx=15, pady=5)
    char_zero.grid(row=4, sticky="w", padx=45, pady=5)
    char_double_zero.grid(row=4, sticky="w", padx=15, pady=5)

    char_plus.grid(row=1, sticky="e", padx=125)
    char_minus.grid(row=2, sticky="e", padx=125, pady=5)
    char_multiply.grid(row=3, sticky="e", padx=125, pady=5)
    char_divide.grid(row=4, sticky="e", padx=125, pady=5)
    char_dot.grid(row=4, sticky="w", padx=75, pady=5)
    char_modulus.grid(row=5, sticky="e", padx=125, pady=5)
    char_delete.grid(row=5, sticky="w", padx=80, pady=5)

    my_calc.mainloop()


if __name__ == '__main__':
    main()
