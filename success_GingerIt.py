import unittest
import tkinter as tk
from gingerit.gingerit import GingerIt

root = tk.Tk()
root.title("LivingSky Tech Grammar Check")
root.geometry("800x600+100+50")

text = tk.Text(root, width = 40, height = 30)
text.place(x=50, y=50)

def output():
    text2 = text.get("1.0", "end-1c")
    parser = GingerIt()
    output1 = parser.parse(text2)
    text3 = tk.Text(root, width = 40, height = 30)
    text3.place(x=500, y=50)
    text3.insert(tk.END, output1.get("result"))
  
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

myButton1 = tk.Button(text='enter', command=combine_funcs(output,lambda: retrieve_input()))
myButton1.place(x=400, y=300)


root.mainloop()

# Look into version control: Git