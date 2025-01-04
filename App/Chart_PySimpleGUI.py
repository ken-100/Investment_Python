import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import base64
from xbbg import blp  # 実際には Bloomberg Terminal 接続が必要
import workdays
import datetime
import math
import io
import os

############################################################
# 0. 初期データ (Flask版からほぼ流用)
############################################################
LS = ["ES","NQ","RTY","VG","TP","JGS","NZ","IFB","FFD","XU","TWT"]
T = [i + "1 Index" for i in LS]

# デフォルト: 直近5年分 (約260日×5)
d_from = workdays.workday(datetime.datetime.today(), days=-260*5).strftime("%Y%m%d")
d_to   = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

# ここで xbbg の blp.bdh() を用いてデータを取得
#  ※Bloomberg 環境がない場合は、適当なサンプル CSV 等を読み込む形に置き換えてください
df = blp.bdh(
    tickers=T,
    flds=["px_last","px_volume"],
    start_date=d_from,
    end_date=d_to,
    Calendar="5D",  # 営業日
    Fill="P",
).reset_index()

# MultiIndex から整形
df = df[[df.columns[0][0]] + T]  # 1列目=Date, 2列目以降=銘柄
df.columns = ["Date"] + [l + x for l in LS for x in ["_last","_volume"]]
df["Date"] = pd.to_datetime(df["Date"])
MIN_DATE = df["Date"].min().date()
MAX_DATE = df["Date"].max().date()

############################################################
# 1. GUIレイアウト
############################################################
layout = [
    [sg.Text("Choose the Future:"),
     sg.Combo(LS, default_value=LS[0], key="-SYMBOL-")],
    
    [sg.Text("Start Date:"),
     sg.Input(str(MIN_DATE), key="-START-", size=(10,1)),
     sg.Text("End Date:"),
     sg.Input(str(MAX_DATE), key="-END-", size=(10,1))],

    [sg.Text("Select data to display:")],
    [sg.Radio("Last Price", group_id="RADIO1", default=True, key="-LAST-"),
     sg.Radio("累積リターン", group_id="RADIO1", default=False, key="-CUMRET-")],

    [sg.Button("実行", key="-EXECUTE-"), sg.Button("CSVダウンロード", key="-DOWNLOAD-")],
    [sg.Text("", key="-WARNING-", size=(50,1), text_color="red")],
    
    # グラフ表示領域
    [sg.Image(key="-IMG-")],
    
    # サマリー表示領域
    [sg.Text("Summary:", visible=False, key="-SUMMARY_TITLE-")],
    # 複数行表示に対応させるため sg.Multiline を使用
    [sg.Multiline(
        "", 
        key="-SUMMARY-", 
        visible=False, 
        size=(70, 5), 
        background_color="white", 
        autoscroll=True
    )],
]

# ウィンドウをリサイズ可能に設定
window = sg.Window(
    "Time-Series Data for Futures (Native版)", 
    layout, 
    size=(700, 600),
    resizable=True
)

