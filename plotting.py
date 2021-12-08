from plotly.subplots import make_subplots
import pandas as pd


def annualised_storage_range(api_responses: dict):

    fg = make_subplots(rows=len(api_responses),
                       row_titles=list(api_responses.keys()))
    row=0
    for country in api_responses:
        country_frame = api_responses[country]
        row+=1
        country_frame['gasDayStartedOn'] = pd.to_datetime(country_frame['gasDayStartedOn'])

        country_frame['Week of year'] = country_frame['gasDayStartedOn'].dt.isocalendar().week

        country_frame['Week starting'] = country_frame['gasDayStartedOn'].dt.to_period('W').dt.start_time

        country_frame['% storage stock'] = (
                                            country_frame['gasInStorage'].astype(float) /
                                            country_frame['workingGasVolume'].astype(float)
                                            )

        country_frame['gasInStorage'] = country_frame['gasInStorage'].astype(float)

        thisyear = country_frame.loc[country_frame['gasDayStartedOn'].dt.year==2021]
        before = country_frame.loc[country_frame['gasDayStartedOn'].dt.year<2021]

        qs = [0, 0.1, .5, .9, 1]

        before_grouping_dat = before.groupby('Week of year')[['% storage stock']].quantile(q=qs)

        thisyear_grouping_dat = thisyear.groupby('Week starting')[['% storage stock']].mean()

        before_plotly_data=before_grouping_dat.reset_index().pivot(index='Week of year',columns='level_1').iloc[:52]


        fg.add_scatter(x=before_plotly_data.index,
                       y=thisyear_grouping_dat['% storage stock']*100,
                       name='2021', row=row, col=1, marker_color='#213264',showlegend=row==1)

        fg.add_scatter(x=before_plotly_data.index,
                       y=before_plotly_data[('% storage stock',1)]*100,
                       name='Max', row=row, col=1, marker_color='#c7bcba',showlegend=row==1)


        fg.add_scatter(x=before_plotly_data.index,
                       y=before_plotly_data[('% storage stock', 0.1)]*100,
                       name='10th percentile', row=row, col=1, marker_color='#f6d35f',showlegend=row==1)

        fg.add_scatter(x=before_plotly_data.index,
                       y=before_plotly_data[('% storage stock', 0.5)]*100,
                       name='median', row=row, col=1,  marker_color='#c24428',showlegend=row==1)

        fg.add_scatter(x=before_plotly_data.index,
                       y=before_plotly_data[('% storage stock', 0.9)]*100,
                       name='90th percentile', row=row, col=1,  marker_color='#f6d35f',showlegend=row==1)


        fg.add_scatter(x=before_plotly_data.index,
                       y=before_plotly_data[('% storage stock',0)]*100,
                       name='Min', row=row, col=1, marker_color='#c7bcba',showlegend=row==1)

        fg.update_yaxes(dict(ticksuffix="%", title='Storage (%)'))
        fg.update_xaxes(dict(title='Week of year'))

    inserts=( country_frame['gasDayStartedOn'].tail(1).iloc[0].strftime('%Y-%m'),'2020-12',)

    fg.update_layout(title_text='Current storage progression vs historic range (from {} to {})'.format(*inserts)
                       )
    return fg