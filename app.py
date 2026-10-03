
import streamlit as st
import pandas as pd
from io import BytesIO

from processor import (
    check_file_compatibility,
    get_dataset_overview,
    get_column_profile,
    get_numeric_analysis,
    get_categorical_analysis,
    get_numeric_columns,
    get_text_columns,
    get_date_columns,
    get_date_analysis,
    get_records_by_month,
    get_records_by_year,
    get_correlation_matrix,
    get_strong_correlations,
    detect_outliers,
    get_histogram_data,
    clean_data
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Universal Data Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# Theme-compatible: works with Light + Dark mode
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GENERAL LAYOUT
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
        color: var(--text-color);
    }


    .subtitle {
        font-size: 17px;
        color: var(--text-color);
        opacity: 0.65;
        margin-bottom: 25px;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        font-size: 24px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 10px;
        color: var(--text-color);
    }


    /* =====================================================
       INFO CARDS
       ===================================================== */

    .info-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);

        padding: 18px;

        border-radius: 12px;

        border: 1px solid rgba(128, 128, 128, 0.25);

        margin-bottom: 15px;
    }


    .info-card h4 {
        color: var(--text-color);
    }


    .info-card p {
        color: var(--text-color);
        opacity: 0.75;
    }


    /* =====================================================
       DATASET BADGE
       ===================================================== */

    .dataset-badge {
        display: inline-block;

        background-color: var(--secondary-background-color);

        color: var(--text-color);

        padding: 6px 12px;

        border-radius: 20px;

        font-size: 14px;

        font-weight: 600;

        border: 1px solid rgba(128, 128, 128, 0.25);

        margin-bottom: 8px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="metric-container"] {

        background-color: var(--secondary-background-color);

        border: 1px solid rgba(128, 128, 128, 0.25);

        padding: 12px;

        border-radius: 10px;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }


    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }


    /* =====================================================
       DATAFRAMES
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    div[data-testid="stExpander"] {
        border-radius: 10px;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 Universal Data Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Analyze, visualize and clean CSV / Excel datasets automatically.
        No domain-specific configuration required.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Data Analyzer")

    st.write(
        "Upload your dataset and use the available "
        "analysis and cleaning tools."
    )

    st.divider()

    st.markdown("### 🧩 Features")

    st.write("📋 Dataset profiling")
    st.write("🔍 Automatic data types")
    st.write("📊 Statistical analysis")
    st.write("📈 Visualizations")
    st.write("📅 Date analysis")
    st.write("🔗 Correlation analysis")
    st.write("🚨 Outlier detection")
    st.write("🧹 Data cleaning")
    st.write("📥 CSV / Excel export")

    st.divider()

    st.caption(
        "Supported formats: CSV, XLSX"
    )

    st.caption(
        "Built with Python, Pandas and Streamlit."
    )


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📂 Upload Dataset</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload one or more CSV / Excel files",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    help="You can upload CSV or XLSX files."
)


# =========================================================
# EMPTY STATE
# =========================================================

if not uploaded_files:

    st.info(
        "👆 Upload a CSV or Excel file to start analyzing your data."
    )

    st.markdown(
        '<div class="section-title">What you can do</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">

                <h4>🔍 Understand</h4>

                <p>
                Automatically inspect rows, columns,
                missing values, duplicates and data types.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

                <h4>📈 Analyze</h4>

                <p>
                Explore statistics, distributions,
                categories, dates and correlations.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="info-card">

                <h4>🧹 Clean</h4>

                <p>
                Remove duplicates, handle missing
                values and manage outliers.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.stop()


# =========================================================
# READ UPLOADED FILES
# =========================================================

dataframes = []
file_names = []
failed_files = []


for uploaded_file in uploaded_files:

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file
            )

        dataframes.append(df)

        file_names.append(
            uploaded_file.name
        )

    except Exception as e:

        failed_files.append(
            f"{uploaded_file.name}: {e}"
        )


# =========================================================
# FILE ERRORS
# =========================================================

if failed_files:

    st.warning(
        "⚠️ Some files could not be read."
    )

    for error in failed_files:

        st.write(
            f"• {error}"
        )


if not dataframes:

    st.error(
        "No valid datasets were loaded."
    )

    st.stop()


# =========================================================
# FILE COMPATIBILITY
# =========================================================

compatible = check_file_compatibility(
    dataframes
)


if len(dataframes) == 1:

    datasets = [
        (
            file_names[0],
            dataframes[0]
        )
    ]

    st.success(
        f"✅ Loaded {file_names[0]}"
    )


elif compatible:

    st.success(
        "✅ All uploaded files have compatible columns."
    )

    combine_files = st.checkbox(
        "Combine compatible files",
        value=True
    )

    if combine_files:

        combined_df = pd.concat(
            dataframes,
            ignore_index=True
        )

        datasets = [
            (
                "Combined Dataset",
                combined_df
            )
        ]

    else:

        datasets = list(
            zip(
                file_names,
                dataframes
            )
        )


else:

    st.warning(
        "⚠️ Uploaded files have different column structures."
    )

    st.info(
        "They will be analyzed separately."
    )

    datasets = list(
        zip(
            file_names,
            dataframes
        )
    )


# =========================================================
# DATASET PROCESSING
# =========================================================

for dataset_name, df in datasets:

    st.divider()

    # =====================================================
    # DATASET HEADER
    # =====================================================

    st.markdown(
        f"""
        <div class="dataset-badge">
            📁 {dataset_name}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header(
        dataset_name
    )


    # =====================================================
    # OVERVIEW
    # =====================================================

    overview = get_dataset_overview(
        df
    )

    st.markdown(
        '<div class="section-title">📋 Dataset Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        f"{overview['rows']:,}"
    )

    col2.metric(
        "Columns",
        overview["columns"]
    )

    col3.metric(
        "Duplicate Rows",
        f"{overview['duplicate_rows']:,}"
    )

    col4.metric(
        "Missing Cells",
        f"{overview['missing_cells']:,}"
    )


    # =====================================================
    # DATA TYPE SUMMARY
    # =====================================================

    st.markdown(
        '<div class="section-title">🔍 Data Type Summary</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🔢 Numeric",
        overview["numeric_columns"]
    )

    col2.metric(
        "🔤 Text",
        overview["text_columns"]
    )

    col3.metric(
        "📅 Date",
        overview["date_columns"]
    )

    col4.metric(
        "☑️ Boolean",
        overview["boolean_columns"]
    )


    # =====================================================
    # DATASET PREVIEW
    # =====================================================

    with st.expander(
        "👀 View Dataset Preview",
        expanded=True
    ):

        st.dataframe(
            df.head(100),
            use_container_width=True,
            height=350
        )


    # =====================================================
    # COLUMN PROFILE
    # =====================================================

    with st.expander(
        "📊 Column Profile"
    ):

        column_profile = get_column_profile(
            df
        )

        st.dataframe(
            column_profile,
            hide_index=True,
            use_container_width=True
        )


    # =====================================================
    # STATISTICAL ANALYSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">📐 Statistical Analysis</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        [
            "🔢 Numeric",
            "🔤 Categorical"
        ]
    )


    # =====================================================
    # NUMERIC ANALYSIS
    # =====================================================

    with tab1:

        numeric_analysis = (
            get_numeric_analysis(df)
        )

        if not numeric_analysis.empty:

            st.dataframe(
                numeric_analysis,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns found."
            )


    # =====================================================
    # CATEGORICAL ANALYSIS
    # =====================================================

    with tab2:

        categorical_analysis = (
            get_categorical_analysis(df)
        )

        if not categorical_analysis.empty:

            st.dataframe(
                categorical_analysis,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No categorical columns found."
            )


    # =====================================================
    # VISUALIZATIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 Visualizations</div>',
        unsafe_allow_html=True
    )

    numeric_columns = get_numeric_columns(
        df
    )

    text_columns = get_text_columns(
        df
    )

    date_columns = get_date_columns(
        df
    )


    # =====================================================
    # NUMERIC DISTRIBUTION
    # =====================================================

    if numeric_columns:

        with st.expander(
            "🔢 Numeric Distribution",
            expanded=True
        ):

            selected_numeric = st.selectbox(
                "Select numeric column",
                numeric_columns,
                key=f"numeric_{dataset_name}"
            )

            histogram = get_histogram_data(
                df,
                selected_numeric,
                bins=12
            )

            if not histogram.empty:

                st.bar_chart(
                    histogram,
                    use_container_width=True
                )


    # =====================================================
    # CATEGORICAL DISTRIBUTION
    # =====================================================

    if text_columns:

        with st.expander(
            "🔤 Categorical Distribution",
            expanded=False
        ):

            selected_text = st.selectbox(
                "Select categorical column",
                text_columns,
                key=f"text_{dataset_name}"
            )

            category_counts = (
                df[selected_text]
                .value_counts()
                .head(15)
            )

            if not category_counts.empty:

                st.bar_chart(
                    category_counts,
                    use_container_width=True
                )


    # =====================================================
    # DATE ANALYSIS
    # =====================================================

    if date_columns:

        with st.expander(
            "📅 Date Analysis",
            expanded=False
        ):

            selected_date = st.selectbox(
                "Select date column",
                date_columns,
                key=f"date_{dataset_name}"
            )

            date_info = get_date_analysis(
                df,
                selected_date
            )

            if date_info["min_date"] is not None:

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "First Date",
                    str(
                        date_info[
                            "min_date"
                        ].date()
                    )
                )

                col2.metric(
                    "Last Date",
                    str(
                        date_info[
                            "max_date"
                        ].date()
                    )
                )

                col3.metric(
                    "Date Range",
                    f"{date_info['date_range_days']:,} days"
                )


            monthly_data = (
                get_records_by_month(
                    df,
                    selected_date
                )
            )

            if not monthly_data.empty:

                st.markdown(
                    "#### Records by Month"
                )

                st.line_chart(
                    monthly_data,
                    use_container_width=True
                )


            yearly_data = (
                get_records_by_year(
                    df,
                    selected_date
                )
            )

            if not yearly_data.empty:

                st.markdown(
                    "#### Records by Year"
                )

                st.bar_chart(
                    yearly_data,
                    use_container_width=True
                )


    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================

    with st.expander(
        "🔗 Correlation Analysis",
        expanded=False
    ):

        correlation_matrix = (
            get_correlation_matrix(df)
        )

        if not correlation_matrix.empty:

            st.info(
                "Correlation measures the strength and "
                "direction of a linear relationship between "
                "numeric variables. It does not establish causation."
            )

            st.dataframe(
                correlation_matrix,
                use_container_width=True
            )

            threshold = st.slider(
                "Minimum absolute correlation",
                min_value=0.1,
                max_value=1.0,
                value=0.5,
                step=0.1,
                key=f"threshold_{dataset_name}"
            )

            strong_correlations = (
                get_strong_correlations(
                    df,
                    threshold
                )
            )

            if not strong_correlations.empty:

                st.markdown(
                    "#### Strong Correlations"
                )

                st.dataframe(
                    strong_correlations,
                    hide_index=True,
                    use_container_width=True
                )

            else:

                st.info(
                    "No correlations found above "
                    "the selected threshold."
                )

        else:

            st.info(
                "At least two numeric columns are required "
                "for correlation analysis."
            )


    # =====================================================
    # OUTLIER DETECTION
    # =====================================================

    with st.expander(
        "🚨 Outlier Detection",
        expanded=False
    ):

        outlier_report = detect_outliers(
            df
        )

        if not outlier_report.empty:

            st.dataframe(
                outlier_report,
                hide_index=True,
                use_container_width=True
            )

            st.caption(
                "Outliers are detected using the "
                "IQR (Interquartile Range) method."
            )

        else:

            st.info(
                "No numeric columns available "
                "for outlier detection."
            )


    # =====================================================
    # DATA CLEANING
    # =====================================================

    st.markdown(
        '<div class="section-title">🧹 Data Cleaning</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose how you want to handle duplicates, "
        "missing values and outliers."
    )


    clean_col1, clean_col2 = st.columns(2)


    # =====================================================
    # DUPLICATES + NUMERIC MISSING
    # =====================================================

    with clean_col1:

        duplicate_action = st.selectbox(
            "Duplicate rows",
            [
                "Remove",
                "Keep"
            ],
            key=f"duplicates_{dataset_name}"
        )

        numeric_missing_action = st.selectbox(
            "Missing numeric values",
            [
                "Median",
                "Mean",
                "Remove Rows",
                "Keep"
            ],
            key=f"numeric_missing_{dataset_name}"
        )


    # =====================================================
    # TEXT MISSING + OUTLIERS
    # =====================================================

    with clean_col2:

        text_missing_action = st.selectbox(
            "Missing text values",
            [
                "Unknown",
                "Most Frequent",
                "Remove Rows",
                "Keep"
            ],
            key=f"text_missing_{dataset_name}"
        )

        outlier_action = st.selectbox(
            "Outliers",
            [
                "Keep",
                "Remove Rows",
                "Cap Values"
            ],
            key=f"outliers_{dataset_name}"
        )


    # =====================================================
    # CLEAN BUTTON
    # =====================================================

    clean_button = st.button(
        "🚀 Apply Cleaning",
        type="primary",
        key=f"clean_{dataset_name}"
    )


    # =====================================================
    # CLEANING RESULT
    # =====================================================

    if clean_button:

        cleaned_df, stats = clean_data(
            df,
            duplicate_action,
            numeric_missing_action,
            text_missing_action,
            outlier_action
        )

        st.success(
            "✅ Cleaning completed successfully!"
        )


        # =================================================
        # CLEANING SUMMARY
        # =================================================

        st.markdown(
            "### 📊 Cleaning Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Original Rows",
            f"{stats['original_rows']:,}"
        )

        col2.metric(
            "Final Rows",
            f"{stats['final_rows']:,}"
        )

        col3.metric(
            "Rows Removed",
            f"{stats['rows_removed']:,}"
        )

        col4.metric(
            "Missing Values",
            (
                f"{stats['original_missing']:,}"
                " → "
                f"{stats['final_missing']:,}"
            )
        )


        # =================================================
        # SECONDARY CLEANING METRICS
        # =================================================

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Original Duplicates",
            f"{stats['original_duplicates']:,}"
        )

        col2.metric(
            "Duplicates Removed",
            f"{stats['duplicates_removed']:,}"
        )

        col3.metric(
            "Outlier Rows Removed",
            f"{stats['outlier_rows_removed']:,}"
        )


        # =================================================
        # CLEANED DATASET
        # =================================================

        with st.expander(
            "✨ View Cleaned Dataset",
            expanded=True
        ):

            st.dataframe(
                cleaned_df.head(100),
                use_container_width=True,
                height=350
            )


        # =================================================
        # EXPORT
        # =================================================

        st.markdown(
            "### 📥 Export Results"
        )

        safe_name = (
            dataset_name
            .replace(" ", "_")
            .replace(".csv", "")
            .replace(".xlsx", "")
        )


        # =================================================
        # CSV EXPORT
        # =================================================

        csv_data = (
            cleaned_df
            .to_csv(index=False)
            .encode("utf-8")
        )


        # =================================================
        # EXCEL EXPORT
        # =================================================

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            cleaned_df.to_excel(
                writer,
                sheet_name="Cleaned Data",
                index=False
            )

            column_profile.to_excel(
                writer,
                sheet_name="Column Profile",
                index=False
            )

            numeric_analysis.to_excel(
                writer,
                sheet_name="Numeric Analysis",
                index=False
            )

            categorical_analysis.to_excel(
                writer,
                sheet_name="Categorical Analysis",
                index=False
            )

            outlier_report.to_excel(
                writer,
                sheet_name="Outliers",
                index=False
            )

            correlation_matrix.to_excel(
                writer,
                sheet_name="Correlations"
            )


        excel_buffer.seek(0)


        # =================================================
        # DOWNLOAD BUTTONS
        # =================================================

        download_col1, download_col2 = st.columns(2)


        with download_col1:

            st.download_button(
                label="📄 Download Cleaned CSV",
                data=csv_data,
                file_name=(
                    f"cleaned_{safe_name}.csv"
                ),
                mime="text/csv",
                use_container_width=True,
                key=f"csv_{dataset_name}"
            )


        with download_col2:

            st.download_button(
                label="📊 Download Excel Report",
                data=excel_buffer.getvalue(),
                file_name=(
                    f"analysis_{safe_name}.xlsx"
                ),
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                ),
                use_container_width=True,
                key=f"excel_{dataset_name}"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Universal Data Analyzer • "
    "Python + Pandas + Streamlit"
)

