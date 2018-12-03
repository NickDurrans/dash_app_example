
# coding: utf-8

# # Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income). The dashboard will have two graphs:
# 
# 1) The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data.
# 
# 2) The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' (more here)

# In[1]:


import dash
#to create apps 
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('nama_10_gdp_1_Data.csv', na_values=':',usecols=["TIME","UNIT","GEO","NA_ITEM","Value"])
df['Value']=df['Value'].str.replace(',','').astype(float)
df=df.dropna()

#~ for dropping values

df=df[~df.GEO.str.contains("Eur") ==True]
df=df[~df.UNIT.str.contains("Current prices, million euro")]
df=df[~df.UNIT.str.contains("Chain linked volumes, index 2010=100")]

print(df.head())
available_indicators = df['NA_ITEM'].unique()
GEOS=df['GEO'].unique()
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    html.H1('\n'),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in GEOS],
                value='European Union (current composition)'
            ),
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column-b',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic-b')
    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == xaxis_column_name) &( dff['GEO']==str(i) )]['Value'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name) &( dff['GEO']==str(i))]['Value'],
            text=dff[dff['GEO']==str(i)]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i[:20]
            
        )for i in dff.GEO.unique()
                ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic-b', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column-b', 'value')])
def update_graph_b(country_name, yaxis_column_b_name,):
    dff = df[df['GEO'] == country_name]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_b_name]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column_b_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_b_name]['Value'],
            mode='lines'
            
            
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'YEAR',
                'type': 'linear' 
            },
            yaxis={
                'title': yaxis_column_b_name,
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

