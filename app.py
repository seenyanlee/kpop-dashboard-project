# %% [markdown]
# # Kpop Dashboard Project

# %% [markdown]
# ## Import libraries

# %%
from dash import Dash, dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import numpy as np
import pandas as pd
# from plotly_calplot import calplot
import plotly.express as px
from summarytools import dfSummary

# %% [markdown]
# ## Exploratory data analysis

# %% [markdown]
# ### Load dataset

# %%
# Data retrieved from https://www.kaggle.com/datasets/nicolsalayoarias/all-kpop-idols/?select=kpopidolsv3.csv
data = pd.read_csv('kpopidolsv3.csv')
data.head()

# %% [markdown]
# ### Data cleaning

# %%
# Extract required columns
df = data[["Full Name", "Group", "Former Group", "Date of Birth", "Debut", "Country", "Gender"]]

dfSummary(df)

# %%
# Drop rows where Full Name is missing (unable to identify) and Debut is filled with a placeholder date (not yet debuted)
df = df.loc[df["Full Name"].isnull() is False]
df = df.loc[df["Debut"] != "0/01/1900"]

# Convert columns to required datatypes
df = df.astype({"Full Name": str, "Group": str, "Former Group": str, "Country": str, "Gender": str})
df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], format = "%d/%m/%Y")
df["Debut"] = pd.to_datetime(df["Debut"], format = "%d/%m/%Y")

# Filter for idols from 2nd Generation onwards (debuted in or after 2005)
df = df.loc[df["Debut"] >= "01/01/2005"]

df.dtypes

# %%
dfSummary(df)

# %% [markdown]
# ### Feature engineering

# %%
# Add new columns
df["Debut Year"] = df["Debut"].dt.year
df["Debut Month"] = df["Debut"].dt.month
df["Birth Year"] = df["Date of Birth"].dt.year
df["Birth Month"] = df["Date of Birth"].dt.month
df["Debut Age"] = df["Debut Year"] - df["Birth Year"]

# %%
# Convert data types of the new columns
# Fill Nan values in the new columns with 0 in order to allow conversion to int
df[["Debut Year", "Debut Month", "Birth Year", "Birth Month", "Debut Age"]] = df[["Debut Year", "Debut Month", "Birth Year", "Birth Month", "Debut Age"]].fillna(0).astype(int)

df.dtypes

# %% [markdown]
# ## Data visualisation

# %%
load_figure_template(["pulse_dark"])

# %% [markdown]
# ### Idol birthday analysis

# %% [markdown]
# 1. Calendar plot: idol birthday distribution

# %%
# Group by

# %% [markdown]
# 2. Bar plot: idol birth year distribution (all / male / female)

# %%
# Part 1: Group by birth year on all idols
bday2 = df.groupby(['Birth Year']).count()['Full Name'].iloc[1:]
bday2.rename('Idol count', inplace = True)

# %%
fig_bday2 = px.bar(bday2, x = bday2.index, y = 'Idol count', title = 'Birth year distribution of K-Pop idols',
             color = 'Idol count')

fig_bday2.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# fig_bday2.show()

# %%
# Part 2: Group by birth year and gender on all idols
bday2a = df.groupby(['Gender', 'Birth Year']).count()['Full Name']
bday2a = pd.concat([bday2a.iloc[:26], bday2a.iloc[27:]], axis = 0)
bday2a.rename('Idol count', inplace = True)
bday2a = bday2a.reset_index()

# %%
fig_bday2a = px.bar(bday2a, x = 'Birth Year', y = 'Idol count', title = 'Birth year distribution of K-Pop idols by gender', 
             color = 'Gender', barmode = 'group')

fig_bday2a.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# fig_bday2a.show()

# %% [markdown]
# 3. Bar plot: idol birth month distribution (all / male / female)

# %%
# Part 1: Group by birth month on all idols
bday3 = df.groupby(['Birth Month']).count()['Full Name'].iloc[1:]
bday3.rename('Idol count', inplace = True)

# %%
fig_bday3 = px.bar(bday3, x = bday3.index, y = 'Idol count', title = 'Birth month distribution of K-Pop idols',
             color = 'Idol count')

fig_bday3.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

# fig_bday3.show()

