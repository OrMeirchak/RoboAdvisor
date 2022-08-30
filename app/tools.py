from xmlrpc.client import boolean
import re
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import pandas as pd

def _map(x:int, in_min:int, in_max:int, out_min:int, out_max:int)->int:
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def validate_email(email:str)->bool:
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,email):
      return True
   return False

def json_to_df(json):
    return pd.json_normalize(json)

def df_to_plt_gini(df):
    # plot frontier, max sharpe & min Gini values with a scatterplot
    # find min Gini & max sharpe values in the dataframe (df)
    min_gini =df['Gini'].min()
    max_sharpe = df['Sharpe Ratio'].max()
    max_profolio_annual = df['Profolio_annual'].max()
    max_gini = df['Gini'].max()

    # use the min, max values to locate and create the two special portfolios
    selected = ["SPY","IEI","LQD","BTC-USD","DAX","GSG"]
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Gini'] == min_gini]
    max_profolios_annual = df.loc[df['Profolio_annual'] == max_profolio_annual]
    max_ginis = df.loc[df['Gini'] == max_gini]

    # plot frontier, max sharpe & min Gini values with a scatterplot
    plt.style.use('seaborn-dark')
    df.plot.scatter(x='Gini', y='Profolio_annual', c='Sharpe Ratio',
    cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=sharpe_portfolio['Gini'], y=sharpe_portfolio['Profolio_annual'], c='green', marker='D', s=200)
    plt.scatter(x=min_variance_port['Gini'], y=min_variance_port['Profolio_annual'], c='orange', marker='D', s=200 )
    plt.scatter(x=max_ginis['Gini'], y=max_profolios_annual['Profolio_annual'], c='red', marker='D', s=200 )
    plt.style.use('seaborn-dark')

    plt.xlabel('Gini (Std. Deviation) Percentage %')
    plt.ylabel('Expected profolio annual Percentage %')
    plt.title('Efficient Frontier')
    plt.subplots_adjust(bottom=0.4)

        # ------------------ Pritning 3 optimal Protfolios -----------------------
        #Setting max_X, max_Y to act as relative border for window size

    red_num = df.index[df["Profolio_annual"] == max_profolio_annual]
    yellow_num = df.index[df['Gini'] == min_gini]
    green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
    multseries = pd.Series([1,1,1]+[100 for stock in selected], index=['Profolio_annual', 'Gini', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected])
    with pd.option_context('display.float_format', '%{:,.2f}'.format):
        plt.figtext(0.2, 0.15, "Max Profolio_annual Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique',ha='center', va='center', wrap=True)
        plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center', wrap=True)
        plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center', wrap=True)

    print(df.loc[yellow_num[0]].multiply(multseries)) 

    x=df.loc[yellow_num[0]].multiply(multseries)

    plt.show()


    fig = plt.figure()

    return plt
    #plot sth

    #tmpfile = BytesIO()
    #fig.savefig(tmpfile, format='png')
    #encoded = base64.b64encode(tmpfile.getvalue()).decode('utf8') 
    #html = 'Some html head' + "<img src='data:image/png;base64,{{}}'>".format(encoded) + 'Some more html'

    #with open('test.html','w') as f:
      #f.write(html)


def return_graph(plt):
    x = np.arange(0,np.pi*3,.1)
    y = np.sin(x)

    fig = plt.figure()
    plt.plot(x,y)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data