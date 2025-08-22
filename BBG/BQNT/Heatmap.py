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
def get_data(univ, univ_type, d_from, d_to, name, sector):
    
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
        'Sub': bq.data.classification_name(
            classification_level='4'
        ),
        # 'Sub1': bq.data.industry_subgroup(),
        # 'Sub2': bq.data.gics_industry_name(),
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
    
    print("Top")
    display(arrange(df,["ID","Short","Kanji","Sector","Sub"],["Weight%","Ret%"],'{:.1%}',5,False))
    
    print("Worst")
    display(arrange(df,["ID","Short","Kanji","Sector","Sub"],["Weight%","Ret%"],'{:.1%}' ,5, True))

    print("HighVolume")
    display(arrange(df,["ID","Short","Kanji","Sector","Sub"],["RelativeVolume"],'{:.0%}' ,5, False))


    Sector = list(set(df[sector].tolist()))
    df["tmp"] = df["Weight%"] * df["Ret%"]
    
    df_Sector = pd.DataFrame({
        sector: Sector,
        'Weight%': 0, 
        'Ret%': 0    
    })
        
    for i,j in enumerate(Sector):
        df_Sector.loc[i,"Weight%"] = df.loc[df[sector]==j,"Weight%"].sum() 

        if df_Sector.loc[i,"Weight%"] ==0:
            df_Sector.loc[i,"Ret%"] = 0 
        else:
            df_Sector.loc[i,"Ret%"] = df.loc[df[sector]==j,"tmp"].sum() / df_Sector.loc[i,"Weight%"]

    df = df.drop('tmp', axis=1)
    
    df_Sector = df_Sector.sort_values("Ret%", ascending=False).reset_index(drop=True)
    
    print("By Sector")
    display(arrange(df_Sector ,[sector],["Weight%","Ret%"],'{:.1%}',20, False))
    


    fig = build_heatmap(univ.replace(" Equity", ""), df.head(200),name, sector)
    fig.show()

    return df


def arrange(df, Fields0, Fields,format_pct, head, ascending=False):
    df1 = df[ Fields0 + Fields].copy()
    df1 = df1.sort_values(Fields[len(Fields)-1], ascending=ascending).reset_index(drop=True).head(head)
    
    C = df1.columns  # Get column names

    format_dict = {col: format_pct for col in Fields}
    styled_df = df1.style\
        .bar(subset=[C[c] for c in range(len(C)) if C[c] in Fields], 
             align='mid', 
             width=60, 
             color=["#ff8080", "#80ff80"])\
        .format(format_dict)\
        .set_properties(subset=Fields, **{'text-align': 'right'})  # 数値を右寄せ
    
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

