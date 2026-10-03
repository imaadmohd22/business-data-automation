import pandas as pd


# =========================
# Detect Data Type
# =========================

def detect_column_type(series):

    if pd.api.types.is_bool_dtype(series):
        return "Boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "Numeric"

    converted_dates = pd.to_datetime(
        series,
        errors="coerce"
    )

    valid_ratio = converted_dates.notna().mean()

    if valid_ratio >= 0.8:
        return "Date"

    return "Text"


# =========================
# File Compatibility
# =========================

def check_file_compatibility(dataframes):

    if len(dataframes) <= 1:
        return True

    first_columns = list(dataframes[0].columns)

    for df in dataframes[1:]:

        if list(df.columns) != first_columns:
            return False

    return True


# =========================
# Dataset Overview
# =========================

def get_dataset_overview(df):

    total_rows = len(df)
    total_columns = len(df.columns)

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_cells = int(
        df.isna().sum().sum()
    )

    numeric_columns = 0
    text_columns = 0
    date_columns = 0
    boolean_columns = 0

    for column in df.columns:

        column_type = detect_column_type(
            df[column]
        )

        if column_type == "Numeric":
            numeric_columns += 1

        elif column_type == "Text":
            text_columns += 1

        elif column_type == "Date":
            date_columns += 1

        elif column_type == "Boolean":
            boolean_columns += 1

    return {
        "rows": total_rows,
        "columns": total_columns,
        "duplicate_rows": duplicate_rows,
        "missing_cells": missing_cells,
        "numeric_columns": numeric_columns,
        "text_columns": text_columns,
        "date_columns": date_columns,
        "boolean_columns": boolean_columns
    }


# =========================
# Column Profile
# =========================

def get_column_profile(df):

    profile = []

    for column in df.columns:

        series = df[column]

        column_type = detect_column_type(
            series
        )

        missing_count = int(
            series.isna().sum()
        )

        unique_count = int(
            series.nunique(
                dropna=True
            )
        )

        non_null = series.dropna()

        if not non_null.empty:

            example_value = str(
                non_null.iloc[0]
            )

        else:

            example_value = "No data"

        profile.append({
            "Column": column,
            "Type": column_type,
            "Missing": missing_count,
            "Unique Values": unique_count,
            "Example": example_value
        })

    return pd.DataFrame(profile)


# =========================
# Numeric Analysis
# =========================

def get_numeric_analysis(df):

    numeric_columns = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    if len(numeric_columns) == 0:
        return pd.DataFrame()

    result = (
        df[numeric_columns]
        .describe()
        .T
        .reset_index()
    )

    result = result.rename(
        columns={
            "index": "Column"
        }
    )

    return result


# =========================
# Categorical Analysis
# =========================

def get_categorical_analysis(df):

    results = []

    for column in df.columns:

        if detect_column_type(
            df[column]
        ) != "Text":
            continue

        counts = (
            df[column]
            .value_counts(
                dropna=False
            )
            .head(10)
        )

        for value, count in counts.items():

            results.append({
                "Column": column,
                "Value": str(value),
                "Count": int(count)
            })

    return pd.DataFrame(results)


# =========================
# Column Lists
# =========================

def get_numeric_columns(df):

    return list(
        df.select_dtypes(
            include="number"
        ).columns
    )


def get_text_columns(df):

    columns = []

    for column in df.columns:

        if detect_column_type(
            df[column]
        ) == "Text":

            columns.append(column)

    return columns


def get_date_columns(df):

    columns = []

    for column in df.columns:

        if detect_column_type(
            df[column]
        ) == "Date":

            columns.append(column)

    return columns


# =========================
# Date Analysis
# =========================

def get_date_analysis(df, column):

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    ).dropna()

    if dates.empty:

        return {
            "min_date": None,
            "max_date": None,
            "date_range_days": 0,
            "total_valid_dates": 0
        }

    min_date = dates.min()
    max_date = dates.max()

    date_range_days = (
        max_date - min_date
    ).days

    return {
        "min_date": min_date,
        "max_date": max_date,
        "date_range_days": date_range_days,
        "total_valid_dates": len(dates)
    }


# =========================
# Records By Month
# =========================

def get_records_by_month(df, column):

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    valid_dates = dates.dropna()

    if valid_dates.empty:
        return pd.DataFrame()

    monthly_counts = (
        valid_dates
        .dt.to_period("M")
        .value_counts()
        .sort_index()
    )

    result = pd.DataFrame({
        "Month": (
            monthly_counts
            .index
            .astype(str)
        ),
        "Records": monthly_counts.values
    })

    return result.set_index("Month")


