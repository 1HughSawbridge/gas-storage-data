import pandas as pd

from data.api_client import get_agsi

from plotting import annualised_storage_range


country='DE'
api_response = get_agsi(country)

api_response['Storage Injections / Withdrawals']=api_response['gasInStorage'].astype(float)-api_response['gasInStorage'].astype(float).shift(-1)

y_col = 'Withdrawals/Injections'

figr = annualised_storage_range(api_response)
figr.update_layout(title_text='{}: current storage progression vs historic range (from {} to {})'.format(country,
                                                                                                  api_response['gasDayStartedOn'].head(1).iloc[0].strftime('%Y-%m'),
                                                                                                  api_response['gasDayStartedOn'].tail(1).iloc[0].strftime('%Y-%m'))
                   )
figr.show()