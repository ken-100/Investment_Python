import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from xbbg import blp
import pdblp
import workdays
import datetime
import math


LS = ["ES","NQ","RTY","VG","TP","JGS","NZ","IFB","FFD","XU","TWT"]
T = [i + "1 Index" for i in LS]

# Default
d_from = workdays.workday(datetime.datetime.today(), days=-260*5).strftime("%Y%m%d")
d_to   = workdays.workday(datetime.datetime.today(), days=-1).strftime("%Y%m%d")


df = blp.bdh(T, ["px_last","px_volume"], d_from, d_to, Calendar="5D", Fill="P").reset_index()
df = df[[df.columns[0][0]] + T]
df.columns = ["Date"] + [l + x for l in LS for x in ["_last","_volume"]]
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.subheader("Time-Series Data for Futures")

# Select
selected_symbol = st.selectbox("Choose the Future", LS)
min_date = df["Date"].min()
max_date = df["Date"].max()
start_date = st.date_input("Start", value=min_date, min_value=min_date, max_value=max_date)
end_date   = st.date_input("End", value=max_date, min_value=min_date, max_value=max_date)


price_options = ["Last Price", "累積リターン"]
selected_price_option = st.radio("Select the data to display.", price_options)


last_col = selected_symbol + "_last"
volume_col = selected_symbol + "_volume"

df_selected = df[["Date", last_col, volume_col]].copy()
df_selected.sort_values("Date", inplace=True)

df_filtered = df_selected[
    (df_selected["Date"] >= pd.to_datetime(start_date)) &
    (df_selected["Date"] <= pd.to_datetime(end_date))
]

if df_filtered.empty:
    st.warning("There is no data within the specified period, change the date.")
    st.stop()

if selected_price_option == "Last Price":
    y_data = df_filtered[last_col]
    y_label = "Last Price"
else:
    df_filtered["CumulativeReturn"] = (1 + df_filtered[last_col].pct_change().fillna(0)).cumprod() - 1
    y_data = df_filtered["CumulativeReturn"]
    y_label = "Cumulative Ret"

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df_filtered["Date"], y_data, label=f"{selected_symbol} {y_label}", color="blue")
ax.set_xlabel("Date")
ax.set_ylabel(y_label, color="blue")
ax.tick_params(axis='y', labelcolor="blue")

# Volume
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
st.pyplot(fig)

# Summary
start_date_dt = pd.to_datetime(start_date)
end_date_dt = pd.to_datetime(end_date)
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
    "銘柄": [selected_symbol],
    "期間": [f"{start_date} ~ {end_date}"],
    "Year": [f"{period_years:.2f}"],
    "TotalRet": [f"{total_return:.2%}"],
    "YearlyRet": [f"{annualized_return:.2%}"],
    "SD": [f"{annualized_std:.2%}"],
}

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df)

# Get CSV
df_download = df_filtered.copy()
if "CumulativeReturn" in df_download.columns:
    df_download = df_download[["Date", last_col, volume_col, "CumulativeReturn"]]
else:
    df_download = df_download[["Date", last_col, volume_col]]

csv_data = df_download.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name=f"{selected_symbol}_{selected_price_option}_{start_date}_{end_date}.csv",
    mime="text/csv"
)