# %%
# Part 2: Group by birth month and gender on all idols
bday3a = df.groupby(['Gender', 'Birth Month']).count()['Full Name']
bday3a = pd.concat([bday3a.iloc[:12], bday3a.iloc[13:]], axis = 0)
bday3a.rename('Idol count', inplace = True)
bday3a = bday3a.reset_index()

# %%
fig_bday3a = px.bar(bday3a, x = 'Birth Month', y = 'Idol count', title = 'Birth month distribution of K-Pop idols by gender',
             color = 'Gender', barmode = 'group')

fig_bday3a.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

# fig_bday3a.show()

# %% [markdown]
# ### Debut analysis

# %% [markdown]
# 1. Calendar plot: debut anniversary distribution

# %%
# Group by Debut Month

# %% [markdown]
# 2. Bar plot: debut anniversary distribution by month

# %%
# Group by Debut Month and exclude rows with placeholder / invalid dates
debut2 = df.groupby(['Debut Month']).count()['Full Name'].iloc[1:]
debut2.rename('Idol count', inplace = True)

# %%
fig_debut2 = px.bar(debut2, x = debut2.index, y = 'Idol count', title = 'Debut month distribution of K-Pop idols',
             color = 'Idol count')

fig_debut2.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

# fig_debut2.show()

# %% [markdown]
# 3. Bubble plot: debut age distribution (all / male / female)

# %%
# Group by Debut Age and Gender
# debut3 = df.groupby(['Debut Age', 'Gender']).count()['Full Name']
# debut3.rename('Idol count', inplace = True)
# debut3 = debut3.reset_index()

# %%
# df.sort_values(by=['Debut Age'])

# %% [markdown]
# 4. Bar plot: number of debuted idols per year

# %%
# Group by Debut Year and count by idol name; exclude rows with placeholder / invalid dates
debut4 = df.groupby(['Debut Year']).count()['Full Name']
debut4.rename('Idol count', inplace = True)

# %%
fig_debut4 = px.bar(debut4, x = debut4.index, y = 'Idol count', title = 'Number of debuted K-Pop idols per year',
             color = 'Idol count')

fig_debut4.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# fig_debut4.show()

# %% [markdown]
# 5. Bar plot: number of debuted groups per year

# %%
# Group by Debut Year and count by group name; exclude rows with placeholder / invalid dates
debut5 = df[['Group', 'Debut Year']].groupby(['Debut Year']).nunique()['Group']
debut5.rename('Group count', inplace = True)

# %%
fig_debut5 = px.bar(debut5, x = debut5.index, y = 'Group count', title = 'Number of debuted K-Pop groups per year',
             color = 'Group count')

fig_debut5.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# fig_debut5.show()

# %% [markdown]
# ### Meta-analysis

# %% [markdown]
# 1. Pie chart: distribution of groups by gender

# %%
# Group by Gender
meta1 = df.groupby(['Gender']).count()['Full Name']
meta1.rename('Idol count', inplace = True)

# %%
fig_meta1 = px.pie(meta1, values = 'Idol count', names = meta1.index, title = 'Gender ratio of K-Pop idols')

# fig_meta1.show()

# %% [markdown]
# 2. Bar plot: number of members per group

# %%
# Group by Group and count by existing group members, then group by the number of members
meta2 = df[['Group', 'Full Name']].groupby(['Group']).nunique()['Full Name']
meta2 = meta2.groupby(meta2.values).count()[:-1]
meta2.rename('Group count', inplace = True)
meta2.index.name = 'Number of members'

# %%
fig_meta2 = px.bar(meta2, x = meta2.index, y = 'Group count', title = 'Number of members per K-Pop group',
             color = 'Group count')

fig_meta2.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# fig_meta2.show()

# %% [markdown]
# 3. Pie chart: idol's country of origin distribution

# %%
# Group by Country and relabel countries with few counts
meta3 = df.groupby(['Country']).count()['Full Name']
meta3.rename('Idol count', inplace = True)
meta3.index = np.where(meta3 < 3, 'Other countries', meta3.index)
meta3.index.name = 'Country / region of origin'
# meta3

# %%
fig_meta3 = px.pie(meta3, values = 'Idol count', names = meta3.index, title = 'Country / region of origin ratio of K-Pop idols')

# fig_meta3.show()

