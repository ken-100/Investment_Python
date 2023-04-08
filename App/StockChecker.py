import tkinter as tk
import yfinance as yf
import pandas as pd

def get_stock_price():
    symbol = entry.get()
    stock_info = yf.Ticker(symbol)
    stock_history = stock_info.history(period="1d")
    price = stock_history['Close'][0]
    label.config(text=f"{symbol} の株価: {price}")

root = tk.Tk()
root.title("株価チェッカー")

frame = tk.Frame(root)
frame.pack()

label = tk.Label(frame, text="銘柄コードを入力してください")
label.pack()


entry = tk.Entry(frame)
entry.pack()

button = tk.Button(frame, text="株価を取得", command=get_stock_price)
button.pack()

root.mainloop()
