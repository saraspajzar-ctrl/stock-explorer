import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Stock Explorer", layout="wide")

# ── Design system ─────────────────────────────────────────────────────────────
PALETTE = ["#FF9A86", "#FFB399", "#FFD6A6", "#FFF0BE", "#FF8A72", "#FFCA8F"]

JOURNEY_DIAGRAM = """
journey
    title A Morning With the Stock Explorer
    section Explore
      Pick the stocks I follow: 5: Analyst
      Zoom into the 2018 crash: 4: Analyst
    section Compare
      Find who recovered fastest: 5: Analyst
      See who bounced around most: 3: Analyst
    section Decide
      Ask what if I had invested: 4: Analyst
      Read the real dollar outcome: 5: Analyst
    section Reflect
      Match events to price dips: 4: Analyst
"""

def mermaid_component(diagram: str, height: int = 420) -> None:
    html = f"""
    <div style="background:#FFF8F2;border:1px solid #FFD6A6;border-radius:12px;
                padding:1.25rem 1.5rem;overflow-x:auto;width:100%;box-sizing:border-box;">
      <div class="mermaid">{diagram}</div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@9.4.3/dist/mermaid.min.js"></script>
    <script>
    (function() {{
      function patchSVG() {{
        var svg = document.querySelector('.mermaid svg');
        if (!svg) return;
        var vb = (svg.getAttribute('viewBox') || '0 0 0 0').split(' ').map(Number);
        if (vb[2] === 0) {{
          var maxX = 0;
          svg.querySelectorAll('*').forEach(function(el) {{
            try {{
              var b = el.getBBox();
              if (b.x + b.width > maxX) maxX = b.x + b.width;
            }} catch(e) {{}}
          }});
          var w = maxX > 20 ? maxX + 80 : 700;
          svg.setAttribute('viewBox', vb[0] + ' ' + vb[1] + ' ' + w + ' ' + vb[3]);
          svg.setAttribute('width', '100%');
          if (vb[3]) svg.setAttribute('height', vb[3]);
        }}
      }}

      function init() {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'base',
          themeVariables: {{
            fillType0: '#FF9A86',
            fillType1: '#FFB399',
            fillType2: '#FFD6A6',
            fillType3: '#FFF0BE',
            fillType4: '#FF8A72',
            fillType5: '#FFCA8F',
            fillType6: '#FFD6A6',
            fillType7: '#FFB399',
            primaryColor: '#FF9A86',
            primaryTextColor: '#3B1F1A',
            primaryBorderColor: '#FF8A72',
            lineColor: '#FF9A86',
            secondaryColor: '#FFD6A6',
            tertiaryColor: '#FFF0BE',
            background: '#FFF8F2',
            fontFamily: 'sans-serif',
          }},
          gantt: {{
            useWidth: 700,
            barHeight: 22,
            barGap: 6,
            topPadding: 55,
            sidePadding: 50,
            axisFormat: "%b '%y"
          }}
        }});
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        setTimeout(patchSVG, 300);
        setTimeout(patchSVG, 800);
      }}

      if (document.readyState === 'complete') {{
        requestAnimationFrame(init);
      }} else {{
        window.addEventListener('load', function() {{ requestAnimationFrame(init); }});
      }}
    }})();
    </script>
    """
    components.html(html, height=height, scrolling=False)

