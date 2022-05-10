# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for launch_site in spacex_df['Launch Site'].unique().tolist():
    launch_sites.append({'label': launch_site, 'value': launch_site})

# Create an app layout
app.layout = html.Div(children=[
    html.Div([
        html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
        ]),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
        id='site-dropdown',
        options= launch_sites,
        value= 'All Sites',
        placeholder= 'Select a Launch Site',
        searchable=True
        ),
        html.Br(),
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),
        
    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=0, max=10000, step=1000,
            marks={
                0: '0',
                1000: '1000 Kg',
                2000: '2000 Kg',
                3000: '3000 Kg',
                4000: '4000 Kg',
                5000: '5000 Kg',
                6000: '6000 Kg',
                7000: '7000 Kg',
                8000: '8000 Kg',
                9000: '9000 Kg',
                10000: '10000 Kg'
            },
            value=[min_payload, max_payload] )
        ], style={'padding': '40px 30px'}),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def updated_pie_chart(site_dropdown):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        df_all = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df_all, 
            values='class', 
            names = 'Launch Site',
            title = 'Total Success Launches by All Sites',
            hole = .2)
        return fig
    else:
        df_selected  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(df_selected,
            names = 'class',
            hole=.2,
            title = 'Total Success Launches The Site: '+site_dropdown)
        return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def updated_scatter_chart(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        mass_low, mass_high = payload_slider
        df_all = spacex_df
        mass_range = (df_all['Payload Mass (kg)'] > mass_low) & (df_all['Payload Mass (kg)'] < mass_high)
        fig = px.scatter(
            df_all[mass_range],
            x='Payload Mass (kg)',
            y='class',
            title = 'Correlation Between Payload and Success for All Sites',
            color='Booster Version Category',
            hover_data=['Payload Mass (kg)'])
    else:
        mass_low, mass_high = payload_slider
        df_selected = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mass_range = (df_selected['Payload Mass (kg)'] > mass_low) & (df_selected['Payload Mass (kg)'] < mass_high)
        fig = px.scatter(
            df_selected[mass_range],
            x='Payload Mass (kg)',
            y='class',
            title = 'Correlation Between Payload and Success for The Site:' + site_dropdown,
            color='Booster Version Category',
            hover_data=['Payload Mass (kg)'])    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
