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


    print("Top：" + univ)
    display(arrange(df,False))
    
    print("Worst:" + univ)
    display(arrange(df,True))
    
    fig = build_heatmap(univ, df.head(100),name)
    fig.show()

    return df

def arrange(df,ascending=False):
    df1 = df.sort_values('Ret%', ascending=ascending).drop('ID1', axis=1).reset_index(drop=True).head(5).copy()
    df1['Weight%'] *= 100
    df1['Ret%'] *= 100
    df1['Weight%'] = df1['Weight%'].apply(lambda x: f'{x:.1f}')
    df1['Ret%'] = df1['Ret%'].apply(lambda x: f'{x:.2f}')
    return df1



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

    # print(df[df['Kanji'].isna()])
    
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

    universe = [request[0] for request in requests]
    
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
    ("SPY US Equity", "Fund",  "-2D",  "-1D", "ID"),
    ("1348 JP Equity", "Fund", "-1D",  "today", "Kanji"),
    ("2828 HK Equity", "Fund", "-1D",  "today", "Short"),
]


List = ListCreation(requests)

for i in range(len(requests)):
    globals()[f"df{i}"] = get_data(requests[i][0], requests[i][1], requests[i][2],requests[i][3], requests[i][4])
    
