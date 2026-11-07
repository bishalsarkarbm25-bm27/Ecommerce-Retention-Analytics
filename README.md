# E-Commerce Customer Retention & Revenue Intelligence

## 1. Project Overview

The E-Commerce Customer Retention & Revenue Intelligence
Dashboard is an interactive business analytics application
developed using Python and Streamlit.

The project focuses on customer retention, revenue
intelligence, customer segmentation, and churn-risk analysis.

The dashboard helps managers identify customers who may
require retention attention and understand how customer
behaviour affects business performance.

The project uses a synthetic customer dataset generated
using NumPy and Pandas.

## 2. Business Problem

Customer churn can negatively affect recurring revenue,
customer lifetime value, and long-term business growth.

An e-commerce company may have thousands of customers,
but its retention team has limited time and resources.

The business needs to understand:

- Which customers are likely to stop purchasing?
- Which customer segments generate the most revenue?
- Which customers should the retention team contact first?
- How much annualised revenue is potentially at risk?
- What actions can managers take to improve retention?

This project demonstrates how customer data can be
transformed into actionable business insights.

## 3. Project Objectives

The main objectives are:

1. Analyse customer purchasing behaviour.
2. Identify customer churn patterns.
3. Evaluate revenue across customer segments.
4. Calculate an illustrative customer retention risk score.
5. Prioritise high-risk customer records.
6. Recommend suitable retention actions.
7. Develop an interactive dashboard for managers.

## 4. Dataset Description

The project uses a synthetic dataset containing
approximately 2,000 customer records.

The dataset includes:

| Column | Description |
|---|---|
| CustomerID | Unique customer identifier |
| Tenure | Number of months as a customer |
| MonthlySpend | Monthly customer spending |
| TotalSpend | Cumulative customer spending |
| NumOrders | Number of orders |
| AvgOrderValue | Average order value |
| DaysSinceLastOrder | Days since the last purchase |
| SupportTickets | Number of customer support tickets |
| ContractType | Customer contract category |
| TechSupport | Tech Support subscription status |
| Churn | Customer churn indicator |

The dataset is synthetic and does not contain
confidential customer information.

## 5. Dashboard Features

### Executive Summary

The dashboard displays:

- Total customers
- Churned customers
- Churn rate
- High-risk active customers
- Annualised revenue at risk

### Customer Retention Analytics

The dashboard evaluates customer churn patterns
across different contract types.

### Revenue Intelligence

The application provides annualised revenue analysis
by customer contract category.

### Customer Segmentation

Customers are classified into:

- New Customers
- Growing Customers
- Loyal Customers

The dashboard provides customer counts, revenue
information, and churn metrics for each segment.

### Retention Risk Assessment

The dashboard uses an illustrative heuristic.

The scoring rules are:

| Risk Indicator | Condition | Score |
|---|---|---:|
| Contract Type | Month-to-month | +2 |
| Tech Support | No | +1 |
| Tenure | 12 months or less | +1 |
| Last Order | More than 60 days ago | +2 |
| Support Tickets | 4 or more | +1 |

A score of 3 or above is classified as High Risk.

A score below 3 is classified as Low Risk.

This is a rule-based business assessment, not a
trained machine-learning prediction.

### Manager-Level Recommendations

For high-risk customers, the application suggests:

- Customer outreach
- Re-engagement campaigns
- Contract conversion discussions
- Tech Support introduction
- Support issue resolution
- Retention follow-up

### Data Export

The dashboard supports CSV downloads for:

- High-risk customers
- Filtered customer records

## 6. Technology Stack

- Python
- NumPy
- Pandas
- Plotly
- Streamlit
- Google Colab
- GitHub
- Streamlit Community Cloud

## 7. Project Structure

The project follows this directory structure:

Ecommerce-Retention-Analytics/

    app.py
    requirements.txt
    README.md

    data/
        customer_data.csv

    notebooks/
        customer_retention_analysis.ipynb

The application reads the dataset from the data directory.

## 8. Local Installation and Execution

### Step 1: Install Anaconda

Install Anaconda or Miniconda.

Python 3.11 is recommended for local development.

### Step 2: Open Anaconda Prompt

Navigate to the project directory.

For a project stored in D drive:

    D:

    cd \Ecommerce-Retention-Analytics

Alternatively:

    cd /d D:\Ecommerce-Retention-Analytics

### Step 3: Create the environment

    conda create -n ecommerce-retention python=3.11 -y

### Step 4: Activate the environment

    conda activate ecommerce-retention

### Step 5: Install the dependencies

    python -m pip install -r requirements.txt

### Step 6: Run the application

    python -m streamlit run app.py

The application will open in the browser.

Local application URL:

    http://localhost:8501

Press Ctrl+C in Anaconda Prompt to stop the application.

## 9. GitHub Repository Setup

Create a GitHub repository named:

    Ecommerce-Retention-Analytics

Upload the following files and folders:

- app.py
- requirements.txt
- README.md
- data/customer_data.csv
- notebooks/customer_retention_analysis.ipynb

Ensure that app.py, requirements.txt, and README.md
are located in the repository root.

The dataset must remain inside the data directory.

## 10. Streamlit Community Cloud Deployment

Visit:

https://share.streamlit.io

Sign in using GitHub.

Create a new Streamlit application.

Select:

- Repository: Ecommerce-Retention-Analytics
- Branch: main
- Main file path: app.py

Click Deploy.

Streamlit Community Cloud installs the libraries
from requirements.txt and launches the application.

After deployment, a public URL ending in
.streamlit.app will be generated.

## 11. Google Colab Workflow

Google Colab is used for:

- Synthetic dataset generation
- Exploratory data analysis
- Data quality checks
- Customer churn analysis
- Python experimentation

The generated CSV file is downloaded from Colab
and placed inside the project's data directory.

The Streamlit application is then executed locally
using Anaconda Prompt.

## 12. Business Limitations

The dataset is synthetic.

The risk-scoring system uses predefined rules and
has not been statistically validated against
historical business data.

Annualised revenue at risk is an illustrative
estimate and should not be interpreted as an
actual revenue-loss forecast.

Before operational use, the company should:

- Validate the scoring logic using historical data.
- Evaluate model performance if machine learning is added.
- Assess false positives and false negatives.
- Review the business impact of retention campaigns.
- Monitor changes in customer behaviour.

## 13. Project Outcome

This project demonstrates the practical application
of Python, NumPy, Pandas, Plotly, and Streamlit
for business analytics.

It combines customer data analysis, revenue
intelligence, customer segmentation, interactive
dashboard development, and cloud deployment.

The project is designed as a portfolio demonstration
for Data Science and Business Analytics roles.