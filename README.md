# 📈 Stock Price Explorer

An interactive Streamlit app for comparing normalized stock prices of big tech companies since Jan 2018.

## Features

- Select any combination of AAPL, MSFT, GOOG, AMZN, NFLX, META from the sidebar
- Per-stock growth metrics with delta indicators
- 🏆 Top performer highlight
- 💡 Did you know? fun fact
- Interactive Plotly line chart

## Architecture

![Architecture diagram](https://mermaid.ink/img/pako:eNpNj71OwzAUhXeewkoXkEgJadOmHZCapIKBAYGY2g6uc01DTWzZDm1Ql4oZARMwsfAQPA8vAI-Ak_7F47nf-Y5MGZ-RCZYanV_uIfN6A-vv8-3x9_sZXTCuWY6CLGHaTtJheqU5maIIa6xAWyNk2ycLS8zrsUnqqjiq_QNrgYLC8fKEsBB1kRc9CfiOJRr1hLBG5U6wat-YUGRqYlph2fpAp4k-y8bDVGGJlcC3D1jaREt2VC7YMBeMS5BrT7jy4ExzOwZzyo0qGlg_78viD7vpkPEsXpeiVUmBvAdl-H4x_fqFrk0yTAPJZ6ocKGGlcwaoh2jCWLdGHdqk9FBpyafQrTVxi2KvwgUbjoJPyJYDpz12nAoXrjnwqQedLedCO264FS7a-Ag0YecjLdd3_QrX33AN8Ki35Vr4eNzB_51vofA)

The Plotly built-in stock dataset flows into the Streamlit app, which is version-controlled on GitHub and auto-deployed to Streamlit Cloud for users to access in their browser.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live app

[https://stock-explorer-myngfytmxubcyrnemegp89.streamlit.app/](https://stock-explorer-myngfytmxubcyrnemegp89.streamlit.app/)