# =========================
# Records By Year
# =========================

def get_records_by_year(df, column):

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    valid_dates = dates.dropna()

    if valid_dates.empty:
        return pd.DataFrame()

    yearly_counts = (
        valid_dates
        .dt.year
        .value_counts()
        .sort_index()
    )

    result = pd.DataFrame({
        "Year": yearly_counts.index,
        "Records": yearly_counts.values
    })

    return result.set_index("Year")


# =========================
# Correlation Analysis
# =========================

def get_correlation_matrix(df):

    numeric_columns = (
        get_numeric_columns(df)
    )

    if len(numeric_columns) < 2:
        return pd.DataFrame()

    correlation = (
        df[numeric_columns]
        .corr()
        .round(3)
    )

    return correlation


# =========================
# Strong Correlations
# =========================

def get_strong_correlations(
    df,
    threshold=0.5
):

    correlation = (
        get_correlation_matrix(df)
    )

    if correlation.empty:
        return pd.DataFrame()

    results = []

    columns = list(
        correlation.columns
    )

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            col1 = columns[i]
            col2 = columns[j]

            value = correlation.loc[
                col1,
                col2
            ]

            if pd.isna(value):
                continue

            if abs(value) >= threshold:

                results.append({
                    "Column 1": col1,
                    "Column 2": col2,
                    "Correlation": value,
                    "Relationship":
                        (
                            "Positive"
                            if value > 0
                            else "Negative"
                        )
                })

    if not results:
        return pd.DataFrame(
            columns=[
                "Column 1",
                "Column 2",
                "Correlation",
                "Relationship"
            ]
        )

    return (
        pd.DataFrame(results)
        .sort_values(
            "Correlation",
            key=lambda x: x.abs(),
            ascending=False
        )
        .reset_index(drop=True)
    )


# =========================
# Outlier Detection
# =========================

def detect_outliers(df):

    results = []

    numeric_columns = (
        get_numeric_columns(df)
    )

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:

            results.append({
                "Column": column,
                "Q1": None,
                "Q3": None,
                "IQR": None,
                "Lower Bound": None,
                "Upper Bound": None,
                "Outliers": 0,
                "Outlier %": 0.0
            })

            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:

            outlier_count = 0

        else:

            lower_bound = (
                q1 - 1.5 * iqr
            )

            upper_bound = (
                q3 + 1.5 * iqr
            )

            outlier_mask = (
                (series < lower_bound)
                |
                (series > upper_bound)
            )

            outlier_count = int(
                outlier_mask.sum()
            )

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        outlier_percentage = (
            outlier_count
            / len(series)
            * 100
        )

        results.append({
            "Column": column,
            "Q1": round(q1, 4),
            "Q3": round(q3, 4),
            "IQR": round(iqr, 4),
            "Lower Bound":
                round(
                    lower_bound,
                    4
                ),
            "Upper Bound":
                round(
                    upper_bound,
                    4
                ),
            "Outliers":
                outlier_count,
            "Outlier %":
                round(
                    outlier_percentage,
                    2
                )
        })

    return pd.DataFrame(results)


# =========================
# Histogram Data
# =========================

def get_histogram_data(
    df,
    column,
    bins=10
):

    series = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if series.empty:
        return pd.DataFrame()

    if series.nunique() == 1:

        return pd.DataFrame({
            "Range": [
                str(series.iloc[0])
            ],
            "Count": [
                len(series)
            ]
        }).set_index("Range")

    categories = pd.cut(
        series,
        bins=bins,
        include_lowest=True
    )

    counts = (
        categories
        .value_counts()
        .sort_index()
    )

    result = pd.DataFrame({
        "Range":
            counts.index.astype(str),
        "Count":
            counts.values
    })

    return result.set_index("Range")


# =========================
# Cleaning
# =========================

