import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Video Game Analytics Dashboard",
    page_icon="🎮",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

games = pd.read_csv("cleaned_games.csv")
sales = pd.read_csv("cleaned_vgsales.csv")
merged = pd.read_csv("merged_games_sales.csv")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🎮 Dashboard Filters")

genre_filter = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + sorted(sales['Genre'].dropna().unique().tolist())
)

platform_filter = st.sidebar.selectbox(
    "Select Platform",
    ["All"] + sorted(sales['Platform'].dropna().unique().tolist())
)

# ==================================================
# APPLY FILTERS
# ==================================================

filtered_sales = sales.copy()

if genre_filter != "All":
    filtered_sales = filtered_sales[
        filtered_sales['Genre'] == genre_filter
    ]

if platform_filter != "All":
    filtered_sales = filtered_sales[
        filtered_sales['Platform'] == platform_filter
    ]

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Video Game Analytics Dashboard
    
    Built using:
    - Python
    - Streamlit
    - SQL
    - Plotly
    """
)

# ==================================================
# TITLE
# ==================================================

st.title("🎮 Video Game Sales & Engagement Dashboard")

st.markdown(
    "Interactive dashboard for analyzing game sales, ratings, platforms, publishers, and engagement trends."
)

st.markdown("---")

# ==================================================
# KPI SECTION
# ==================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Games",
    f"{len(filtered_sales):,}"
)

col2.metric(
    "Global Sales",
    f"{filtered_sales['Global_Sales'].sum():,.2f} M"
)

col3.metric(
    "Average Rating",
    round(games['Rating'].mean(), 2)
)

col4.metric(
    "Total Wishlist",
    f"{games['Wishlist'].sum():,.0f}"
)

st.markdown("---")

# ==================================================
# TOP ROW CHARTS
# ==================================================

col1, col2 = st.columns(2)

# TOP RATED GAMES

with col1:

    st.subheader("⭐ Top Rated Games")

    top_rated = games[
        ['Title', 'Rating']
    ].sort_values(
        by='Rating',
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_rated,
        x='Rating',
        y='Title',
        orientation='h',
        height=450,
        color='Rating'
    )

    st.plotly_chart(fig1, use_container_width=True)

# PLATFORM SALES

with col2:

    st.subheader("🎮 Best Selling Platforms")

    platform_sales = filtered_sales.groupby(
        'Platform'
    )['Global_Sales'].sum().reset_index()

    platform_sales = platform_sales.sort_values(
        by='Global_Sales',
        ascending=False
    ).head(10)

    fig2 = px.bar(
        platform_sales,
        x='Platform',
        y='Global_Sales',
        height=450,
        color='Global_Sales'
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==================================================
# SECOND ROW
# ==================================================

col3, col4 = st.columns(2)

# PIE CHART

with col3:

    st.subheader("🌍 Regional Sales Share")

    regional_sales = pd.DataFrame({
        'Region': ['NA', 'EU', 'JP', 'Other'],
        'Sales': [
            filtered_sales['NA_Sales'].sum(),
            filtered_sales['EU_Sales'].sum(),
            filtered_sales['JP_Sales'].sum(),
            filtered_sales['Other_Sales'].sum()
        ]
    })

    fig3 = px.pie(
        regional_sales,
        names='Region',
        values='Sales',
        hole=0.4,
        height=450
    )

    st.plotly_chart(fig3, use_container_width=True)

# GENRE SALES

with col4:

    st.subheader("🧩 Genre Sales Analysis")

    genre_sales = filtered_sales.groupby(
        'Genre'
    )['Global_Sales'].sum().reset_index()

    genre_sales = genre_sales.sort_values(
        by='Global_Sales',
        ascending=False
    )

    fig4 = px.bar(
        genre_sales,
        x='Genre',
        y='Global_Sales',
        color='Global_Sales',
        height=450
    )

    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ==================================================
# SCATTERPLOT
# ==================================================

st.subheader("📈 Wishlist vs Global Sales")

sample_merged = merged.sample(1000)

fig5 = px.scatter(
    sample_merged,
    x='Wishlist',
    y='Global_Sales',
    color='Genre',
    hover_data=['Title'],
    height=600
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ==================================================
# HEATMAP
# ==================================================

st.subheader("🔥 Correlation Heatmap")

corr_columns = [
    'Rating',
    'Times Listed',
    'Number of Reviews',
    'Plays',
    'Playing',
    'Backlogs',
    'Wishlist'
]

corr_matrix = games[corr_columns].corr()

fig, ax = plt.subplots(figsize=(10,5))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap='coolwarm',
    linewidths=0.5,
    fmt=".2f",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

# ==================================================
# DATA PREVIEW
# ==================================================

st.subheader("📄 Dataset Preview")

st.dataframe(
    merged.head(20),
    use_container_width=True
)

# ==================================================
# INSIGHTS
# ==================================================

st.subheader("💡 Key Insights")

st.markdown("""
- Adventure and Action genres dominate global sales.
- Highly rated games generally attract larger wishlists.
- Nintendo and Sony platforms contribute heavily to sales.
- North America generates the largest gaming revenue.
- User engagement metrics strongly correlate with ratings and wishlist counts.
""")

st.markdown("---")

st.caption(
    "Created for Video Game Sales and Engagement Analysis Project"
)