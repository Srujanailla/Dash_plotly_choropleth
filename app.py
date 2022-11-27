from distutils.log import debug
from pickle import TRUE
import dash
from dash import html

app = dash.Dash(__name__)

#app-layout is used to set the UI elements  
app.layout = html.Div([html.H1('Indian General Elections')])

if __name__=="__main__":
    app.run_server(debug=True)
