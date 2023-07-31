import requests, os
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Kalkulator walut')

try:

    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/A/")
    open("dane_walutowe.txt", "w").write(str(response.json()[0]))

    root.geometry("400x225")

    def internet(word): #currency, code, mid

        table = []

        for i in (response.json()[0]["rates"]):
            name = i[word]
            table.append(name)

        return table
    
    currency = []
    for i in range(len(internet("currency"))):
        currency.append(internet("currency")[i])

    mid = []
    for i in range(len(internet("mid"))):
        mid.append(internet("mid")[i])

except requests.ConnectionError:

    root.geometry("500x275") 

    f = open("dane_walutowe.txt", "r")
    dic = eval(f.read())

    def no_internet(word:str): #currency, code, mid

        table = []

        for i in (dic["rates"]):
            name = i[word]
            table.append(name)
        
        return table
    
    currency = []
    for i in range(len(no_internet("currency"))):
        currency.append(no_internet("currency")[i])

    mid = []
    for i in range(len(no_internet("mid"))):
        mid.append(no_internet("mid")[i])
    
    connection_label = Label(root, text = "Brak połączenia z internetem.\n Stan na: " + dic["effectiveDate"] + ".")
    connection_label.grid(row = 5, column = 1, padx = 10, pady = 10)

def calculate():

    global result

    try:

        for i in range(len(mid)):
            if source_currency.get() == currency[i]:
                source_currency_number = i

        for i in range(len(mid)):
            if goal_currency.get() == currency[i]:
                goal_currency_number = i

        if value.get().count(".") == 1:
            if value.get()[-3] != ".":
                raise ValueError

        if value.get()[0] == "-":
                raise ValueError
        
        amount = round(float(value.get()) * mid[source_currency_number] / mid[goal_currency_number], 2)  
        result = Label(root, text = str(amount), font = 12)
        result.grid(row = 3, column = 2, padx = 10, pady = 10)
    

    except ValueError:

        result = Label(root, text = "Źle wprowadzona kwota", font = 12)
        result.grid(row = 3, column = 2, padx = 10, pady = 10)

    count_button["state"] = DISABLED

def clear():
    result.destroy()
    count_button["state"] = NORMAL

source = Label(root, text="Waluta źródłowa")
source.grid(row = 0, column = 0, padx = 10, pady = 10)

source_currency = ttk.Combobox(root, values = currency)
source_currency.grid(row = 0, column = 2, padx = 10, pady = 10)                             

goal = Label(root, text = "Waluta docelowa")
goal.grid(row = 1, column = 0, padx = 10, pady = 10)

goal_currency = ttk.Combobox(root, values = currency)
goal_currency.grid(row = 1, column = 2, padx = 10, pady = 10)                                

money_in = Label(root, text = "Wpłata")
money_in.grid(row = 2, column = 0, padx = 10, pady = 10)

value = Entry(root)
value.grid(row = 2, column = 2, padx = 10, pady = 10)

money_out = Label(root, text = "Wypłata")
money_out.grid(row = 3, column = 0, padx = 10, pady = 10)

count_button = Button(
    root, 
    text = "OBLICZ",
    font = 12,
    command = calculate,
    bg = "blue", 
    fg = "white")
count_button.grid(row = 4, column = 1, padx = 10, pady = 10)

clear_button = Button(
    root, 
    text = "WYCZYŚĆ",
    font = 12,
    command = clear,
    bg = "green", 
    fg = "white")
clear_button.grid(row = 4, column = 0, padx = 10, pady = 10)

end_button = Button(
    root, 
    text = "KONIEC",
    font = 12, 
    command = quit, 
    bg = "red", 
    fg = "white")
end_button.grid(row = 4, column = 2, padx = 10, pady = 10)

root.mainloop()