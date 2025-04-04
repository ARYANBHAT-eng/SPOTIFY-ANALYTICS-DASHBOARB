import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ========== THEME SETUP ==========
THEMES = {
    'dark': {
        'background': '#0E0E0E',
        'card': '#191414',
        'primary': '#1DB954',
        'secondary': '#1ED760',
        'text': '#FFFFFF',
        'muted': '#B3B3B3',
        'positive': '#1DB954',
        'negative': '#FF5733'
    },
    'light': {
        'background': '#F8F9FA',
        'card': '#FFFFFF',
        'primary': '#1DB954',
        'secondary': '#1ED760',
        'text': '#191414',
        'muted': '#6C757D',
        'positive': '#28A745',
        'negative': '#DC3545'
    }
}

FONT_FAMILY = "'Circular', 'Helvetica Neue', Helvetica, Arial, sans-serif"
TITLE_STYLE = {
    'font-family': FONT_FAMILY,
    'font-weight': 'bold',
    'letter-spacing': '-0.5px'
}

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ========== DATA LOADING ==========
def load_data():
    """Load data from the 20k songs CSV file"""
    try:
        df = pd.read_csv('indian_music_20k.csv', parse_dates=['release_date'])
        
        # Ensure proper data types
        df['explicit'] = df['explicit'].astype(bool)
        
        # Create duration in minutes if not present
        if 'duration_min' not in df.columns and 'duration_ms' in df.columns:
            df['duration_min'] = df['duration_ms'] / 60000
            
        print(f"Successfully loaded dataset with {len(df)} songs")
        return df
    
    except Exception as e:
        print(f"Error loading dataset: {e}")
        # Fallback to empty dataframe with expected columns
        return pd.DataFrame(columns=[
            'name', 'artist', 'popularity', 'duration_min', 'danceability',
            'energy', 'speechiness', 'acousticness', 'valence', 'explicit',
            'artist_genres', 'release_date', 'image_url', 'mood'
        ])

# Load data
df = load_data()

# ========== UI COMPONENTS ==========
def create_kpi_card(title, value, delta=None, id=None, theme='dark'):
    """Create a KPI card with optional delta indicator"""
    theme_data = THEMES[theme]
    return dbc.Card([
        dbc.CardBody([
            html.H6(title, style={
                'color': theme_data['muted'],
                'font-family': FONT_FAMILY,
                'margin-bottom': '5px'
            }),
            html.H3(value if id is None else html.Div(id=id), style={
                'color': theme_data['text'],
                'font-family': FONT_FAMILY,
                'margin': '10px 0'
            }),
            html.Small([
                html.I(className="fas fa-arrow-up") if delta and delta > 0 else 
                html.I(className="fas fa-arrow-down") if delta and delta < 0 else "",
                f" {abs(delta)}%" if delta else ""
            ], style={
                'color': theme_data['positive'] if delta and delta > 0 else 
                        theme_data['negative'] if delta and delta < 0 else 
                        theme_data['muted']
            })
        ])
    ], style={
        'borderRadius': '12px',
        'backgroundColor': theme_data['card'],
        'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
        'height': '100%',
        'padding': '15px'
    })

def create_track_preview(image_url, track_name, artist, preview_url, theme):
    """Create track preview component"""
    theme_data = THEMES[theme]
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Img(
                    src=image_url,
                    style={
                        'width': '80px',
                        'height': '80px',
                        'borderRadius': '4px',
                        'marginRight': '15px',
                        'objectFit': 'cover'
                    }
                ),
                html.Div([
                    html.H5(track_name, style={
                        'marginBottom': '5px',
                        'color': theme_data['text'],
                        'fontFamily': FONT_FAMILY
                    }),
                    html.P(artist, style={
                        'color': theme_data['muted'],
                        'marginBottom': '10px',
                        'fontFamily': FONT_FAMILY
                    }),
                    html.Audio(
                        src=preview_url,
                        controls=True,
                        style={'width': '100%'}
                    ) if preview_url else html.P(
                        "Preview not available",
                        style={
                            'color': theme_data['muted'],
                            'fontFamily': FONT_FAMILY
                        }
                    )
                ], style={'flex': 1})
            ], style={
                'display': 'flex',
                'alignItems': 'center'
            })
        ])
    ], style={
        'marginBottom': '15px',
        'backgroundColor': theme_data['card'],
        'borderRadius': '12px'
    })