# %% [markdown]
# ## Dashboard

# %% [markdown]
# ### Dash app setup

# %%
app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])

# %% [markdown]
# ### Dashboard layout and callback

# %%
# Define repeatedly-used styling
H2_STYLE = 'my-4 ms-2 me-2 text-primary border-bottom border-primary'
H3_STYLE = 'mt-4 mb-3 ms-4 opacity-75'
TAB_STYLE = 'bg-primary bg-gradient bg-opacity-50 text-black'
TAB_SELECTED_STYLE = 'bg-light bg-gradient text-primary mx-2'

# %%
app.layout = html.Div([
        html.H1('K-Pop Data Visualisations', className='mt-5 mb-2 ms-2 me-2 bg-primary bg-opacity-50 text-dark rounded'),
        html.A('Find data source here', href='https://www.kaggle.com/datasets/nicolsalayoarias/all-kpop-idols/?select=kpopidolsv3.csv', className='mb-4 ms-2'),
        html.Div([
            html.H2('Idol Birthday Analysis', className=H2_STYLE),
            html.Div([
                html.H3('Idol birth year distribution', className=H3_STYLE),
                dcc.Tabs(id="tabs-birth-year", value='overall-birth-year', className='mx-2', children=[
                    dcc.Tab(label='Overall', value='overall-birth-year', className=TAB_STYLE, selected_className=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Male / Female', value='splitted-birth-year', className=TAB_STYLE, selected_className=TAB_SELECTED_STYLE),
                ]),
                html.Div(id='tabs-content-birth-year')
            ]),
            html.Div([
                html.H3('Idol birth month distribution', className=H3_STYLE),
                dcc.Tabs(id="tabs-birth-month", value='overall-birth-month', className='mx-2', children=[
                    dcc.Tab(label='Overall', value='overall-birth-month', className=TAB_STYLE, selected_className=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Male / Female', value='splitted-birth-month', className=TAB_STYLE, selected_className=TAB_SELECTED_STYLE),
                ]),
                html.Div(id='tabs-content-birth-month')
            ]),
        ]),
        html.Div([
            html.H2('Idol Debut Analysis', className=H2_STYLE),
            html.Div([
                html.H3('Idol debut month distribution', className=H3_STYLE),
                dcc.Graph(figure=fig_debut2, className='mx-2'),
            ]),
            html.Div([
                html.H3('Number of debuted idols per year', className=H3_STYLE),
                dcc.Graph(figure=fig_debut4, className='mx-2'),
            ]),
            html.Div([
                html.H3('Number of debuted groups per year', className=H3_STYLE),
                dcc.Graph(figure=fig_debut5, className='mx-2'),
            ]),
        ]),
        html.Div([
            html.H2('Meta-analysis', className=H2_STYLE),
            html.Div([
                html.H3('Gender ratio of idols', className=H3_STYLE),
                dcc.Graph(figure=fig_meta1, className='mx-2'),
            ]),
            html.Div([
                html.H3('Number of members per group', className=H3_STYLE),
                dcc.Graph(figure=fig_meta2, className='mx-2'),
            ]),
            html.Div([
                html.H3('Country of origin distribution of idols', className=H3_STYLE),
                dcc.Graph(figure=fig_meta3, className='mx-2')
            ])
        ])
])

# Render tabs for birth year analysis
@callback(Output('tabs-content-birth-year', 'children'), Input('tabs-birth-year', 'value'))
def render_content(tab):
    if tab == 'overall-birth-year':
        return html.Div([
            dcc.Graph(figure=fig_bday2, className='mx-2')
        ])
    elif tab == 'splitted-birth-year':
        return html.Div([
            dcc.Graph(figure=fig_bday2a, className='mx-2')
        ])

# Render tabs for birth month analysis
@callback(Output('tabs-content-birth-month', 'children'), Input('tabs-birth-month', 'value'))
def render_content(tab):
    if tab == 'overall-birth-month':
        return html.Div([
            dcc.Graph(figure=fig_bday3, className='mx-2')
        ])
    elif tab == 'splitted-birth-month':
        return html.Div([
            dcc.Graph(figure=fig_bday3a, className='mx-2')
        ])

# %% [markdown]
# ### Run dashboard

# %%
if __name__ == '__main__':
    app.run(debug = True)
