import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
#  PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Main background */
        .main { background-color: #f5f7fa; }

        /* Metric card */
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 16px 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
        [data-testid="stMetricLabel"] { font-size: 13px; color: #64748b; font-weight: 600; }
        [data-testid="stMetricValue"] { font-size: 26px; font-weight: 700; color: #1e293b; }
        [data-testid="stMetricDelta"] { font-size: 13px; }

        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, #1e3a5f 0%, #2563eb 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 18px;
            letter-spacing: 0.3px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] { background-color: #1e3a5f; }
        [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        [data-testid="stSidebar"] .stMultiSelect > div { background-color: #2d527a !important; }

        /* Dataframe */
        [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

        /* Expander */
        [data-testid="stExpander"] {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: #ffffff;
        }

        /* Divider */
        hr { border-color: #e2e8f0; margin: 24px 0; }

        /* Alert boxes */
        .info-box {
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 14px;
            color: #1e40af;
            margin-bottom: 12px;
        }
        .success-box {
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 14px;
            color: #15803d;
            margin-bottom: 12px;
        }
        .warning-box {
            background: #fffbeb;
            border-left: 4px solid #d97706;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 14px;
            color: #92400e;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  HELPER: section header
# ─────────────────────────────────────────────
def section(icon: str, title: str):
    st.markdown(
        f'<div class="section-header">{icon}&nbsp;&nbsp;{title}</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  STEP 1 — LOAD DATASET
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


DATA_PATH = os.path.join(os.path.dirname(__file__), "supermarket_sales.csv")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Supermarket Analytics")
    st.markdown("---")

    raw_df = load_data(DATA_PATH)

    # Filters
    st.markdown("### 🔍 Filters")

    branches = st.multiselect(
        "Branch",
        options=sorted(raw_df["Branch"].unique()),
        default=sorted(raw_df["Branch"].unique()),
    )
    cities = st.multiselect(
        "City",
        options=sorted(raw_df["City"].unique()),
        default=sorted(raw_df["City"].unique()),
    )
    categories = st.multiselect(
        "Category",
        options=sorted(raw_df["Category"].unique()),
        default=sorted(raw_df["Category"].unique()),
    )
    customer_types = st.multiselect(
        "Customer Type",
        options=sorted(raw_df["Customer Type"].unique()),
        default=sorted(raw_df["Customer Type"].unique()),
    )
    genders = st.multiselect(
        "Gender",
        options=sorted(raw_df["Gender"].unique()),
        default=sorted(raw_df["Gender"].unique()),
    )

    date_min = raw_df["Date"].min().date()
    date_max = raw_df["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    st.markdown("---")
    st.markdown("### 📄 Dataset Info")
    st.markdown(f"- **Total Records:** {len(raw_df):,}")
    st.markdown(f"- **Columns:** {raw_df.shape[1]}")
    st.markdown(f"- **Date Span:** {date_min} → {date_max}")


# ─────────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────────
df = raw_df.copy()
if len(date_range) == 2:
    start_d, end_d = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["Date"] >= start_d) & (df["Date"] <= end_d)]

df = df[
    df["Branch"].isin(branches)
    & df["City"].isin(cities)
    & df["Category"].isin(categories)
    & df["Customer Type"].isin(customer_types)
    & df["Gender"].isin(genders)
]

# ─────────────────────────────────────────────
#  PAGE TITLE
# ─────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#1e3a5f; font-size:32px; font-weight:800; margin-bottom:4px;'>"
    "🛒 Supermarket Sales Analytics Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#64748b; font-size:15px; margin-bottom:24px;'>"
    "End-to-end analysis: data quality check → sales computation → group summaries → charts → business insights</p>",
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()

# ════════════════════════════════════════════
#  SECTION 1 — LOAD & PREVIEW
# ════════════════════════════════════════════
section("📂", "Step 1 — Load Dataset")

col1, col2, col3 = st.columns(3)
col1.metric("Filtered Records", f"{len(df):,}", f"{len(df) - len(raw_df):,} from total")
col2.metric("Columns", raw_df.shape[1])
col3.metric("Date Range", f"{df['Date'].min().date()} → {df['Date'].max().date()}")

with st.expander("📋 Raw Data Preview (first 20 rows)", expanded=False):
    st.dataframe(
        df.head(20).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

with st.expander("📊 Column Data Types & Sample Values", expanded=False):
    dtype_df = pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Non-Null Count": df.notnull().sum().values,
            "Sample Value": [str(df[c].dropna().iloc[0]) if not df[c].dropna().empty else "N/A" for c in df.columns],
        }
    )
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ════════════════════════════════════════════
#  SECTION 2 — DATA QUALITY CHECK
# ════════════════════════════════════════════
section("🔍", "Step 2 — Data Quality Check")

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
neg_qty = (df["Quantity"] < 0).sum()
neg_price = (df["Unit Price"] < 0).sum()
duplicate_rows = df.duplicated().sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Missing Values", int(missing.sum()))
col2.metric("Duplicate Rows", int(duplicate_rows))
col3.metric("Negative Quantity", int(neg_qty))
col4.metric("Negative Unit Price", int(neg_price))

# Quality verdict
total_issues = int(missing.sum()) + int(duplicate_rows) + int(neg_qty) + int(neg_price)
if total_issues == 0:
    st.markdown('<div class="success-box">✅ <strong>Dataset is clean.</strong> No missing values, duplicates, or invalid numeric entries were found in the filtered data.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warning-box">⚠️ <strong>{total_issues} issue(s) detected.</strong> Review the detail table below.</div>', unsafe_allow_html=True)

with st.expander("🔎 Missing Values Per Column", expanded=total_issues > 0):
    quality_df = pd.DataFrame(
        {
            "Column": missing.index,
            "Missing Count": missing.values,
            "Missing %": missing_pct.values,
            "Status": ["✅ OK" if v == 0 else "❌ Has Nulls" for v in missing.values],
        }
    )
    st.dataframe(quality_df, use_container_width=True, hide_index=True)

with st.expander("📈 Numeric Column Statistics", expanded=False):
    st.dataframe(
        df[["Quantity", "Unit Price", "Sales", "Rating"]].describe().round(2),
        use_container_width=True,
    )

st.markdown("---")

# ════════════════════════════════════════════
#  SECTION 3 — SALES CALCULATION VERIFICATION
# ════════════════════════════════════════════
section("🧮", "Step 3 — Sales = Quantity × Unit Price (Verification)")

# Recalculate and compare
df["Calculated_Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)
df["Sales_Match"] = df["Sales"].round(2) == df["Calculated_Sales"]
match_count = df["Sales_Match"].sum()
mismatch_count = len(df) - match_count

col1, col2, col3 = st.columns(3)
col1.metric("Rows Verified", f"{len(df):,}")
col2.metric("Sales Matches (Qty × Price)", f"{match_count:,}", f"{match_count/len(df)*100:.1f}%")
col3.metric("Mismatches Detected", f"{mismatch_count:,}")

if mismatch_count == 0:
    st.markdown('<div class="success-box">✅ <strong>All Sales values verified.</strong> Every row satisfies Sales = Quantity × Unit Price (rounded to 2 decimal places).</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warning-box">⚠️ <strong>{mismatch_count} row(s)</strong> have a discrepancy between the stored Sales value and Quantity × Unit Price.</div>', unsafe_allow_html=True)
    with st.expander("View Mismatched Rows"):
        st.dataframe(
            df[~df["Sales_Match"]][["Invoice ID", "Quantity", "Unit Price", "Sales", "Calculated_Sales"]],
            use_container_width=True,
            hide_index=True,
        )

with st.expander("📋 Sample: Quantity × Unit Price = Sales", expanded=False):
    sample = df[["Invoice ID", "Quantity", "Unit Price", "Calculated_Sales", "Sales", "Sales_Match"]].head(10)
    sample.columns = ["Invoice ID", "Quantity", "Unit Price", "Qty × Price", "Stored Sales", "Match?"]
    sample["Match?"] = sample["Match?"].map({True: "✅", False: "❌"})
    st.dataframe(sample, use_container_width=True, hide_index=True)

st.markdown("---")

# ════════════════════════════════════════════
#  SECTION 4 — GROUP SUMMARIES
# ════════════════════════════════════════════
section("📊", "Step 4 — Group Summaries (Totals, Counts & Averages)")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📦 By Category", "🏙️ By City", "🏢 By Branch", "💳 By Payment", "👤 By Customer Type"]
)

def summary_table(group_col: str) -> pd.DataFrame:
    grp = (
        df.groupby(group_col)
        .agg(
            Transactions=("Invoice ID", "count"),
            Total_Sales=("Sales", "sum"),
            Avg_Sales=("Sales", "mean"),
            Total_Quantity=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    grp["Total_Sales"] = grp["Total_Sales"].round(2)
    grp["Avg_Sales"] = grp["Avg_Sales"].round(2)
    grp["Avg_Rating"] = grp["Avg_Rating"].round(2)
    grp.columns = [group_col, "Transactions", "Total Sales (₹)", "Avg Sale (₹)", "Total Qty", "Avg Rating"]
    return grp

with tab1:
    t = summary_table("Category")
    st.dataframe(t, use_container_width=True, hide_index=True)
with tab2:
    t = summary_table("City")
    st.dataframe(t, use_container_width=True, hide_index=True)
with tab3:
    t = summary_table("Branch")
    st.dataframe(t, use_container_width=True, hide_index=True)
with tab4:
    t = summary_table("Payment")
    st.dataframe(t, use_container_width=True, hide_index=True)
with tab5:
    t = summary_table("Customer Type")
    st.dataframe(t, use_container_width=True, hide_index=True)

# Monthly trend summary
st.markdown("#### 📅 Monthly Sales Summary")
df["Month"] = df["Date"].dt.to_period("M").astype(str)
monthly = (
    df.groupby("Month")
    .agg(Transactions=("Invoice ID", "count"), Total_Sales=("Sales", "sum"), Avg_Sale=("Sales", "mean"))
    .reset_index()
    .sort_values("Month")
)
monthly["Total_Sales"] = monthly["Total_Sales"].round(2)
monthly["Avg_Sale"] = monthly["Avg_Sale"].round(2)
monthly.columns = ["Month", "Transactions", "Total Sales (₹)", "Avg Sale (₹)"]
st.dataframe(monthly, use_container_width=True, hide_index=True)

st.markdown("---")

# ════════════════════════════════════════════
#  SECTION 5 — CHARTS
# ════════════════════════════════════════════
section("📈", "Step 5 — Visual Analysis")

PALETTE = px.colors.qualitative.Set2

# ── Row 1: Sales by Category  &  Sales by City
col1, col2 = st.columns(2)

with col1:
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig = px.bar(
        cat_sales,
        x="Category",
        y="Sales",
        title="Total Sales by Category",
        color="Category",
        color_discrete_sequence=PALETTE,
        text_auto=".2s",
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Category",
        yaxis_title="Total Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    city_sales = df.groupby("City")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig = px.bar(
        city_sales,
        x="City",
        y="Sales",
        title="Total Sales by City",
        color="City",
        color_discrete_sequence=PALETTE,
        text_auto=".2s",
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="City",
        yaxis_title="Total Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Monthly Sales Trend  &  Payment Method Pie
col3, col4 = st.columns(2)

with col3:
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_trend = df.groupby("Month")["Sales"].sum().reset_index().sort_values("Month")
    fig = px.line(
        monthly_trend,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#2563eb"],
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Month",
        yaxis_title="Total Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
    )
    fig.update_traces(line_width=2.5, marker_size=7)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    pay_sales = df.groupby("Payment")["Sales"].sum().reset_index()
    fig = px.pie(
        pay_sales,
        names="Payment",
        values="Sales",
        title="Sales Share by Payment Method",
        color_discrete_sequence=PALETTE,
        hole=0.35,
    )
    fig.update_layout(
        font_family="Segoe UI",
        title_font_size=15,
        margin=dict(t=45, b=10, l=10, r=10),
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Gender breakdown  &  Branch + Category heatmap
col5, col6 = st.columns(2)

with col5:
    gender_cat = df.groupby(["Category", "Gender"])["Sales"].sum().reset_index()
    fig = px.bar(
        gender_cat,
        x="Category",
        y="Sales",
        color="Gender",
        barmode="group",
        title="Sales by Category & Gender",
        color_discrete_sequence=["#2563eb", "#f59e0b"],
        text_auto=".2s",
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Category",
        yaxis_title="Total Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
        legend_title="Gender",
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    heatmap_data = df.groupby(["Branch", "Category"])["Sales"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="Branch", columns="Category", values="Sales").fillna(0)
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns.tolist(),
            y=heatmap_pivot.index.tolist(),
            colorscale="Blues",
            text=heatmap_pivot.values.round(0),
            texttemplate="%{text:,.0f}",
            showscale=True,
            colorbar=dict(title="Sales (₹)"),
        )
    )
    fig.update_layout(
        title="Branch × Category Sales Heatmap",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Category",
        yaxis_title="Branch",
        margin=dict(t=45, b=10, l=10, r=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Top products  &  Rating distribution
col7, col8 = st.columns(2)

with col7:
    top_products = (
        df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top_products.sort_values("Sales"),
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        text_auto=".2s",
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Total Sales (₹)",
        yaxis_title="Product",
        coloraxis_showscale=False,
        margin=dict(t=45, b=10, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:
    fig = px.histogram(
        df,
        x="Rating",
        color="Category",
        nbins=18,
        title="Customer Rating Distribution by Category",
        barmode="overlay",
        opacity=0.7,
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Rating",
        yaxis_title="Count",
        margin=dict(t=45, b=10, l=10, r=10),
        legend_title="Category",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Row 5: Customer Type sales  &  Quantity vs Sales scatter
col9, col10 = st.columns(2)

with col9:
    ctype = df.groupby(["Customer Type", "Category"])["Sales"].sum().reset_index()
    fig = px.bar(
        ctype,
        x="Customer Type",
        y="Sales",
        color="Category",
        barmode="stack",
        title="Sales by Customer Type (Stacked by Category)",
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Customer Type",
        yaxis_title="Total Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
        legend_title="Category",
    )
    st.plotly_chart(fig, use_container_width=True)

with col10:
    fig = px.scatter(
        df,
        x="Quantity",
        y="Sales",
        color="Category",
        size="Unit Price",
        hover_data=["Product", "City", "Rating"],
        title="Quantity vs Sales (Bubble = Unit Price)",
        color_discrete_sequence=PALETTE,
        opacity=0.7,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_family="Segoe UI",
        title_font_size=15,
        xaxis_title="Quantity Sold",
        yaxis_title="Sales (₹)",
        margin=dict(t=45, b=10, l=10, r=10),
        legend_title="Category",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════
#  SECTION 6 — BUSINESS INSIGHTS
# ════════════════════════════════════════════
section("💡", "Step 6 — Business Decisions & Insights")

# Compute key facts from data
top_category    = df.groupby("Category")["Sales"].sum().idxmax()
top_city        = df.groupby("City")["Sales"].sum().idxmax()
top_branch      = df.groupby("Branch")["Sales"].sum().idxmax()
top_product     = df.groupby("Product")["Sales"].sum().idxmax()
top_payment     = df.groupby("Payment")["Sales"].sum().idxmax()
top_cust_type   = df.groupby("Customer Type")["Sales"].sum().idxmax()
top_gender      = df.groupby("Gender")["Sales"].sum().idxmax()
avg_rating      = df["Rating"].mean()
total_revenue   = df["Sales"].sum()
total_txns      = len(df)
avg_basket      = total_revenue / total_txns
best_rated_cat  = df.groupby("Category")["Rating"].mean().idxmax()
worst_rated_cat = df.groupby("Category")["Rating"].mean().idxmin()

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 📌 Key Performance Indicators")
    kpi_data = {
        "Metric": [
            "Total Revenue", "Total Transactions", "Average Basket Size",
            "Top Revenue Category", "Top Revenue City", "Top Branch",
            "Best-Selling Product", "Preferred Payment", "Dominant Customer Type",
            "Top Gender Segment", "Average Customer Rating",
            "Highest-Rated Category", "Lowest-Rated Category",
        ],
        "Value": [
            f"₹ {total_revenue:,.2f}", f"{total_txns:,}", f"₹ {avg_basket:,.2f}",
            top_category, top_city, f"Branch {top_branch}",
            top_product, top_payment, top_cust_type,
            top_gender, f"{avg_rating:.2f} / 5",
            best_rated_cat, worst_rated_cat,
        ],
    }
    st.dataframe(pd.DataFrame(kpi_data), use_container_width=True, hide_index=True)

with col_b:
    st.markdown("#### 🎯 Actionable Recommendations")

    insights = [
        ("📦", "Stock & Inventory",
         f"<strong>{top_category}</strong> is the top revenue driver. Prioritise shelf space, "
         f"supplier contracts, and promotions for this category to maximise returns."),
        ("🏙️", "City Expansion",
         f"<strong>{top_city}</strong> generates the highest sales. Consider opening additional "
         f"counters or launching targeted loyalty campaigns there."),
        ("🏢", "Branch Performance",
         f"<strong>Branch {top_branch}</strong> leads in revenue. Study its operational practices "
         f"and replicate them across underperforming branches."),
        ("💳", "Payment Optimisation",
         f"<strong>{top_payment}</strong> is the most used payment method. Negotiate lower MDR "
         f"rates with the provider and promote it with cashback offers."),
        ("👤", "Customer Loyalty",
         f"<strong>{top_cust_type}</strong> customers contribute more revenue. Invest in a "
         f"membership rewards programme to convert Normal buyers into Members."),
        ("⭐", "Service Quality",
         f"<strong>{worst_rated_cat}</strong> has the lowest average rating. Review product quality, "
         f"freshness, or display for this category and collect feedback."),
        ("🛍️", "Upselling",
         f"The scatter chart shows a positive correlation between Quantity and Sales. "
         f"Train staff to suggest bundle deals and multi-unit discounts."),
        ("📅", "Seasonal Planning",
         f"Use the monthly trend chart to identify peak and low-traffic months. "
         f"Plan discounts and stock-ups ahead of peak periods."),
    ]

    for icon, title, text in insights:
        st.markdown(
            f'<div class="info-box">'
            f'<strong>{icon} {title}:</strong><br>{text}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ─── Full Filtered Dataset Download
st.markdown("---")
section("📥", "Export Filtered Data")
csv_export = df.drop(columns=["Calculated_Sales", "Sales_Match", "Month"], errors="ignore").to_csv(index=False)
st.download_button(
    label="⬇️  Download Filtered Dataset as CSV",
    data=csv_export,
    file_name="filtered_supermarket_sales.csv",
    mime="text/csv",
)

# ─── Footer
st.markdown(
    "<br><hr><p style='text-align:center; color:#94a3b8; font-size:13px;'>"
    "🛒 Supermarket Sales Analytics Dashboard &nbsp;|&nbsp; Built with Streamlit & Plotly"
    "</p>",
    unsafe_allow_html=True,
)