# ========== APP LAYOUT ==========
app.layout = html.Div([
    dcc.Store(id='theme-store', data='dark'),
    dcc.Loading(id="loading-spinner", type="circle", fullscreen=True),
    
    # Main container
    html.Div([
        # Header with theme toggle
        dbc.Row([
            dbc.Col([
                html.H1("Spotify India Analytics", style={
                    **TITLE_STYLE,
                    'font-size': '2.5rem',
                    'background': 'linear-gradient(90deg, #1DB954, #1ED760)',
                    '-webkit-background-clip': 'text',
                    '-webkit-text-fill-color': 'transparent',
                    'margin-bottom': '0'
                }),
                html.P("Explore trends across 20,000 Indian songs", style={
                    'color': THEMES['dark']['muted'],
                    'font-family': FONT_FAMILY,
                    'margin-top': '5px'
                })
            ], md=10),
            dbc.Col([
                dbc.Switch(
                    id='theme-toggle',
                    label="Dark Mode",
                    value=True,
                    style={'float': 'right'},
                    label_style={'font-family': FONT_FAMILY}
                )
            ], md=2)
        ], className="mb-4"),
        
        # KPI Row
        dbc.Row([
            dbc.Col(create_kpi_card("Total Tracks", len(df), id='kpi-total-tracks'), md=2),
            dbc.Col(create_kpi_card("Avg Popularity", round(df['popularity'].mean(), 1), id='kpi-avg-popularity'), md=2),
            dbc.Col(create_kpi_card("Avg Duration", f"{round(df['duration_min'].mean(), 1)} min", id='kpi-avg-duration'), md=2),
            dbc.Col(create_kpi_card("Top Genre", df['artist_genres'].str.split(', ').explode().value_counts().index[0], id='kpi-top-genre'), md=2),
            dbc.Col(create_kpi_card("Explicit %", f"{round(df['explicit'].mean()*100, 1)}%", id='kpi-explicit-pct'), md=2),
            dbc.Col(create_kpi_card("Energy Index", round(df['energy'].mean()*100, 1), id='kpi-energy-index'), md=2),
        ], className="mb-4"),
        
        # Main content
        dbc.Row([
            # Filters column
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters", style={
                        'font-family': FONT_FAMILY,
                        'font-weight': 'bold',
                        'color': THEMES['dark']['primary'],
                        'border-bottom': f'1px solid {THEMES["dark"]["muted"]}'
                    }),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Artists", style={'font-family': FONT_FAMILY}),
                                dcc.Dropdown(
                                    id='artist-dropdown',
                                    options=[{'label': a, 'value': a} for a in sorted(df['artist'].unique())],
                                    multi=True,
                                    placeholder="All Artists",
                                    style={'font-family': FONT_FAMILY}
                                )
                            ], md=6),
                            dbc.Col([
                                html.Label("Genres", style={'font-family': FONT_FAMILY}),
                                dcc.Dropdown(
                                    id='genre-dropdown',
                                    options=[{'label': g, 'value': g} for g in sorted(set(g for sublist in df['artist_genres'].str.split(', ') for g in sublist))],
                                    multi=True,
                                    placeholder="All Genres",
                                    style={'font-family': FONT_FAMILY}
                                )
                            ], md=6)
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Audio Features", style={'font-family': FONT_FAMILY}),
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    options=[
                                        {'label': 'Danceability', 'value': 'danceability'},
                                        {'label': 'Energy', 'value': 'energy'},
                                        {'label': 'Speechiness', 'value': 'speechiness'},
                                        {'label': 'Acousticness', 'value': 'acousticness'},
                                        {'label': 'Valence', 'value': 'valence'}
                                    ],
                                    value=['danceability', 'energy'],
                                    multi=True,
                                    style={'font-family': FONT_FAMILY}
                                )
                            ])
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Release Date Range", style={'font-family': FONT_FAMILY}),
                                dcc.DatePickerRange(
                                    id='date-range',
                                    min_date_allowed=df['release_date'].min(),
                                    max_date_allowed=df['release_date'].max(),
                                    start_date=df['release_date'].min(),
                                    end_date=df['release_date'].max(),
                                    display_format='YYYY-MM-DD'
                                )
                            ])
                        ]),
                        html.Br(),
                        dbc.Button(
                            "Apply Filters",
                            id='apply-button',
                            color="primary",
                            className="w-100",
                            style={'borderRadius': '50px'}
                        )
                    ])
                ], style={
                    'borderRadius': '12px',
                    'backgroundColor': THEMES['dark']['card'],
                    'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
                    'height': '100%'
                })
            ], md=3),
            
            # Visualizations column
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Top Tracks by Popularity", style={
                                'font-family': FONT_FAMILY,
                                'font-weight': 'bold',
                                'color': THEMES['dark']['primary'],
                                'border-bottom': f'1px solid {THEMES["dark"]["muted"]}'
                            }),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='top-tracks-chart',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], style={
                            'borderRadius': '12px',
                            'backgroundColor': THEMES['dark']['card'],
                            'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
                            'height': '100%'
                        })
                    ], md=12, className="mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Audio Features Radar", style={
                                    'font-family': FONT_FAMILY,
                                    'font-weight': 'bold',
                                    'color': THEMES['dark']['primary'],
                                    'border-bottom': f'1px solid {THEMES["dark"]["muted"]}'
                                }),
                                dbc.CardBody([
                                    dcc.Graph(
                                        id='features-radar',
                                        config={'displayModeBar': False}
                                    )
                                ])
                            ], style={
                                'borderRadius': '12px',
                                'backgroundColor': THEMES['dark']['card'],
                                'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
                                'height': '100%'
                            })
                        ], md=6, className="mb-4"),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Mood Analysis", style={
                                    'font-family': FONT_FAMILY,
                                    'font-weight': 'bold',
                                    'color': THEMES['dark']['primary'],
                                    'border-bottom': f'1px solid {THEMES["dark"]["muted"]}'
                                }),
                                dbc.CardBody([
                                    dcc.Graph(
                                        id='mood-chart',
                                        config={'displayModeBar': False}
                                    )
                                ])
                            ], style={
                                'borderRadius': '12px',
                                'backgroundColor': THEMES['dark']['card'],
                                'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
                                'height': '100%'
                            })
                        ], md=6, className="mb-4")
                    ]),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Track Previews", style={
                                    'font-family': FONT_FAMILY,
                                    'font-weight': 'bold',
                                    'color': THEMES['dark']['primary'],
                                    'border-bottom': f'1px solid {THEMES["dark"]["muted"]}'
                                }),
                                dbc.CardBody([
                                    html.Div(id='track-preview-container')
                                ])
                            ], style={
                                'borderRadius': '12px',
                                'backgroundColor': THEMES['dark']['card'],
                                'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
                                'height': '100%'
                            })
                        ], md=12)
                    ])
                ])
            ], md=9)
        ])
    ], id='main-container', style={
        'backgroundColor': THEMES['dark']['background'],
        'color': THEMES['dark']['text'],
        'fontFamily': FONT_FAMILY,
        'minHeight': '100vh',
        'padding': '20px'
    })
])