def build_heatmap(univ, df,name, sector):
    """
    Builds a treemap heatmap from DataFrame with ID, Sector, Weight%, Ret%.
    """

    tmp = df[df[sector].isna()]
    
    if len(tmp) > 0:
        print("Delete")
        display(tmp)
        df = df[~df[sector].isna()].reset_index(drop=False)
        
    # Ensure required columns exist
    required_cols = ['ID',"Short",'Kanji', 'Sector', 'Sub', 'Weight%', 'Ret%']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")
    
    # Create range colors based on returns
    range_colors = create_range_colors(df, 'Ret%')
    
    # Build the treemap with custom_data for proper text display
    fig = px.treemap(
        df,
        path=[sector, name],
        values='Weight%',
        color='Ret%',
        color_continuous_scale=centered_color_scale(range_colors),
        range_color=range_colors,
        custom_data=['ID', 'Short',"Sub",'Ret%'],  # Add Ret% to custom_data
        height=600
    )
    
    # Update text template to use customdata
    fig.data[0].texttemplate = (
        "<b>%{label}</b><br>"
        "%{customdata[3]:.2%}"  
    )
    
    fig.data[0].textposition = 'middle center'
    
    # Update layout with dark theme similar to original
    fig.update_layout(
        margin=dict(l=10, r=30, t=35, b=20),
        paper_bgcolor="#212121",
        font=dict(color='white', size=12),
        title={
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
            "Ret: %{customdata[3]:.2%}<br>"  
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

    requests = pd.DataFrame(requests, columns=["Ticker", "Type", "from", "to", "name","sector"])
    universe = requests["Ticker"].tolist()
    
    data_items = {
        'Name': bq.data.name(),
        'Crncy': bq.data.crncy(),
        'ISO': bq.data.country_iso(),
        "Geo": bq.data.fund_geo_focus(),
        "MktCap": bq.data.fund_mkt_cap_focus(),
    }
    
    response = bq.execute(bql.Request(universe, data_items))
    
    List = pd.concat(
        [data_item.df()[data_item.name] for data_item in response], 
        axis=1
    )
    
    List = List.reset_index(drop=False)
    display(List)
    
    return List



def main(requests):

    requests = pd.DataFrame(requests, columns=["Ticker", "Type", "from", "to", "name","sector"])
    List = ListCreation(requests)
    for i in range(len(requests)):

        print("\n"+List.loc[i,"ID"].replace(" Equity", "") + ": " + List.loc[i,"Name"])
        
        tmp0 = requests.loc[i,"from"]
        tmp1 = requests.loc[i,"to"]
        
        if tmp0[len(tmp0)-1] == "D" and tmp1[len(tmp1)-1] == "D":
            
            d_from_orig = int(requests.loc[i,"from"].replace('D', ''))
            d_to_orig = int(requests.loc[i,"to"].replace('D', ''))
            
            d_from1 = ( d_from_orig  - 5) * 2
            d_from1 = str(d_from1) + "D"
            
            data_items = bq.data.px_last(dates=bq.func.range(d_from1, '0D'))
            response = bq.execute(bql.Request(requests.loc[i,"Ticker"], data_items))
            
            tmp = response[0].df()
            tmp = tmp.reset_index(drop=True)
            tmp = tmp.sort_values(by='DATE', ascending=False).dropna().reset_index(drop=True)
    
            d_from =  tmp["DATE"][-d_from_orig]
            d_to =  tmp["DATE"][-d_to_orig]
    
            print(d_from.strftime("%Y/%-m/%-d")+"-"+d_to.strftime("/%-m/%-d"))
    
        
        elif tmp0[len(tmp0)-1] != "D" and tmp1[len(tmp1)-1] == "D":
    
            d_to_orig = int(requests.loc[i,"to"].replace('D', ''))
    
            
            data_items = bq.data.px_last(dates=bq.func.range('-100D', '0D'))
            response = bq.execute(bql.Request(requests.loc[i,"Ticker"], data_items))
            
            tmp = response[0].df()
            tmp = tmp.reset_index(drop=True)
            tmp = tmp.sort_values(by='DATE', ascending=False).dropna().reset_index(drop=True)
    
            d_from =  requests.loc[i,"from"].replace("/","-")
            d_to =  tmp["DATE"][-d_to_orig]
    
            print(d_from.replace("-","/")+"-"+d_to.strftime("/%-m/%-d"))
    
        
        else:
            d_from =  requests.loc[i,"from"].replace("/","-")
            d_to =  requests.loc[i,"to"].replace("/","-")
    
            print(d_from.replace("-","/")+"-"+d_to.replace("-","/"))
    
        globals()[f"df{i}"] = get_data(requests.loc[i,"Ticker"], requests.loc[i,"Type"], d_from, d_to, requests.loc[i,"name"], requests.loc[i,"sector"])


# Cell 3
# Overseas assets, previous day
requests = [
    ("SPY US Equity", "Fund", "-1D", "0D", "ID","Sector"),
    ("IWM US Equity", "Fund", "-1D", "0D", "ID","Sector"),
    ("VGK US Equity", "Fund", "-1D", "0D", "ID","Sector"),
    ("EZU US Equity", "Fund", "-1D", "0D", "ID","Sector"),
    ("INDA US Equity", "Fund", "-1D", "0D", "ID","Sector"),
]

main(requests)



# Cell 4
# Asian assets, toiday
requests = [
    ("1348 JP Equity", "Fund", "-1D", "0D", "Kanji","Sector"),
    ("1343 JP Equity", "Fund", "-1D", "0D", "Kanji","Sub"),
    ("2800 HK Equity", "Fund", "-1D", "0D", "Short","Sector"),
    ("2839 HK Equity", "Fund", "-1D", "0D", "Short","Sector"),
]
main(requests)



# Cell 5
# Specify the from date
requests = [
    ("SPY US Equity", "Fund", "2025/7/31", "0D", "Kanji","Sub"),
    ("1348 JP Equity", "Fund", "2025/7/31", "0D", "Kanji","Sector"),
]
main(requests)
    
