
```
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Defining the layout of the app - which is the frontend
app.layout = html.Div(children=[

    html.H1("Indian General Elections 2019"),
    dbc.Tabs([
              dbc.Tab([html.P("Lok Sabha is the lower house of the Indian national parliament where members are elected through an adult universal suffrage first-past-the-post voting system to the 543 single member parliamentary constituencies in India. LokSabha elections are held once in five years and members are called Members of Parliament (MP)."), 
              html.P("  In the Indian Political System, reservation is provided to historically disadvantaged groups to boost their representation. Some of the constituencies are reserved for only those candidates falling under a certain reservation category. For example, in the general elections, a Scheduled Caste (SC) or Scheduled Tribe (ST) candidate will be able to contest from a general seat. However, from a SC/ST reserved parliamentary constituency, only a SC/STC candidate can contest."), "Data Sources:", 
              html.Ul(html.A("  Creative Commons Attribution-ShareAlike2.5 India", href='https://github.com/datameet/maps/tree/master/parliamentary-constituencies'))], label='Introduction'),

              dbc.Tab([

                dcc.Dropdown(id='state_dropdown',value='UTTAR PRADESH',options=[{'label': state, 'value':str(state)} for state in states_unique]),
                dcc.Graph(id='PC_Reservation_Status')], label="Reservation Status"),
          
            ])
    

])  

#Running the app
if __name__ == '__main__':
    app.run_server(debug=True)

```
