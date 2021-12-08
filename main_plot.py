from data.api_client import get_agsi

from plotting import annualised_storage_range

countries = ['NL', 'DE', 'IT', 'ES']

api_responses = {country: get_agsi(country) for country in countries}

figr = annualised_storage_range(api_responses)

figr.show()