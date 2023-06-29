from cryptography.fernet import Fernet
import requests
import tkinter as Tk
import tkinter.ttk as ttk
import json
import math

def get_addr():
    addr = address_input.get("1.0", "end-1c")
    # turn addresses into 
    try: 
        t = requests.get("https://blockchain.info/ticker")
        price = t.json()
        usd = price["USD"]["last"]
    except KeyError:
        print("Error getting bitcoin price")
    try:
        a = 'https://blockchain.info/multiaddr?active='+ addr + "&n=0"
        r = requests.get(a)
        data = r.json()
    except KeyError:
        print("error getting wallets")

    address_input.delete('1.0', 'end-1c')
    id = 0
    try:
        for i in data["addresses"]:
            balance = data["addresses"][id]["final_balance"] / 1e8
            output = math.floor(balance * usd)
            usdp = "{:,}".format(output)
            tx = data["addresses"][id]["n_tx"]
            s = "ADDRESS: " + str(data["addresses"][id]["address"]) + " USD: " + "$" + str(usdp) + " BTC: " + str(balance) + " transaction number: " + str(tx)
            address_input.configure(state='normal') 
            address_input.insert(1.0, s + '\n')
            id += 1   
    except KeyError:
        print("Error showing wallets")

root = Tk.Tk()
style= ttk.Style(root)
style.theme_use('clam')
root.configure(bg="#000000")
root.geometry("1000x400")
root.title("BTC Balance Checker")

frame = ttk.Frame(root)
frame.pack(fill=Tk.BOTH)
address_input = Tk.Text(root, font=('Fixedsys', 14), width=100, wrap='none',bg='#000000', fg='#39ff14')
address_input.pack(side=Tk.LEFT)

scrl = ttk.Scrollbar(root, orient='vertical', command=address_input.yview)
scrl.pack(side=Tk.RIGHT, fill=Tk.Y)
style.configure("Vertical.TScrollbar", gripcount=0,
                background="#000000", darkcolor="#39ff14", lightcolor="#39ff14",
                troughcolor="#000000", bordercolor="#39ff14", arrowcolor="#39ff14")

scrl2 = ttk.Scrollbar(frame, orient='horizontal', command=address_input.xview)
scrl2.pack(side=Tk.BOTTOM, fill=Tk.X)
style.configure("Horizontal.TScrollbar", gripcount=0,
                background="#000000", darkcolor="#39ff14", lightcolor="#39ff14",
                troughcolor="#000000", bordercolor="#39ff14", arrowcolor="#39ff14")

style.configure('TButton', font=('Fixedsys', 14), background='#000000', foreground='#39ff14', bordercolor="#39ff14")
style.map('TButton', background=[('active', '#232323')])
scrl.config(command=address_input.yview)
addrButton = ttk.Button(root, text="Check Balances", command=get_addr)
addrButton.pack(side=Tk.BOTTOM)
address_input['yscrollcommand'] = scrl.set
address_input['xscrollcommand'] = scrl2.set
root.mainloop()