# ========== CALLBACKS ==========
@app.callback(
    Output('theme-store', 'data'),
    Input('theme-toggle', 'value')
)
def update_theme(dark_mode):
    return 'dark' if dark_mode else 'light'

@app.callback(
    Output('main-container', 'style'),
    Output('theme-toggle', 'label'),
    Input('theme-store', 'data')
)
def apply_theme(theme):
    theme_data = THEMES[theme]
    container_style = {
        'backgroundColor': theme_data['background'],
        'color': theme_data['text'],
        'fontFamily': FONT_FAMILY,
        'minHeight': '100vh',
        'padding': '20px'
    }
    toggle_label = "Dark Mode" if theme == 'dark' else "Light Mode"
    return container_style, toggle_label

@app.callback(
    Output('top-tracks-chart', 'figure'),
    Output('features-radar', 'figure'),
    Output('mood-chart', 'figure'),
    Output('track-preview-container', 'children'),
    Output('kpi-total-tracks', 'children'),
    Output('kpi-avg-popularity', 'children'),
    Output('kpi-avg-duration', 'children'),
    Output('kpi-top-genre', 'children'),
    Output('kpi-explicit-pct', 'children'),
    Output('kpi-energy-index', 'children'),
    Input('apply-button', 'n_clicks'),
    State('artist-dropdown', 'value'),
    State('genre-dropdown', 'value'),
    State('feature-dropdown', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    State('theme-store', 'data')
)
def update_dashboard(n_clicks, artists, genres, features, start_date, end_date, theme):
    # Filter data
    filtered_df = df.copy()
    
    # Apply filters
    if artists:
        filtered_df = filtered_df[filtered_df['artist'].isin(artists)]
    if genres:
        genre_mask = filtered_df['artist_genres'].apply(lambda x: any(g in x for g in genres))
        filtered_df = filtered_df[genre_mask]
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['release_date'] >= start_date) & 
            (filtered_df['release_date'] <= end_date)
        ]
    
    theme_data = THEMES[theme]
    
    # 1. Top Tracks Chart
    top_tracks_fig = px.bar(
        filtered_df.nlargest(10, 'popularity'),
        x='name', y='popularity', color='artist',
        template='plotly_dark' if theme == 'dark' else 'plotly_white',
        hover_data=['duration_min', 'artist_genres']
    ).update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': FONT_FAMILY},
        margin={'t': 0},
        xaxis={'title': None, 'categoryorder': 'total descending'},
        yaxis={'title': None},
        legend={'orientation': 'h', 'y': -0.2}
    )
    
    # 2. Features Radar Chart
    features_fig = go.Figure()
    if features:
        avg_features = filtered_df[features].mean()
        features_fig.add_trace(go.Scatterpolar(
            r=avg_features.values,
            theta=features,
            fill='toself',
            line_color=theme_data['primary']
        ))
    features_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': FONT_FAMILY},
        margin={'t': 0},
        showlegend=False
    )
    
    # 3. Mood Chart
    mood_fig = px.pie(
        filtered_df,
        names='mood',
        hole=0.4,
        color_discrete_sequence=[
            theme_data['muted'], 
            theme_data['primary'], 
            theme_data['secondary']
        ]
    ).update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': FONT_FAMILY},
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # 4. Track Previews
    previews = []
    for _, row in filtered_df.nlargest(3, 'popularity').iterrows():
        previews.append(create_track_preview(
            row['image_url'],
            row['name'],
            row['artist'],
            row['preview_url'],
            theme
        ))
    
    # 5. Calculate KPIs
    total_tracks = len(filtered_df)
    avg_popularity = round(filtered_df['popularity'].mean(), 1)
    avg_duration = f"{round(filtered_df['duration_min'].mean(), 1)} min"
    
    # Get top genre
    genre_list = filtered_df['artist_genres'].str.split(', ').explode()
    top_genre = genre_list.value_counts().index[0] if not genre_list.empty else "N/A"
    
    # Explicit content percentage
    explicit_pct = round((filtered_df['explicit'].mean() * 100), 1)
    
    # Energy index (custom metric)
    energy_index = round(filtered_df['energy'].mean() * 100, 1)
    
    return (
        top_tracks_fig,
        features_fig,
        mood_fig,
        previews,
        total_tracks,
        avg_popularity,
        avg_duration,
        top_genre,
        f"{explicit_pct}%",
        f"{energy_index}"
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)