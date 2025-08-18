# Cell 1
import re
import ipydatagrid as ipd
import ipywidgets as widgets
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bql
import bqplot as bqp

bq = bql.Service()


# Cell 2
def get_data(univ, univ_type, d_from, d_to, name):
    
    d = {
        'Index': bq.univ.members(univ),
        'Fund': bq.univ.holdings(univ),
        'Portfolio': bq.univ.members(univ, type='port')
    }
    universe =  d[univ_type]

    
    dates = bq.func.range(d_from, d_to)
    
    data_items = {
        'Name': bq.data.name(),
        'Short': bq.data.short_name(),
        'Kanji': bq.data.name_kanji_short(),
        'Sector': bq.data.classification_name(),
        'Weight%': bq.data.id()["WEIGHTS"]/100,
        'Ret%': bq.data.total_return(calc_interval=dates),
        'Volume': bq.data.px_volume(dates=d_to),
        'Volume_avg': bq.data.volume_avg_12m(),
    }

    request = bql.Request(universe, data_items)
    response = bq.execute(request)

    df = pd.concat(
        [data_item.df()[data_item.name] for data_item in response], 
        axis=1
    )
    
    df = df.sort_values('Weight%', ascending=False)
    df = df.reset_index(drop=False)

    df.insert(1, 'ID1', df['ID'].str.split().str[1])
    df["ID"] = df["ID"].str.split().str[0]

    df["RelativeVolume"] = df["Volume"] / df["Volume_avg"]
    
    print("Top：" + univ)
    display(arrange(df,False))
    
    print("Worst:" + univ)
    display(arrange(df,True))

    print("HighVolume:" + univ)
    display(arrange1(df))
    
    fig = build_heatmap(univ, df.head(100),name)
    fig.show()

    return df


def arrange(df, ascending=False):
    df1 = df[["ID","Short","Kanji","Sector","Weight%","Ret%"]].copy()
    df1 = df1.sort_values('Ret%', ascending=ascending).reset_index(drop=True).head(5)
    
    C = df1.columns  # Get column names
    styled_df = df1.style\
        .bar(subset=[C[c] for c in range(len(C)) if C[c] in ['Weight%', 'Ret%']], 
             align='mid', 
             width=60, 
             color=["#ff8080", "#80ff80"])\
        .format({
            'Weight%': '{:.1%}',
            'Ret%': '{:.1%}'
        })\
        .set_properties(subset=['Weight%', 'Ret%'], **{'text-align': 'right'})  # 数値を右寄せ
    
    return styled_df

# To Be Corrected
def arrange1(df):
    df1 = df[["ID","Short","Kanji","Sector","RelativeVolume"]].copy()
    df1 = df1.sort_values("RelativeVolume", ascending=False).reset_index(drop=True).head(5)
    
    C = df1.columns  # Get column names
    styled_df = df1.style\
        .bar(subset=[C[c] for c in range(len(C)) if C[c] in ["RelativeVolume"]], 
             align='mid',
             width=60,  
             color=["#ff8080", "#80ff80"])\
        .format({
            "RelativeVolume": '{:.0%}'
        })\
        .set_properties(subset=["RelativeVolume"], **{'text-align': 'right'})  # 数値を右寄せ
    
    return styled_df
    
    
def create_range_colors(df, return_col='Ret%'):
    """
    Creates a tuple of negative and positive integers for color range.
    """
    max_val = max(df[return_col].abs())
    return (-max_val, max_val)

def centered_color_scale(range_colors):
    """
    Generates color scale with 0 as the center point.
    """
    min_val, max_val = range_colors
    zero_pos = (0 - min_val) / (max_val - min_val)
    lower_increment = zero_pos
    upper_increment = 1 - zero_pos
    
    colors = [
        (0, "#f63538"),
        (0 + lower_increment / 3, "#f63538"),
        (zero_pos - lower_increment / 30, "#544441"), 
        (zero_pos, "#414554"), 
        (zero_pos + upper_increment / 30, '#425441'),
        (1 - upper_increment / 3, "#30cc5a"),
        (1, "#30cc5a")
    ]
    return colors