st.markdown("""
<style>
/* ════════════════════════════════════
   MOBILE FIRST — base styles (all screens)
   ════════════════════════════════════ */

html, body { box-sizing: border-box; }
*, *::before, *::after { box-sizing: inherit; }

[data-testid="stAppViewContainer"] {
    width: 100% !important;
    max-width: 100% !important;
}
.stMain, [data-testid="stMain"] {
    max-width: 100% !important;
    width: 100% !important;
    flex: 1 1 auto !important;
    min-width: 0 !important;
}
.stMainBlockContainer,
[data-testid="stMainBlockContainer"],
.block-container,
[data-testid="block-container"] {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 1rem !important;
}

html, body, [data-testid="stAppViewContainer"] { background: #E6F2DD; }

[data-testid="stSidebar"] {
    background: #B1D3B9;
    border-right: 1px solid #88BDA4;
}
[data-testid="stSidebar"] * { color: #1B2E28 !important; }
[data-testid="stSidebar"] label {
    font-size: 0.72rem;
    letter-spacing: .07em;
    text-transform: uppercase;
    color: #659287 !important;
}

h1 {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -.02em;
    color: #1B2E28 !important;
}
h2, h3 { color: #2a5e4e !important; font-weight: 600 !important; letter-spacing: -.01em; }
h3 { font-size: 0.9rem !important; }
p, li { color: #4a6b5e; }

[data-testid="stTabs"] { margin-top: 0.5rem; }
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #659287 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: .04em;
    border-bottom: 2px solid transparent !important;
    padding: 0.5rem 0.75rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1B2E28 !important;
    border-bottom: 2px solid #659287 !important;
}
[data-testid="stTabsContent"] { padding-top: 1rem !important; }

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #B1D3B9;
    border-radius: 12px;
    padding: 0.75rem 1rem !important;
    box-shadow: 0 1px 3px rgba(101,146,135,0.12);
    margin-bottom: 0.5rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #659287 !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] > div,
[data-testid="stMetricValue"] > div > div,
[data-testid="stMetricValue"] p {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #FF9A86 !important;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] > div { font-size: 0.78rem !important; font-weight: 600; }

[data-testid="column"] {
    width: 100% !important;
    flex: none !important;
    min-width: 100% !important;
    padding: 0.2rem 0 !important;
}

[data-testid="stPlotlyChart"],
.js-plotly-plot { width: 100% !important; overflow-x: auto; }

[data-testid="stCaptionContainer"] { color: #659287 !important; font-size: 0.75rem !important; }
[data-testid="stAlert"] {
    background: #d4ecd9 !important;
    border: 1px solid #88BDA4 !important;
    border-radius: 10px !important;
    color: #2a5e4e !important;
}

hr { border-color: #B1D3B9 !important; margin: 1rem 0 !important; }

[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border-color: #88BDA4 !important;
    color: #1B2E28 !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border-color: #88BDA4 !important;
    border-radius: 8px !important;
    color: #1B2E28 !important;
}

.fun-fact {
    background: linear-gradient(135deg, #FFD6A6 0%, #FFF0BE 100%);
    border: 1px solid #FFB399;
    border-left: 3px solid #FF9A86;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    color: #5C3D2E;
    font-size: 0.82rem;
    line-height: 1.5;
    margin-bottom: 1rem;
}
.fun-fact strong { color: #FF9A86; }

.diagram-label {
    color: #659287;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

@media (min-width: 768px) {
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1.25rem !important;
    }
    h1 { font-size: 1.75rem !important; }
    h3 { font-size: 0.95rem !important; }
    button[data-baseweb="tab"] { font-size: 0.85rem !important; padding: 0.55rem 1rem !important; }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] p { font-size: 1.6rem !important; }
    [data-testid="column"] {
        width: auto !important;
        flex: 1 1 0% !important;
        min-width: 0 !important;
        padding: 0 0.25rem !important;
    }
    [data-testid="stMetric"] { margin-bottom: 0; }
    hr { margin: 1.25rem 0 !important; }
}

@media (min-width: 1024px) {
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"],
    .block-container {
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-top: 1.5rem !important;
    }
    h1 { font-size: 2rem !important; }
    h3 { font-size: 1rem !important; }
    button[data-baseweb="tab"] { font-size: 0.88rem !important; padding: 0.6rem 1.2rem !important; }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] p { font-size: 1.75rem !important; }
    [data-testid="stMetricLabel"] { font-size: 0.7rem !important; }
    hr { margin: 1.5rem 0 !important; }
    .fun-fact { font-size: 0.88rem; padding: 0.9rem 1.1rem; }
    .diagram-label { font-size: 0.82rem; }
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = px.data.stocks()
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()
tickers = [c for c in df.columns if c != "date"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
chosen = st.sidebar.multiselect("Choose stocks", tickers, default=["AAPL", "MSFT", "GOOG"])
if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

min_date = df["date"].min().date()
max_date = df["date"].max().date()
start_date, end_date = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MMM YYYY",
)

investment = st.sidebar.number_input("Investment amount ($)", min_value=1, value=1000, step=100)
calc_stock = st.sidebar.selectbox("Stock for investment calculator", chosen)

# ── Filter & re-index ─────────────────────────────────────────────────────────
mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
dff = df[mask].copy()
if dff.empty:
    st.warning("No data in the selected date range.")
    st.stop()

for t in tickers:
    first = dff[t].iloc[0]
    if first != 0:
        dff[t] = dff[t] / first

# ── Shared chart style ────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,248,242,0.7)",
    font_color="#5C3D2E",
    font_size=11,
    title_font_color="#3B1F1A",
    title_font_size=13,
    legend=dict(bgcolor="rgba(255,248,242,0.85)", bordercolor="#FFD6A6", borderwidth=1),
    xaxis=dict(gridcolor="#FFD6A6", linecolor="#FFB399", zerolinecolor="#FFB399"),
    yaxis=dict(gridcolor="#FFD6A6", linecolor="#FFB399", zerolinecolor="#FFB399"),
    margin=dict(l=8, r=8, t=40, b=8),
)
color_map = {t: PALETTE[i % len(PALETTE)] for i, t in enumerate(chosen)}

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Stock Price Explorer")
st.caption(
    f"Prices re-indexed to 1.00 at {start_date.strftime('%b %Y')} · "
    "each line shows relative growth within the selected window"
)

st.markdown("""
<div class="fun-fact">
<strong>Did you know?</strong>
Microsoft has split its stock <strong>9 times</strong> since its 1986 IPO at $21 per share.
One IPO share has since multiplied into <strong>288 shares</strong> — meaning a $1,000 investment
at the open would be worth over <strong>$6 million today</strong>.
<span style="font-size:0.72rem;color:#4B5563;margin-left:.5rem;">Source: Wikipedia · History of Microsoft</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_diagrams = st.tabs(["Dashboard", "Journey & Timeline"])

# ════════════════════════════════════════
#  TAB 1 — Dashboard
# ════════════════════════════════════════
with tab_dash:

    cols = st.columns(len(chosen))
    for col, t in zip(cols, chosen):
        growth = (dff[t].iloc[-1] - 1) * 100
        col.metric(t, f"{dff[t].iloc[-1]:.2f}×", f"{growth:+.1f}%")

    best = max(chosen, key=lambda t: dff[t].iloc[-1])
    best_growth = (dff[best].iloc[-1] - 1) * 100
    st.metric("Top performer", best, f"+{best_growth:.1f}%")

    st.markdown("---")
    daily_returns = dff[chosen].pct_change().dropna()
    volatility = daily_returns.std() * 100
    most_volatile = volatility.idxmax()

    vcols = st.columns(len(chosen) + 1)
    vcols[0].markdown("**Volatility**\n\n*daily std dev*")
    for col, t in zip(vcols[1:], chosen):
        badge = " *" if t == most_volatile else ""
        col.metric(f"{t}{badge}", f"{volatility[t]:.2f}%")

    st.markdown("---")
    multiplier = dff[calc_stock].iloc[-1]
    final_value = investment * multiplier
    gain = final_value - investment
    gain_pct = (multiplier - 1) * 100
    period_label = f"{start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}"

    st.subheader(f"What if I invested ${investment:,.0f} in {calc_stock}?")
    res_cols = st.columns(3)
    res_cols[0].metric("Period", period_label)
    res_cols[1].metric("Current value", f"${final_value:,.2f}", f"{gain_pct:+.1f}%")
    res_cols[2].metric("Gain / Loss", f"${gain:+,.2f}")

    st.markdown("---")

    chart_col, bar_col = st.columns([3, 2])

    with chart_col:
        fig_line = go.Figure()
        for t in chosen:
            fig_line.add_trace(go.Scatter(
                x=dff["date"], y=dff[t],
                name=t,
                mode="lines",
                line=dict(color=color_map[t], width=2),
                hovertemplate=f"<b>{t}</b>: %{{y:.2f}}×<extra></extra>",
            ))
        fig_line.update_layout(title="Normalized price over time", **CHART_LAYOUT)
        st.plotly_chart(fig_line, use_container_width=True)

    with bar_col:
        growth_pct = [(dff[t].iloc[-1] - 1) * 100 for t in chosen]
        bar_df = pd.DataFrame({"Stock": chosen, "Growth (%)": growth_pct})
        fig_bar = go.Figure(go.Bar(
            x=bar_df["Stock"],
            y=bar_df["Growth (%)"],
            marker_color=[color_map[t] for t in chosen],
            text=[f"{v:.1f}%" for v in growth_pct],
            textposition="outside",
            textfont_color="#5C3D2E",
            hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
        ))
        fig_bar.update_layout(
            title="Total growth by stock",
            yaxis_ticksuffix="%",
            showlegend=False,
            **CHART_LAYOUT,
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ════════════════════════════════════════
#  TAB 2 — Journey & Timeline
# ════════════════════════════════════════
with tab_diagrams:

    st.markdown("""
    <p style="color:#8892A4;font-size:0.88rem;margin-bottom:1.5rem;">
    The <strong style="color:#CBD5E1;">User Journey</strong> maps how a session flows through
    this app. The <strong style="color:#CBD5E1;">market timeline</strong> shows the macro events
    that drove the 2018–2019 price moves visible in the Dashboard charts.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<p class="diagram-label">Market Events 2018 – 2019</p>', unsafe_allow_html=True)

    gantt_df = pd.DataFrame([
        {"Event": "Q1 correction  −10%",    "Start": "2018-02-01", "End": "2018-04-01", "Phase": "Bear Market"},
        {"Event": "US–China trade war",      "Start": "2018-04-01", "End": "2018-07-01", "Phase": "Trade War"},
        {"Event": "Tech sector selloff",     "Start": "2018-10-01", "End": "2018-12-01", "Phase": "Bear Market"},
        {"Event": "December crash  −20%",    "Start": "2018-12-03", "End": "2018-12-24", "Phase": "Bear Market"},
        {"Event": "Fed pauses rate hikes",   "Start": "2019-01-07", "End": "2019-02-07", "Phase": "Recovery"},
        {"Event": "Q1 strong rally",         "Start": "2019-01-15", "End": "2019-04-15", "Phase": "Recovery"},
        {"Event": "Trade war flares up",     "Start": "2019-05-05", "End": "2019-09-01", "Phase": "Trade War"},
        {"Event": "Fed cuts rates ×3",       "Start": "2019-08-01", "End": "2019-11-01", "Phase": "Recovery"},
        {"Event": "New all-time highs",      "Start": "2019-11-01", "End": "2019-12-15", "Phase": "Recovery"},
    ])
    gantt_df["Start"] = pd.to_datetime(gantt_df["Start"])
    gantt_df["End"]   = pd.to_datetime(gantt_df["End"])

    fig_gantt = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="End",
        y="Event",
        color="Phase",
        color_discrete_map={
            "Bear Market": "#FF9A86",
            "Trade War":   "#FFD6A6",
            "Recovery":    "#FFB399",
        },
        title="Major Market Events 2018 – 2019",
        hover_data={"Start": "|%b %d, %Y", "End": "|%b %d, %Y", "Phase": True},
    )
    fig_gantt.update_yaxes(autorange="reversed", categoryorder="total ascending")
    fig_gantt.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,248,242,0.7)",
        font_color="#5C3D2E",
        font_size=11,
        title_font_color="#3B1F1A",
        title_font_size=13,
        legend=dict(bgcolor="rgba(255,248,242,0.85)", bordercolor="#FFD6A6", borderwidth=1, title_text="Phase"),
        height=380,
        margin=dict(l=180, r=20, t=45, b=30),
        xaxis=dict(
            gridcolor="#FFD6A6", linecolor="#FFB399", zerolinecolor="#FFB399",
            tickformat="%b '%y", dtick="M2",
        ),
        yaxis=dict(gridcolor="#FFD6A6", linecolor="#FFB399"),
    )
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.markdown("---")

    st.markdown('<p class="diagram-label">User Journey</p>', unsafe_allow_html=True)
    mermaid_component(JOURNEY_DIAGRAM, height=360)
