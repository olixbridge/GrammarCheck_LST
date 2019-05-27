import tkinter as tk
from grammarbot import GrammarBotClient

root = tk.Tk()
root.title("LivingSky Tech Grammar Check")
root.geometry("800x600+100+50")

text = tk.Text(root, width = 40, height = 30)
text.place(x=50, y=50)

def retrieve_input():
    input = text.get("1.0", "end-1c")

def output():
    client = GrammarBotClient()
    client = GrammarBotClient(api_key='AF5B9M2X') # GrammarBotClient(api_key=my_api_key_here)
    res = client.check(text.get("1.0", "end-1c")) # GrammarBotApiResponse(matches=[GrammarBotMatch(offset=2, length=4, rule={'CANT'}, category={'TYPOS'}), GrammarBotMatch(offset=26, length=5, rule={'CONFUSION_RULE'}, category={'TYPOS'})])
    res.detected_language # "en-US"
    res.result_is_incomplete # False
    res.matches # [GrammarBotMatch(offset=2, length=4, rule={'CANT'}, category={'TYPOS'}), GrammarBotMatch(offset=26, length=5, rule={'CONFUSION_RULE'}, category={'TYPOS'})]
    match0 = res.matches[0] # GrammarBotMatch(offset=2, length=4, rule={'CANT'}, category={'TYPOS'})
    match0.replacement_offset # 2
    match0.replacement_length # 4
    match0.replacements # ["can't", 'cannot']
    match0.corrections # 
    res.raw_json
    text2 = tk.Text(root, width = 40, height = 30)
    text2.place(x=500, y=50)
    text2.insert(tk.END, match0.corrections[0])
  
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

myButton1 = tk.Button(text='enter', command=combine_funcs(output,lambda: retrieve_input()))
myButton1.place(x=400, y=300)


root.mainloop()





# a = StringVar()
# text = Text(textvariable= a).pack()
# text = Text(myGui).pack()
# myButton1 = Button(text='enter', fg='black', bg='green', command=print, font=10).pack()

# Look into version control: Git