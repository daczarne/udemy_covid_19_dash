import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# GitHub repos URLs
url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Get the data into the app
confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# Unpivot the data frames
total_confirmed = confirmed.melt(
  id_vars = ["Province/State", "Country/Region", "Lat", "Long"],
  value_vars = confirmed.columns[4:],
  var_name = "date",
  value_name = "confirmed"
)

total_deaths = deaths.melt(
  id_vars = ["Province/State", "Country/Region", "Lat", "Long"],
  value_vars = deaths.columns[4:],
  var_name = "date",
  value_name = "deaths"
)

total_recovered = recovered.melt(
  id_vars = ["Province/State", "Country/Region", "Lat", "Long"],
  value_vars = recovered.columns[4:],
  var_name = "date",
  value_name = "recovered"
)

# Merge data frames
covid_data = total_confirmed.merge(
  right = total_deaths,
  how = "left",
  on = ["Province/State", "Country/Region", "date", "Lat", "Long"]
).merge(
  right = total_recovered,
  how = "left",
  on = ["Province/State", "Country/Region", "date", "Lat", "Long"]
)

# Wrangle data
covid_data["recovered"] = covid_data["recovered"].fillna(0)
covid_data["active"] = covid_data["confirmed"] - covid_data["deaths"] - covid_data["recovered"]
covid_data["date"] = pd.to_datetime(covid_data["date"])


# Instanciate the app
app = dash.Dash(__name__, )

# Build the layout
app.layout = html.Div(
	[
		html.Div(
			[
				html.Div(
					[
						html.Img(
							src = app.get_asset_url("corona-logo-1.jpg"),
							id = "corona-image",
							style = {
								"height": "60px",
								"width": "auto",
								"margin-bottom": "25px"
							}
						)
					],
					className = "one-third column"
				)
			],
			id = "header",
			className = "row flex-display",
			style = {
				"margin-bottom": "25px"
			}
		)
	],
	id = "mainContainer",
	style = {
		"display": "flex",
		"flex-direction": "column"
	}
)

# Build the callbacks


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
