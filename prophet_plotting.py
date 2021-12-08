
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from data.api_client import get_agsi


country = 'DE'
column  = 'Storage Injections / Withdrawals'

api_response = get_agsi(country)

api_response['Storage Injections / Withdrawals']=api_response['gasInStorage'].astype(float)-api_response['gasInStorage'].astype(float).shift(-1)

y_col = 'Withdrawals/Injections'

df=api_response.rename(columns={'gasDayStartedOn': 'ds', y_col: 'y'})[['ds', 'y']].dropna()

mdl = Prophet(changepoint_range=1,
              yearly_seasonality=3,
              mcmc_samples=100)

mdl.add_country_holidays(country_name=country)

mdl.fit(df)

future = mdl.make_future_dataframe(periods=365)
forecast = mdl.predict(future)

forecast_plot=plot_plotly(mdl, forecast)
forecast_plot.update_layout(title=f"{country} Gas {column}")
forecast_plot.show()

# Python
component_plot=plot_components_plotly(mdl, forecast)
component_plot.update_layout(title=f"{country} Gas {column}")
component_plot.show()