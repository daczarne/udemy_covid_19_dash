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

# Daily totals
covid_data_1 = covid_data.groupby(["date"])[["confirmed", "deaths", "recovered", "active"]].sum().reset_index()

# Helper functions
def intraday_variation(a, b):
	return round((1 - b / a) * 100, 2)

# Instanciate the app
app = dash.Dash(__name__, )

# Build the layout
app.layout = html.Div(
	children = [
		# (First row) Header: Logo - Title - Last updated
		html.Div(
			children = [
				# Logo
				html.Div(
					children = [
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
				),
				html.Div(
					children = [
						# Title and subtitle
						html.Div(
							children = [
								html.H3(
									children = "Covid-19",
									style = {
										"margin-bottom": "0",
										"color": "white"
									}
								),
								html.H5(
									children = "Track Covid-19 cases",
									style = {
										"margin-bottom": "0",
										"color": "white"
									}
								)
							]
						)
					],
					className = "one-half column",
					id = 'title'
				),
				# Last updated
				html.Div(
					children = [
						html.H6(
							children = "Last Updated " + str(covid_data["date"].iloc[-1].strftime("%B %d, %Y")),
							style = {
								"color": "orange"
							}
						)
					],
					className = "one-thid column",
					id = "title1"
				)
			],
			id = "header",
			className = "row flex-display",
			style = {
				"margin-bottom": "25px"
			}
		),
		# (Second row) Cards: Global cases - Global deaths - Global recovered - Global active
		html.Div(
			children = [
				# (Column 1): Global cases
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Global cases",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total value
						html.P(
							children = f"{covid_data_1['confirmed'].iloc[-1]:,.0f}",
							style = {
								"textAlign": "center",
								"color": "orange",
								"fontSize": 40
							}
						),
						# New cases
						html.P(
							children = "new: " +
								f"{covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]:,.0f}" +
								" (" +
								f"{round(((covid_data_1['confirmed'].iloc[-1] - covid_data_1['confirmed'].iloc[-2]) / covid_data_1['confirmed'].iloc[-1]) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "orange",
								"fontSize": 15,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 2): Global deaths
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Global deaths",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total value
						html.P(
							children = f"{covid_data_1['deaths'].iloc[-1]:,.0f}",
							style = {
								"textAlign": "center",
								"color": "#dd1e35",
								"fontSize": 40
							}
						),
						# New deaths
						html.P(
							children = "new: " +
								f"{covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]:,.0f}" +
								" (" +
								f"{round(((covid_data_1['deaths'].iloc[-1] - covid_data_1['deaths'].iloc[-2]) / covid_data_1['deaths'].iloc[-1]) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "#dd1e35",
								"fontSize": 15,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 3): Global recovered
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Global recovered",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total recovered
						html.P(
							children = f"{covid_data_1['recovered'].iloc[-1]:,.0f}",
							style = {
								"textAlign": "center",
								"color": "green",
								"fontSize": 40
							}
						),
						# New recovered
						html.P(
							children = "new: " +
								f"{covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]:,.0f}" +
								" (" +
								f"{round(((covid_data_1['recovered'].iloc[-1] - covid_data_1['recovered'].iloc[-2]) / covid_data_1['recovered'].iloc[-1]) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "green",
								"fontSize": 15,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				),
				# (Column 4): Global active
				html.Div(
					children = [
						# Title
						html.H6(
							children = "Global active",
							style = {
								"textAlign": "center",
								"color": "white"
							}
						),
						# Total v
						html.P(
							children = f"{covid_data_1['active'].iloc[-1]:,.0f}",
							style = {
								"textAlign": "center",
								"color": "#e55467",
								"fontSize": 40
							}
						),
						# New active
						html.P(
							children = "new: " +
								f"{covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]:,.0f}" +
								" (" +
								f"{round(((covid_data_1['active'].iloc[-1] - covid_data_1['active'].iloc[-2]) / covid_data_1['active'].iloc[-1]) * 100, 2)}" +
								"%)",
							style = {
								"textAlign": "center",
								"color": "#e55467",
								"fontSize": 15,
								"margin-top": "-18px"
							}
						)
					],
					className = "card_container three columns"
				)
			],
			className = "row flex-display"
		),
		# (Third row):
		html.Div(
			[
				# Column 1: Country selector
				html.Div(
					[
						html.P(
							children = "Select Country: ",
							className = "fix_label",
							style = {
								"color": "white"
							}
						),
						dcc.Dropdown(
							id = "w_countries",
							multi = False,
							searchable = True,
							value = "",
							placeholder = "Select Country",
							options = [{"label": c, "value": c} for c in (covid_data["Country/Region"].unique())],
							className = "dcc_compon"
						)
					],
					className = "create_container three columns"
				)
			],
			className = "row flex-display"
		)
	]
)

# Build the callbacks


# Run the app
if __name__ == "__main__":
  app.run_server(debug = True)