def build_heatmap(univ, df,name):
    """
    Builds a treemap heatmap from DataFrame with ID, Sector, Weight%, Ret%.
    """

     
    tmp = df[df['Sector'].isna()]
    
    if len(tmp) > 0:
        print("Delete")
        display(tmp)
        df = df[~df['Sector'].isna()].reset_index(drop=False)
        
    # Ensure required columns exist
    required_cols = ['ID',"Short",'Kanji', 'Sector', 'Weight%', 'Ret%']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")
    
    # Create range colors based on returns
    range_colors = create_range_colors(df, 'Ret%')
    
    # Build the treemap with custom_data for proper text display
    fig = px.treemap(
        df,
        # path=['Sector', 'ID'],
        path=['Sector', name],
        values='Weight%',
        color='Ret%',
        color_continuous_scale=centered_color_scale(range_colors),
        range_color=range_colors,
        custom_data=['ID', 'Short','Ret%'],  # Add Ret% to custom_data
        height=600
    )
    
    # Update text template to use customdata
    fig.data[0].texttemplate = (
        "<b>%{label}</b><br>"
        "%{customdata[2]:.2%}"  # Use customdata[0] for Ret%
    )
    
    fig.data[0].textposition = 'middle center'
    
    # Update layout with dark theme similar to original
    fig.update_layout(
        margin=dict(l=10, r=30, t=35, b=20),
        paper_bgcolor="#212121",
        font=dict(color='white', size=12),
        title={
            # 'text': 'Sector Heatmap',
            'text': univ,
            'font': {'color': 'white', 'size': 20},
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    # Update traces
    fig.update_traces(
        marker=dict(cornerradius=5),
        insidetextfont=dict(color="white"),
        hovertemplate=(
            "%{customdata[0]}<br>"
            "%{customdata[1]}<br>"
            "Weight: %{value:.2%}<br>"
            "Return: %{customdata[2]:.2%}<br>"  
            "<extra></extra>"
        )
    )

    # Update colorbar
    fig.update_coloraxes(
        colorbar_tickformat='.0%',
        colorbar_title_text='Return %'
    )
    
    return fig


def ListCreation(requests):

    # universe = [request[0] for request in requests]
    universe = requests["Ticker"].tolist()
    
    data_items = {
        'Name': bq.data.name(),
        'Crncy': bq.data.crncy(),
        'ISO': bq.data.country_iso(),
    }
    
    response = bq.execute(bql.Request(universe, data_items))
    
    List = pd.concat(
        [data_item.df()[data_item.name] for data_item in response], 
        axis=1
    )
    
    List = List.reset_index(drop=False)
    display(List)
    
    return List

# Cell 3
requests = [
    ("SPY US Equity", "Fund", "-1D", "0D", "ID"),
    ("IWM US Equity", "Fund", "-1D", "0D", "ID"),
    ("1348 JP Equity", "Fund", "-1D", "0D", "Kanji"),
    ("1343 JP Equity", "Fund", "-1D", "0D", "Kanji"),
    ("2828 HK Equity", "Fund", "-1D", "0D", "Short"),
]

columns = ["Ticker", "Type", "from", "to", "Format"]

requests = pd.DataFrame(requests, columns=columns)
requests


# Cell 4
List = ListCreation(requests)

for i in range(len(requests)):

    d_from_orig = int(requests.loc[i,"from"].replace('D', ''))
    d_to_orig = int(requests.loc[i,"to"].replace('D', ''))
    
    d_from = ( d_from_orig  - 5) * 2
    d_from = str(d_from) + "D"
    
    data_items = bq.data.px_last(dates=bq.func.range(d_from, '0D'))
    
    request = bql.Request(requests.loc[i,"Ticker"], data_items)
    response = bq.execute(request)
    
    tmp = response[0].df()
    tmp = tmp.reset_index(drop=True)
    tmp = tmp.sort_values(by='DATE', ascending=False).reset_index(drop=True).dropna()
    
    d_to =  str(-tmp.index[d_to_orig] ) + "D"
    d_from =  str(-tmp.index[-d_from_orig] ) + "D"
    
    globals()[f"df{i}"] = get_data(requests.loc[i,"Ticker"], requests.loc[i,"Type"], d_from, d_to, requests.loc[i,"Format"])
    
    
