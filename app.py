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
df = data[["Full Name", "Stage Name", "Group", "Former Group", "Date of Birth", "Debut", "Country", "Gender"]]

dfSummary(df)

# %%
# Drop rows where Full Name is missing (unable to identify) and Debut is filled with a placeholder date (not yet debuted)
df = df.loc[df["Full Name"].isnull() == False]
df = df.loc[df["Debut"] != "0/01/1900"]

# Convert columns to required datatypes
df = df.astype({"Full Name": str, "Stage Name": str, "Group": str, "Former Group": str, "Country": str, "Gender": str})
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
fig_bday2 = px.bar(bday2, x = bday2.index, y = 'Idol count', 
                   title = 'Birth year distribution of K-Pop idols', color = 'Idol count')

fig_bday2.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# %%
# Part 2: Group by birth year and gender on all idols
bday2a = df.groupby(['Gender', 'Birth Year']).count()['Full Name']
bday2a = pd.concat([bday2a.iloc[:26], bday2a.iloc[27:]], axis = 0)
bday2a.rename('Idol count', inplace = True)
bday2a = bday2a.reset_index()

# %%
fig_bday2a = px.bar(bday2a, x = 'Birth Year', y = 'Idol count', barmode = 'group',
                    title = 'Birth year distribution of K-Pop idols by gender', color = 'Gender')

fig_bday2a.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# %% [markdown]
# 3. Bar plot: idol birth month distribution (all / male / female)

# %%
# Part 1: Group by birth month on all idols
bday3 = df.groupby(['Birth Month']).count()['Full Name'].iloc[1:]
bday3.rename('Idol count', inplace = True)

# %%
fig_bday3 = px.bar(bday3, x = bday3.index, y = 'Idol count', 
                   title = 'Birth month distribution of K-Pop idols', color = 'Idol count')

fig_bday3.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

# %%
# Part 2: Group by birth month and gender on all idols
bday3a = df.groupby(['Gender', 'Birth Month']).count()['Full Name']
bday3a = pd.concat([bday3a.iloc[:12], bday3a.iloc[13:]], axis = 0)
bday3a.rename('Idol count', inplace = True)
bday3a = bday3a.reset_index()

# %%
fig_bday3a = px.bar(bday3a, x = 'Birth Month', y = 'Idol count', barmode = 'group',
                    title = 'Birth month distribution of K-Pop idols by gender', color = 'Gender')

fig_bday3a.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

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
fig_debut2 = px.bar(debut2, x = debut2.index, y = 'Idol count', 
                    title = 'Debut month distribution of K-Pop idols', color = 'Idol count')

fig_debut2.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1, 13)),
        ticktext = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
)

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
fig_debut4 = px.bar(debut4, x = debut4.index, y = 'Idol count', 
                    title = 'Number of debuted K-Pop idols per year', color = 'Idol count')

fig_debut4.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

# %% [markdown]
# 5. Bar plot: number of debuted groups per year

# %%
# Group by Debut Year and count by group name; exclude rows with placeholder / invalid dates
debut5 = df[['Group', 'Debut Year']].groupby(['Debut Year']).nunique()['Group']
debut5.rename('Group count', inplace = True)

# %%
fig_debut5 = px.bar(debut5, x = debut5.index, y = 'Group count', 
                    title = 'Number of debuted K-Pop groups per year', color = 'Group count')

fig_debut5.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    )
)

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

# %% [markdown]
# 3. Pie chart: idol's country of origin distribution

# %%
# Group by Country and relabel countries with few counts
meta3 = df.groupby(['Country']).count()['Full Name']
meta3.rename('Idol count', inplace = True)
meta3.index = np.where(meta3 < 3, 'Other countries', meta3.index)
meta3.index.name = 'Country / region of origin'

# %%
fig_meta3 = px.pie(meta3, values = 'Idol count', names = meta3.index, 
                   title = 'Country / region of origin ratio of K-Pop idols')

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
ACTIVE_TAB_STYLE = 'bg-light bg-gradient'
ACTIVE_LABEL_STYLE = 'text-primary fw-bold border border-primary'

# %% [markdown]
# #### Define segments of layout below

# %%
layout_home = html.Div([
    html.H1('K-Pop Data Visualisations', className='mt-5 mb-2 mx-2 bg-primary bg-opacity-50 text-dark rounded'),
    html.P(
        "This is a personal project on building a K-Pop themed dashboard using Dash. I do not own any data used in this analysis.",
        className='mx-2'
    ),
    html.A(
        'Find data source here', 
        href='https://www.kaggle.com/datasets/nicolsalayoarias/all-kpop-idols/?select=kpopidolsv3.csv', 
        className='mb-4 mx-2'
    ),
])

