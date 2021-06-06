import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

df = pd.read_csv('train.csv')
df.Pclass = pd.Categorical(df.Pclass)

df.Pclass = df.Pclass.map({1: 'First class', 2: 'Second class', 3: 'Third class'})
df.Embarked = df.Embarked.map({'S':'Southampton', 'C':'Cherbourg', 'Q': 'Queenstown'})

colors = {
    'background': '#4B84B4 ',
    'text': '#DAF7A6',
    'font-size':'30px'
}

class_fig = px.bar(df, 'Pclass', barmode="group", title="The ticket class distribution of passengers")
class_fig.update_traces(marker_color='black')
class_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])


sex_fig = px.bar(df, x='Sex', barmode="group",title="Gender distribution on board")
sex_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])

sex_fig2 = px.bar(df, x='Sex', barmode="group",title="Gender distribution on board")
sex_fig2.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])

sex_fig3 = px.bar(df, x='Sex', barmode="group",title="Gender distribution on board")
sex_fig3.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],font_color=colors['text'])

location_fig = px.bar(df, 'Embarked', barmode="group", title="Where the passengers were seated from")
location_fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
location_fig.update_traces(marker_color='blue')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Visualization on Titanic dataset.',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='This application is made to present \
    the overall picture of passengers on Titanic board ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-size': '30px',

    }),

    html.Div([

        dcc.Graph(
            id='class_fig',
            figure=class_fig,
            style={'width': '50%', 'float': 'left', 'display': 'block', 'background': '#4B84B4'}
        ),
        dcc.Graph(
            id='sex_fig',
            figure=sex_fig,
            style={'width': '50%', 'float': 'left', 'background': '#4B84B4'}
        ),

        html.Div([
            html.Div(children='To see the gender balance between classes change the class', style={
                'textAlign': 'left',
                'color': colors['text'],
                'font-size': '20px',
                'padding-top': '20px',
                'background': '#4B84B4'
            }),

            dcc.Dropdown(
                id='drop1',
                options=[{'label': i, 'value': i} for i in df['Pclass'].unique()],
                style={'border': '5px groove green', 'width': '100px', 'background': '#4B84B4'},
                placeholder='Choose the passenger class',
                value=16,
            ),

            dcc.Graph(id='sex_fig3', figure=sex_fig3, style={'width': '100%', 'float': 'left', 'background': '#4B84B4'})],

            style={'width': '100%', 'float': 'left', 'background': '#4B84B4'}
        )

    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20', 'background': '#4B84B4'}),


    html.Div([

        html.Div(children='Choose the age of the kid to see what is happening in their family', style={
            'textAlign': 'left',
            'color': colors['text'],
            'font-size': '20px',
            'background': '#4B84B4'
        }),

        html.Div([
            dcc.Slider(
                id='class-slider',
                min=df.Age.min(),
                max=df.Age.max(),
                value=df.Age.min(),
                marks={str(age): str(age) for age in df['Age'].unique()},
                step=None)
        ], style={'border': '5px groove red', 'width': '40%', 'padding-top': '20px', 'background': '#4B84B4'}),

        dcc.Graph(id='sex_fig2', figure=sex_fig2, style={'width': '50%', 'float': 'left', 'background': '#4B84B4'}),

        html.Div([
            dcc.Graph(
                id='location_fig',
                figure=location_fig,
                style={'padding-left': '10%', 'width': '60%', 'background': '#4B84B4'})
        ], style={'width': '50%', 'float': 'right'})

    ], style={'width': '100%', 'float': 'left', 'background': '#4B84B4'}),
])

@app.callback(
    dash.dependencies.Output('sex_fig2', 'figure'),
    [dash.dependencies.Input('class-slider', 'value')])

def update_graph(new_value):
    filt_df = df[df.Age == new_value]
    fig = px.bar(filt_df, 'Sex', color='Pclass')

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        transition_duration=100
    )

    return fig


@app.callback(
    dash.dependencies.Output('sex_fig3', 'figure'),
    [dash.dependencies.Input('drop1', 'value')]
)
def update_graph(new_value):
    filt_df = df[df.Pclass == new_value]
    fig = px.bar(filt_df, 'Sex', color='Pclass', barmode="group")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        transition_duration=1)
    return fig

app.run_server()