############################################################
# 2. イベントループ
############################################################
def plot_to_base64(fig):
    """Matplotlib Figure を base64 エンコード文字列として返す"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.read()
    return base64.b64encode(img_bytes)

# CSV 出力パスを指定（適当なファイル名）
csv_output_path = os.path.join(os.path.expanduser("~"), "futures_data.csv")

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-EXECUTE-":
        # 入力を取得
        selected_symbol = values["-SYMBOL-"]
        start_date_str = values["-START-"]
        end_date_str   = values["-END-"]
        use_last = values["-LAST-"]         # True/False
        use_cum  = values["-CUMRET-"]       # True/False

        # 警告メッセージ領域は一旦クリア
        window["-WARNING-"].update("")

        # 文字列をdatetimeに変換
        try:
            start_date_dt = pd.to_datetime(start_date_str)
            end_date_dt   = pd.to_datetime(end_date_str)
        except Exception as e:
            window["-WARNING-"].update("日付の形式が不正です。YYYY-MM-DD 形式などで入力してください。")
            continue

        # データ絞り込み
        last_col = selected_symbol + "_last"
        volume_col = selected_symbol + "_volume"

        df_selected = df[["Date", last_col, volume_col]].copy()
        df_selected.sort_values("Date", inplace=True)

        df_filtered = df_selected[
            (df_selected["Date"] >= start_date_dt) &
            (df_selected["Date"] <= end_date_dt)
        ]

        if df_filtered.empty:
            window["-WARNING-"].update("指定期間内にデータがありません。日付を変更してください。")
            continue

        # グラフ作成
        if use_last:
            y_data = df_filtered[last_col]
            y_label = "Last Price"
        else:
            # 累積リターン計算
            df_filtered["CumulativeReturn"] = (
                (1 + df_filtered[last_col].pct_change().fillna(0)).cumprod() - 1
            )
            y_data = df_filtered["CumulativeReturn"]
            y_label = "Cumulative Return ( (1 + r).cumprod() - 1 )"

        fig, ax = plt.subplots(figsize=(6,3), dpi=100)
        ax.plot(df_filtered["Date"], y_data, label=f"{selected_symbol} {y_label}", color="blue")
        ax.set_xlabel("Date")
        ax.set_ylabel(y_label, color="blue")
        ax.tick_params(axis='y', labelcolor="blue")

        ax2 = ax.twinx()
        ax2.bar(df_filtered["Date"], df_filtered[volume_col], alpha=0.3, color="gray", label="Volume")
        ax2.set_ylabel("Volume", color="gray")
        ax2.tick_params(axis='y', labelcolor="gray")

        lines_1, labels_1 = ax.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax2.legend(
            lines_1 + lines_2, labels_1 + labels_2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=2,
        )

        fig.tight_layout()

        # figure -> base64 -> PySimpleGUI で表示
        png_b64 = plot_to_base64(fig)
        plt.close(fig)
        window["-IMG-"].update(data=png_b64)

        # サマリー計算
        period_days = (end_date_dt - start_date_dt).days
        period_years = period_days / 365.0 if period_days > 0 else 0.0

        if len(df_filtered) >= 2:
            total_return = (df_filtered[last_col].iloc[-1] / df_filtered[last_col].iloc[0]) - 1
        else:
            total_return = 0.0

        if period_years > 0 and len(df_filtered) >= 2:
            annualized_return = (1 + total_return) ** (1 / period_years) - 1
        else:
            annualized_return = 0.0

        daily_return = df_filtered[last_col].pct_change().dropna()
        annualized_std = daily_return.std() * math.sqrt(260)

        summary_data = {
            "銘柄":       [selected_symbol],
            "期間":       [f"{start_date_str} ~ {end_date_str}"],
            "Year":       [f"{period_years:.2f}"],
            "TotalRet":   [f"{total_return:.2%}"],
            "YearlyRet":  [f"{annualized_return:.2%}"],
            "SD(Yearly)": [f"{annualized_std:.2%}"],
        }
        summary_df = pd.DataFrame(summary_data)

        # CSV っぽい文字列を作る
        summary_str = summary_df.to_string(index=False)
        
        # サマリー表示
        window["-SUMMARY_TITLE-"].update(visible=True)
        window["-SUMMARY-"].update(summary_str, visible=True)

        # 実行結果を一時的に保持（CSVダウンロード時に使う）
        df_filtered.to_pickle("temp_filtered.pkl")

    if event == "-DOWNLOAD-":
        # 直前の df_filtered を読み込み (実行していない/空の場合は空)
        if not os.path.exists("temp_filtered.pkl"):
            window["-WARNING-"].update("まだデータの絞り込みが行われていません。先に[実行]してください。")
            continue
        
        df_filtered = pd.read_pickle("temp_filtered.pkl")

        # CSV 保存
        df_filtered.to_csv(csv_output_path, index=False, encoding="utf-8-sig")
        sg.popup(f"CSV を保存しました: {csv_output_path}")

window.close()
