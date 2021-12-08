from plotly.subplots import make_subplots
import pandas as pd


def annualised_storage_range(api_response):
    api_response['gasDayStartedOn'] = pd.to_datetime(api_response['gasDayStartedOn'])

    api_response['Week of year'] = api_response['gasDayStartedOn'].dt.isocalendar().week

    api_response['Week starting'] = api_response['gasDayStartedOn'].dt.to_period('W').dt.start_time

    api_response['% storage stock'] = api_response['gasInStorage'].astype(float) / api_response[
        'workingGasVolume'].astype(float)

    api_response['gasInStorage'] = api_response['gasInStorage'].astype(float)

    thisyear = api_response.loc[api_response['gasDayStartedOn'].dt.year==2021]
    before = api_response.loc[api_response['gasDayStartedOn'].dt.year<2021]

    qs = [0, 0.1, .5, .9, 1]

    before_grouping_dat = before.groupby('Week of year')[['% storage stock']].quantile(q=qs)

    thisyear_grouping_dat = thisyear.groupby('Week starting')[['% storage stock']].mean()



    before_plotly_data=before_grouping_dat.reset_index().pivot(index='Week of year',columns='level_1').iloc[:52]
    fg = make_subplots(rows=1)


    fg.add_scatter(x=before_plotly_data.index,
                   y=before_plotly_data[('% storage stock',1)]*100,
                   name='Min', row=1, col=1, marker_color='#c7bcba')

    fg.add_scatter(x=before_plotly_data.index,
                   y=before_plotly_data[('% storage stock',0)]*100,
                   name='Min', row=1, col=1, marker_color='#c7bcba')

    fg.add_scatter(x=before_plotly_data.index,
                   y=before_plotly_data[('% storage stock', 0.1)]*100,
                   name='10th percentile', row=1, col=1, marker_color='#f6d35f')

    fg.add_scatter(x=before_plotly_data.index,
                   y=before_plotly_data[('% storage stock', 0.9)]*100,
                   name='90th percentile', row=1, col=1,  marker_color='#f6d35f')

    fg.add_scatter(x=before_plotly_data.index,
                   y=before_plotly_data[('% storage stock', 0.5)]*100,
                   name='median', row=1, col=1,  marker_color='#c24428')

    fg.add_scatter(x=before_plotly_data.index,
                   y=thisyear_grouping_dat['% storage stock']*100,
                   name='2021', row=1, col=1, marker_color='#213264')

    fg.update_yaxes(dict(ticksuffix="%", title='Percentage Storage(%)'))
    fg.update_xaxes(dict(title='Week of year'))


    return fg