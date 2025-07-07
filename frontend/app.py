import dash
from dash import dcc, html
import plotly.express as px
import sys
import os

# Fügt das Projektverzeichnis zum Python-Pfad hinzu, um Backend-Module zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.data_import.readers import load_yaml_markers, load_chat_log_from_txt
from backend.analysis.core import analyze_monthly_scores

# --- Datenverarbeitung ---
# 1. Beispieldaten laden
markers = load_yaml_markers('data/markers.yaml')
chat_df = load_chat_log_from_txt('data/chat.txt')

# 2. Daten analysieren
monthly_scores_df = analyze_monthly_scores(chat_df, markers)

# 3. Plotly-Figur erstellen
fig = px.line(
    monthly_scores_df,
    x='month',
    y='score',
    title='Monatlicher Beziehungs-Score',
    markers=True,
    labels={'month': 'Monat', 'score': 'Score'}
)
fig.update_layout(
    xaxis_title="Monat",
    yaxis_title="Aggregierter Score",
    title_x=0.5,
    template="plotly_white"
)


# --- Dash App-Initialisierung und Layout ---
app = dash.Dash(__name__)
server = app.server
app.title = "Frausar_RePatAl"

app.layout = html.Div(children=[
    html.H1(children='Frausar_RePatAl: Beziehungsanalyse-Dashboard'),
    html.Div(children='Analyse und Visualisierung von Beziehungschroniken.'),
    dcc.Graph(
        id='relationship-score-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True) 