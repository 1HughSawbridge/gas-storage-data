
import requests
import pandas as pd
import json
import os


def get_agsi(country, **kwargs):

    root = 'https://agsi.gie.eu/api/data/'

    header = {"x-key": os.getenv('AGSI_API_KEY')}

    response = requests.get(url=f'{root}{country}', params=kwargs, headers=header)

    df = pd.DataFrame(json.loads(response.content))

    df = df.loc[df['status'] != 'N']

    return df
