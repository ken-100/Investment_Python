from flask import Flask, request, render_template_string, send_file, redirect, url_for, make_response
import pandas as pd
import matplotlib.pyplot as plt
from xbbg import blp
import workdays
import datetime
import math
import io
import base64

app = Flask(__name__)

############################################################
# 1. データ準備 (Streamlit 版と同じロジック)
############################################################
LS = ["ES","NQ","RTY","VG","TP","JGS","NZ","IFB","FFD","XU","TWT"]
T = [i + "1 Index" for i in LS]

# デフォルト: 直近5年分 (約260日×5)
d_from = workdays.workday(datetime.datetime.today(), days=-260*5).strftime("%Y%m%d")
d_to   = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")

# Bloomberg からデータ取得 (xbbgの blp.bdh を使用)
df = blp.bdh(T, ["px_last","px_volume"], d_from, d_to, Calendar="5D", Fill="P").reset_index()

# MultiIndexから整形
df = df[[df.columns[0][0]] + T]  # 1列目=Date, 2列目以降=銘柄
df.columns = ["Date"] + [l + x for l in LS for x in ["_last","_volume"]]
df["Date"] = pd.to_datetime(df["Date"])

# 日付の最小・最大 (フォームのデフォルトに使う)
MIN_DATE = df["Date"].min().date()
MAX_DATE = df["Date"].max().date()

############################################################
# 2. HTMLテンプレート (簡易的にコード内へ埋め込み)
############################################################
html_template = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Flask App - Time-Series Data</title>
</head>
<body>
    <h2>Time-Series Data for Futures (Flask版)</h2>
    <form method="POST" action="/">
        <label>Choose the Future:</label>
        <select name="selected_symbol">
            {% for sym in LS %}
            <option value="{{ sym }}" {% if sym == selected_symbol %}selected{% endif %}>{{ sym }}</option>
            {% endfor %}
        </select>
        <br><br>

        <label>Start Date:</label>
        <input type="date" name="start_date" value="{{ start_date }}">
        <label>End Date:</label>
        <input type="date" name="end_date" value="{{ end_date }}">
        <br><br>

        <label>Select the data to display:</label>
        <input type="radio" name="selected_price_option" value="Last Price" 
            {% if selected_price_option == 'Last Price' %} checked {% endif %}>
            Last Price
        <input type="radio" name="selected_price_option" value="累積リターン"
            {% if selected_price_option == '累積リターン' %} checked {% endif %}>
            累積リターン
        <br><br>

        <button type="submit">Submit</button>
    </form>

    {% if warning %}
    <p style="color:red;">{{ warning }}</p>
    {% endif %}

    {% if plot_img %}
    <hr>
    <h3>Chart</h3>
    <img src="data:image/png;base64,{{ plot_img }}" alt="plot">
    {% endif %}

    {% if summary_html %}
    <hr>
    <h3>Summary</h3>
    {{ summary_html|safe }}
    {% endif %}

    {% if can_download %}
    <hr>
    <form method="GET" action="/download_csv">
        <input type="hidden" name="selected_symbol" value="{{ selected_symbol }}">
        <input type="hidden" name="price_option" value="{{ selected_price_option }}">
        <input type="hidden" name="start_date" value="{{ start_date }}">
        <input type="hidden" name="end_date" value="{{ end_date }}">
        <button type="submit">Download CSV</button>
    </form>
    {% endif %}
