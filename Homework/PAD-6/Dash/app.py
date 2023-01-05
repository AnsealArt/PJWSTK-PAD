from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Define visuals
colors = {
    'background': '#111111',
    'text': 'darkslateblue'
}

# Read the data
df = pd.read_csv('winequelity.csv', index_col=0)

# Define page layout
app.layout = html.Div(style={'backgroundcolor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.P(
        children='Dash: A web application framework for your data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children=dash_table.DataTable(
            df.head(10).to_dict('records'), 
            [{"name": i, "id": i} for i in df.columns]
        )
    ),

    html.P(),

    html.Div([
        dcc.RadioItems(['Regression', 'Classification'], 'Regression', id='radio-menu')
    ]),

    html.Div([
        dcc.Dropdown(df.columns[:-1], df.columns[1], id='dropdown-menu')
    ]),

    html.P(),

    html.Div([
        dcc.Graph(id='graph-for-user')
    ])
])

def update_plot_layout(fig):
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color='white'
    )

# Define page actions
@app.callback(
    Output('graph-for-user', 'figure'),
    Input('radio-menu', 'value'),
    Input('dropdown-menu', 'value')
)

def update_figure(value_radio, value_menu):

    """
        in: value_radio = 'Regression' or 'Classification'
        in: value_menu = any of df columns
        out: graph update action

        Function to update graphs based on user's choice:
            - Regression - plot pH by user's choice
            - Classification - plot target by user's choice
    """

    if value_radio == 'Regression':
        fig = px.bar(df, x='pH', y=value_menu)
        update_plot_layout(fig)

    elif value_radio == 'Classification':
        fig = px.scatter(df, x=value_menu, y='target')
        update_plot_layout(fig)

    else:
        return f'Value {value_radio} is not supported'
    
    return fig

# Run application
if __name__ == '__main__':
    app.run_server(debug=True)