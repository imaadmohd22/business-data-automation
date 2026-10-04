# Generic CSV & Excel Data Analyzer

A Python-based web application for **cleaning, profiling, analyzing, and exporting CSV and Excel datasets**.

The tool is designed to work with general-purpose tabular data rather than a specific business domain. Users can upload CSV/XLSX files, automatically inspect data quality, analyze columns, detect outliers and correlations, clean the dataset, and download the processed result.

## 🚀 Features

### 📂 File Upload

* Supports CSV files
* Supports Excel (`.xlsx`) files
* Handles invalid or unsupported files gracefully
* Supports multiple uploaded files

### 🔍 Automatic Data Profiling

The application automatically analyzes uploaded datasets and provides:

* Number of rows and columns
* Column names
* Data types
* Missing values
* Duplicate records
* Unique values
* Numeric and categorical columns
* Date columns

### 📊 Data Analysis

#### Numeric Analysis

* Count
* Mean
* Standard deviation
* Minimum
* Maximum
* Quartiles
* Distribution visualization

#### Categorical Analysis

* Unique values
* Most frequent values
* Frequency distribution
* Category visualization

#### Date Analysis

* Minimum date
* Maximum date
* Date range
* Records by month
* Records by year

### 🔗 Correlation Analysis

The application can calculate correlations between numeric columns and identify strong relationships.

> Correlation does not necessarily imply causation.

### 🚨 Outlier Detection

Uses the **Interquartile Range (IQR)** method to identify potential numeric outliers.

Users can:

* View detected outliers
* Keep outliers
* Remove outlier rows
* Cap extreme values

### 🧹 Data Cleaning

Users can configure cleaning operations for:

* Missing numeric values
* Missing text values
* Duplicate rows
* Numeric outliers

Available strategies include:

* Remove rows
* Keep missing values
* Replace with median
* Replace with mean
* Replace with most frequent value
* Replace missing text with `"Unknown"`
* Remove or cap outliers

### 📥 Export

After cleaning, users can download the processed dataset as:

* CSV
* Excel (`.xlsx`)

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** — data processing and analysis
* **Streamlit** — interactive web application
* **OpenPyXL** — Excel file handling

---

## 🏗️ Project Structure

```text
business-data-automation/
│
├── app.py              # Streamlit application and UI
├── processor.py        # Data processing and analysis logic
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignored files
└── README.md           # Project documentation
```

---

## 🔄 Application Workflow

```text
CSV / Excel Upload
        ↓
File Detection
        ↓
Dataset Preview
        ↓
Automatic Data Profiling
        ↓
Data Quality Checks
        ↓
Data Cleaning
        ↓
Statistical Analysis
        ↓
Charts & Visualizations
        ↓
Export Cleaned Dataset
```

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/imaadmohd22/business-data-automation.git
```

### 2. Navigate to the project

```bash
cd business-data-automation
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📌 Example Use Cases

This tool can be useful for datasets such as:

* Business data
* Customer data
* Survey datasets
* Financial datasets
* Sports statistics
* Operational data
* Research datasets
* Marketing data
* General CSV/Excel files

The application does not depend on a fixed set of domain-specific columns, allowing it to work with many different types of tabular datasets.

---

## 🎯 Project Objective

The goal of this project is to automate common data-preparation tasks that are often performed manually.

Instead of repeatedly:

1. Opening a CSV/Excel file
2. Checking missing values
3. Finding duplicates
4. Inspecting data types
5. Looking for outliers
6. Calculating statistics
7. Creating basic visualizations
8. Cleaning the dataset
9. Exporting the final file

users can perform these tasks through a single interactive application.

---

## 🔮 Future Improvements

Potential improvements include:

* PDF report generation
* Automated data-quality scoring
* More visualization options
* Advanced Excel support
* Multi-file comparison
* Intelligent column matching
* Automated cleaning recommendations
* User-defined cleaning pipelines
* Database connectivity
* Authentication
* Cloud deployment
* AI-assisted data analysis

---

## 👨‍💻 Author

**Mohd Imaad**

Computer Science & Artificial Intelligence

GitHub:
https://github.com/imaadmohd22

LinkedIn:
https://www.linkedin.com/in/mohd-imaad-b40311257/

---

## 📄 License

This project is currently available for portfolio and demonstration purposes.