def clean_data(
    df,
    duplicate_action="Remove",
    numeric_missing_action="Median",
    text_missing_action="Unknown",
    outlier_action="Keep"
):

    cleaned_df = df.copy()

    original_rows = len(
        cleaned_df
    )

    original_missing = int(
        cleaned_df.isna()
        .sum()
        .sum()
    )

    original_duplicates = int(
        cleaned_df.duplicated()
        .sum()
    )

    # =========================
    # Duplicate Handling
    # =========================

    if duplicate_action == "Remove":

        cleaned_df = (
            cleaned_df
            .drop_duplicates()
            .copy()
        )

    duplicates_removed = (
        original_rows
        - len(cleaned_df)
    )


    # =========================
    # Numeric Missing Values
    # =========================

    numeric_columns = (
        get_numeric_columns(
            cleaned_df
        )
    )

    if (
        numeric_missing_action
        == "Median"
    ):

        for column in numeric_columns:

            if cleaned_df[
                column
            ].isna().any():

                value = (
                    cleaned_df[column]
                    .median()
                )

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(value)
                )


    elif (
        numeric_missing_action
        == "Mean"
    ):

        for column in numeric_columns:

            if cleaned_df[
                column
            ].isna().any():

                value = (
                    cleaned_df[column]
                    .mean()
                )

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(value)
                )


    elif (
        numeric_missing_action
        == "Remove Rows"
    ):

        if numeric_columns:

            cleaned_df = (
                cleaned_df
                .dropna(
                    subset=numeric_columns
                )
                .copy()
            )


    # =========================
    # Text Missing Values
    # =========================

    text_columns = (
        get_text_columns(
            cleaned_df
        )
    )

    if (
        text_missing_action
        == "Unknown"
    ):

        for column in text_columns:

            cleaned_df[column] = (
                cleaned_df[column]
                .fillna("Unknown")
            )


    elif (
        text_missing_action
        == "Most Frequent"
    ):

        for column in text_columns:

            if cleaned_df[
                column
            ].isna().any():

                mode = (
                    cleaned_df[column]
                    .mode()
                )

                if not mode.empty:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(mode.iloc[0])
                    )


    elif (
        text_missing_action
        == "Remove Rows"
    ):

        if text_columns:

            cleaned_df = (
                cleaned_df
                .dropna(
                    subset=text_columns
                )
                .copy()
            )


    # =========================
    # Outlier Handling
    # =========================

    outlier_rows_removed = 0

    numeric_columns = (
        get_numeric_columns(
            cleaned_df
        )
    )

    if (
        outlier_action
        == "Remove Rows"
    ):

        rows_before = len(
            cleaned_df
        )

        row_mask = pd.Series(
            True,
            index=cleaned_df.index
        )

        for column in numeric_columns:

            series = cleaned_df[
                column
            ]

            if series.dropna().empty:
                continue

            q1 = series.quantile(
                0.25
            )

            q3 = series.quantile(
                0.75
            )

            iqr = q3 - q1

            if iqr == 0:
                continue

            lower = (
                q1 - 1.5 * iqr
            )

            upper = (
                q3 + 1.5 * iqr
            )

            column_mask = (
                series.isna()
                |
                (
                    series >= lower
                )
                &
                (
                    series <= upper
                )
            )

            row_mask = (
                row_mask
                & column_mask
            )

        cleaned_df = (
            cleaned_df[
                row_mask
            ]
            .copy()
        )

        outlier_rows_removed = (
            rows_before
            - len(cleaned_df)
        )


    elif (
        outlier_action
        == "Cap Values"
    ):

        for column in numeric_columns:

            series = cleaned_df[
                column
            ]

            if series.dropna().empty:
                continue

            q1 = series.quantile(
                0.25
            )

            q3 = series.quantile(
                0.75
            )

            iqr = q3 - q1

            if iqr == 0:
                continue

            lower = (
                q1 - 1.5 * iqr
            )

            upper = (
                q3 + 1.5 * iqr
            )

            cleaned_df[column] = (
                series.clip(
                    lower,
                    upper
                )
            )


    # =========================
    # Final Statistics
    # =========================

    final_rows = len(
        cleaned_df
    )

    final_missing = int(
        cleaned_df.isna()
        .sum()
        .sum()
    )

    final_duplicates = int(
        cleaned_df.duplicated()
        .sum()
    )

    return cleaned_df, {

        "original_rows":
            original_rows,

        "final_rows":
            final_rows,

        "rows_removed":
            original_rows
            - final_rows,

        "original_missing":
            original_missing,

        "final_missing":
            final_missing,

        "original_duplicates":
            original_duplicates,

        "duplicates_removed":
            duplicates_removed,

        "final_duplicates":
            final_duplicates,

        "outlier_rows_removed":
            outlier_rows_removed
    }

