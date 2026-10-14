"""Interactive dashboard for SpaceX launch outcomes."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
candidates = [DATA_DIR / "spacex_launch_dash.csv", DATA_DIR / "dataset_part_2.csv"]
csv_path = next((p for p in candidates if p.exists()), None)
if csv_path is None:
    raise FileNotFoundError("Run `python src/download_data.py` first, or add spacex_launch_dash.csv to data/.")

df = pd.read_csv(csv_path)
# Normalize common course column names.
site_col = next((c for c in ["Launch Site", "LaunchSite", "launch_site"] if c in df.columns), None)
payload_col = next((c for c in ["Payload Mass (kg)", "PayloadMass", "payload_mass_kg"] if c in df.columns), None)
class_col = next((c for c in ["class", "Class", "LandingOutcome"] if c in df.columns), None)
if site_col is None:
    raise ValueError(f"Could not identify launch-site column in {list(df.columns)}")
if class_col is None:
    raise ValueError(f"Could not identify landing outcome column in {list(df.columns)}")

sites = ["All sites"] + sorted(df[site_col].dropna().astype(str).unique().tolist())
app = Dash(__name__)
app.layout = html.Div([
    html.H1("SpaceX Falcon 9 Launch Outcomes"),
    html.Label("Launch site"),
    dcc.Dropdown(sites, value="All sites", id="site", clearable=False),
    html.Div(id="summary"),
    dcc.Graph(id="outcomes"),
    html.Label("Payload mass (kg)"),
    dcc.RangeSlider(
        min=float(df[payload_col].min()) if payload_col else 0,
        max=float(df[payload_col].max()) if payload_col else 1,
        step=100,
        value=[float(df[payload_col].min()), float(df[payload_col].max())] if payload_col else [0, 1],
        id="payload-range",
        tooltip={"placement": "bottom", "always_visible": False},
    ) if payload_col else html.P("Payload column is not available in this dataset."),
], style={"maxWidth": "1100px", "margin": "30px auto", "fontFamily": "Arial"})

@app.callback(
    Output("summary", "children"),
    Output("outcomes", "figure"),
    Input("site", "value"),
    *([Input("payload-range", "value")] if payload_col else []),
)
def update(site, *args):
    filtered = df.copy()
    if site != "All sites":
        filtered = filtered[filtered[site_col].astype(str) == site]
    if payload_col and args:
        lo, hi = args[0]
        filtered = filtered[filtered[payload_col].between(lo, hi)]
    counts = filtered[class_col].astype(str).value_counts().rename_axis("Outcome").reset_index(name="Launches")
    figure = px.bar(counts, x="Outcome", y="Launches", title="Launches by landing outcome")
    return f"Records shown: {len(filtered)}", figure

if __name__ == "__main__":
    app.run(debug=True)
