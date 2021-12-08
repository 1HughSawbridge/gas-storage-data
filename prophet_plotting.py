
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from data.api_client import get_agsi


"""
Used to generate the Prophet time series models for % storage stocks
"""

country = 'eu'
# y_col  = 'Storage Injections / Withdrawals (TWh)'
y_col = '% storage stock'

api_response = get_agsi(country)

api_response['Storage Injections / Withdrawals (TWh)'] = (api_response['gasInStorage'].astype(float) -
                                                    api_response['gasInStorage'].astype(float).shift(-1)).clip(-10, 10)

api_response['% storage stock'] = 100 * (
                                        api_response['gasInStorage'].astype(float) /
                                        api_response['workingGasVolume'].astype(float)
                                        )




df=api_response.rename(columns={'gasDayStartedOn': 'ds', y_col: 'y'})[['ds', 'y']].dropna()

mdl = Prophet(
              changepoint_range=0.95,
              yearly_seasonality=3,
              weekly_seasonality=False,
              n_changepoints=20,
              changepoint_prior_scale=0.003
              )

# mdl.add_country_holidays(country_name=country)

mdl.fit(df)

future = mdl.make_future_dataframe(periods=365)
forecast = mdl.predict(future)

forecast_plot=plot_plotly(mdl, forecast)
forecast_plot.update_layout(title=f"{country.upper()} Gas {y_col}")
forecast_plot.update_yaxes(dict(
                                ticksuffix="%",
                                title=y_col))

forecast_plot.update_xaxes(dict(title='Date'))
forecast_plot.show()

# Python
component_plot=plot_components_plotly(mdl, forecast)
component_plot.update_layout(title=f"{country.upper()} Gas {y_col}")
# forecast_plot.update_yaxes(dict(ticksuffix="%"))
component_plot.show()