</body>
</html>
"""

############################################################
# 3. Flaskルート
############################################################
@app.route("/", methods=["GET", "POST"])
def index():
    # デフォルト値
    selected_symbol = LS[0]
    selected_price_option = "Last Price"
    start_date = str(MIN_DATE)
    end_date   = str(MAX_DATE)

    warning = None
    plot_img = None
    summary_html = None
    can_download = False

    if request.method == "POST":
        # フォームから受け取る
        selected_symbol = request.form.get("selected_symbol", LS[0])
        selected_price_option = request.form.get("selected_price_option", "Last Price")
        start_date = request.form.get("start_date", str(MIN_DATE))
        end_date   = request.form.get("end_date", str(MAX_DATE))

        # 日付をdatetimeに変換 (エラー対策は省略)
        start_date_dt = pd.to_datetime(start_date)
        end_date_dt   = pd.to_datetime(end_date)

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
            warning = "指定期間内にデータがありません。日付を変更してください。"
        else:
            # グラフ作成
            if selected_price_option == "Last Price":
                y_data = df_filtered[last_col]
                y_label = "Last Price"
            else:
                # 累積リターン計算
                df_filtered["CumulativeReturn"] = (1 + df_filtered[last_col].pct_change().fillna(0)).cumprod() - 1
                y_data = df_filtered["CumulativeReturn"]
                y_label = "Cumulative Return ( (1 + r).cumprod() - 1 )"

            # Matplotlib で描画
            fig, ax = plt.subplots(figsize=(8, 4))
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

            # 画像をメモリ上に書き込んで base64 エンコード
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            plot_img = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig)

            # サマリー計算
            # (1) 期間
            period_days = (end_date_dt - start_date_dt).days
            period_years = period_days / 365.0 if period_days > 0 else 0.0

            # (2) トータルリターン
            if len(df_filtered) >= 2:
                total_return = (df_filtered[last_col].iloc[-1] / df_filtered[last_col].iloc[0]) - 1
            else:
                total_return = 0.0

            # (3) トータルリターンの年率
            if period_years > 0 and len(df_filtered) >= 2:
                annualized_return = (1 + total_return) ** (1 / period_years) - 1
            else:
                annualized_return = 0.0

            # (4) 年率標準偏差
            daily_return = df_filtered[last_col].pct_change().dropna()
            annualized_std = daily_return.std() * math.sqrt(260)

            summary_data = {
                "銘柄": [selected_symbol],
                "期間": [f"{start_date} ~ {end_date}"],
                "Year": [f"{period_years:.2f}"],
                "TotalRet": [f"{total_return:.2%}"],
                "YearlyRet": [f"{annualized_return:.2%}"],
                "SD(Yearly)": [f"{annualized_std:.2%}"],
            }
            summary_df = pd.DataFrame(summary_data)
            summary_html = summary_df.to_html(index=False)

            # ダウンロードを許可
            can_download = True

    return render_template_string(
        html_template,
        LS=LS,
        selected_symbol=selected_symbol,
        selected_price_option=selected_price_option,
        start_date=start_date,
        end_date=end_date,
        warning=warning,
        plot_img=plot_img,
        summary_html=summary_html,
        can_download=can_download
    )

############################################################
# 4. CSV ダウンロード用エンドポイント
############################################################
@app.route("/download_csv", methods=["GET"])
def download_csv():
    selected_symbol = request.args.get("selected_symbol", LS[0])
    price_option = request.args.get("price_option", "Last Price")
    start_date_str = request.args.get("start_date", str(MIN_DATE))
    end_date_str   = request.args.get("end_date", str(MAX_DATE))

    start_date_dt = pd.to_datetime(start_date_str)
    end_date_dt   = pd.to_datetime(end_date_str)

    last_col = selected_symbol + "_last"
    volume_col = selected_symbol + "_volume"

    df_selected = df[["Date", last_col, volume_col]].copy()
    df_selected.sort_values("Date", inplace=True)
    df_filtered = df_selected[
        (df_selected["Date"] >= start_date_dt) &
        (df_selected["Date"] <= end_date_dt)
    ]

    # 累積リターンがある場合は計算して列を追加
    if price_option == "累積リターン":
        df_filtered["CumulativeReturn"] = (1 + df_filtered[last_col].pct_change().fillna(0)).cumprod() - 1

    # CSV データをバイナリに変換
    csv_data = df_filtered.to_csv(index=False).encode("utf-8-sig")

    # Flask で CSV を返す
    response = make_response(csv_data)
    filename = f"{selected_symbol}_{price_option}_{start_date_str}_{end_date_str}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv; charset=utf-8-sig"
    return response

############################################################
# 5. メイン実行
############################################################
if __name__ == "__main__":
    app.run(debug=True)
