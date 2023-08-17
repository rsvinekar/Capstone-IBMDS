# Import required libraries for dash 2.x
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].unique()
opts = [{'label': 'All Sites', 'value': 'ALL'}]
for site in sites: 
    opt = {}
    opt['label']=site
    opt['value']=site
    opts.append(opt)
# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=opts,
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload],
                                    marks={i: i for i in range(0, 10000, 1000)}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Br(),html.Br(),html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='All Sites Data: Successful Launches')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        class_num = data.groupby(['class']).value_counts({'Launch Site'}).reset_index(name='counts')
        class_num.replace({0:"Failure", 1:"Success"}, inplace=True)
        fig = px.pie(class_num, values='counts', names='class', title="Site:"+ entered_site +" Failure vs Success", color_discrete_sequence=["red", "green"])
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,payload_range):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0],payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category",title="All Launch sites", labels={
                     "class": "Launch Outcome",
                     "Booster Version Category": "Booster Category"
                 })
        fig.update_layout(legend_title_text="Booster Category")
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",color="Booster Version Category",title="Launch Site:"+ entered_site, labels={
                     "class": "Launch Outcome",
                     "Booster Version Category": "Booster Category"
                 })
        return fig
		


# Run the app
if __name__ == '__main__':
    app.run_server()
