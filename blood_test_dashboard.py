
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Sample/mock data; replace this with your own CSV if available
data = {
    'Date': pd.date_range(start='2020-01-01', periods=12, freq='M').tolist() * 3,
    'Test Name': ['Total B12'] * 12 + ['Serum Folate'] * 12 + ['Vit B6'] * 12,
    'Value': [220, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450,
              30, 35, 33, 31, 30, 28, 29, 32, 34, 36, 37, 38,
              80, 90, 85, 88, 91, 93, 96, 99, 102, 105, 108, 110],
    'Unit': ['pmol/L'] * 12 + ['nmol/L'] * 12 + ['nmol/L'] * 12
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = 'Blood Test Dashboard'

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Blood Test Trends Dashboard'),

    html.Label('Select Blood Tests:'),
    dcc.Dropdown(
        id='test-selector',
        options=[{'label': test, 'value': test} for test in df['Test Name'].unique()],
        value=['Total B12', 'Serum Folate'],
        multi=True
    ),

    dcc.Graph(id='trend-graph')
])

# Callback to update the graph based on selected tests
@app.callback(
    Output('trend-graph', 'figure'),
    [Input('test-selector', 'value')]
)
def update_graph(selected_tests):
    traces = []
    for test in selected_tests:
        test_df = df[df['Test Name'] == test]
        traces.append(go.Scatter(
            x=test_df['Date'],
            y=test_df['Value'],
            mode='lines+markers',
            name=f"{test} ({test_df['Unit'].iloc[0]})"
        ))

    layout = go.Layout(
        title='Selected Blood Test Trends Over Time',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Test Values'},
        hovermode='closest'
    )

    return {'data': traces, 'layout': layout}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