# %%
layout_birthday = html.Div([
    html.H2('Idol Birthday Analysis', className=H2_STYLE),
    html.Div([
        html.H3('Idol birth year distribution', className=H3_STYLE),
        dbc.Tabs(id="tabs-birth-year", active_tab='overall-birth-year', class_name='mx-2', children=[
            dbc.Tab(
                    label='Overall', 
                    tab_id='overall-birth-year', 
                    class_name=TAB_STYLE, 
                    activeTabClassName=ACTIVE_TAB_STYLE, 
                    activeLabelClassName=ACTIVE_LABEL_STYLE
                ),
            dbc.Tab(
                    label='Male / Female', 
                    tab_id='splitted-birth-year', 
                    class_name=TAB_STYLE, 
                    activeTabClassName=ACTIVE_TAB_STYLE, 
                    activeLabelClassName=ACTIVE_LABEL_STYLE
                ),
        ]),
        html.Div(id='tabs-content-birth-year')
    ]),
    html.Div([
        html.H3('Idol birth month distribution', className=H3_STYLE),
        dbc.Tabs(id="tabs-birth-month", active_tab='overall-birth-month', class_name='mx-2', children=[
            dbc.Tab(
                    label='Overall', 
                    tab_id='overall-birth-month', 
                    class_name=TAB_STYLE, 
                    activeTabClassName=ACTIVE_TAB_STYLE, 
                    activeLabelClassName=ACTIVE_LABEL_STYLE
                ),
            dbc.Tab(
                    label='Male / Female', 
                    tab_id='splitted-birth-month', 
                    class_name=TAB_STYLE, 
                    activeTabClassName=ACTIVE_TAB_STYLE, 
                    activeLabelClassName=ACTIVE_LABEL_STYLE
                ),
        ]),
        html.Div(id='tabs-content-birth-month')
    ]),
])

# %%
layout_debut = html.Div([
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
])

# %%
layout_meta = html.Div([
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

# %%
layout_interactive = html.Div([
    html.H2('Interactive analysis', className=H2_STYLE),
    html.Div([
        html.H3('List of foreign idols', className=H3_STYLE),
        dcc.Dropdown(
            id='dropdown-foreign', 
            options=sorted([i for i in list(df["Country"].unique()) if i != "South Korea"]), 
            searchable=True,
            placeholder='Select a country / region...',
            className='mx-4'
        ),
        html.Div(id='dropdown-content-foreign')
    ]),
    html.Div([
        html.H3('List of groups by alphabet', className=H3_STYLE),
        dcc.Dropdown(
            id='dropdown-alphabet', 
            options=list(i.upper() for i in map(chr, range(ord('a'), ord('z')+1))) + ["Others"], # generate alphabets A-Z in a list
            searchable=True,
            placeholder='Select an alphabet...',
            className='mx-4'
        ),
        html.Div(id='dropdown-content-alphabet')
    ])
])

# %% [markdown]
# #### Define sidebar layout

# %%
# Define sidebar styling
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Define padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# %%
sidebar = html.Div(
    [
        html.H2("Contents", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Birthday analysis", href="/page-1", active="exact"),
                dbc.NavLink("Debut analysis", href="/page-2", active="exact"),
                dbc.NavLink("Meta-analysis", href="/page-3", active="exact"),
                dbc.NavLink("Interactive", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div([
            html.P(children=["© ", html.A("SY Lee", href='https://github.com/seenyanlee')], className='ms-2 position-absolute bottom-0')
        ])
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# %% [markdown]
# #### Combine dashboard layout and define callback functions

# %%
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

# Render sidebar
@callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return layout_home
    elif pathname == "/page-1":
        return layout_birthday
    elif pathname == "/page-2":
        return layout_debut
    elif pathname == "/page-3":
        return layout_meta
    elif pathname == "/page-4":
        return layout_interactive
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Render tabs for birth year analysis
@callback(Output('tabs-content-birth-year', 'children'), Input('tabs-birth-year', 'active_tab'))
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
@callback(Output('tabs-content-birth-month', 'children'), Input('tabs-birth-month', 'active_tab'))
def render_content(tab):
    if tab == 'overall-birth-month':
        return html.Div([
            dcc.Graph(figure=fig_bday3, className='mx-2')
        ])
    elif tab == 'splitted-birth-month':
        return html.Div([
            dcc.Graph(figure=fig_bday3a, className='mx-2')
        ])
    
# Render dropdown menu for list of foreign idols
@callback(Output('dropdown-content-foreign', 'children'), Input('dropdown-foreign', 'value'))
def update_output(value):
    return dbc.Table.from_dataframe(df[df["Country"] == value][["Stage Name", "Group"]], hover=True, class_name='mx-4')

# Render dropdown menu for list of groups
@callback(Output('dropdown-content-alphabet', 'children'), Input('dropdown-alphabet', 'value'))
def update_output(value):
    sr_group = df["Group"].dropna()
    if value != "Others":
        return dbc.Table.from_dataframe(pd.DataFrame(sr_group[sr_group.str.startswith(str(value))]
                                                        .sort_values(key=lambda col: col.str.lower())
                                                        .unique(),
                                                     columns=["Group names"]),
                                        hover=True,
                                        class_name='mx-4')
    elif value == "Others":
        return dbc.Table.from_dataframe(pd.DataFrame(sr_group[sr_group < "A"]
                                                        .sort_values(key=lambda col: col.str.lower())
                                                        .unique(),
                                                     columns=["Group names"]),
                                        hover=True,
                                        class_name='mx-4')
 

# %% [markdown]
# ### Run dashboard 

# %%
if __name__ == '__main__':
    app.run(debug = True)


