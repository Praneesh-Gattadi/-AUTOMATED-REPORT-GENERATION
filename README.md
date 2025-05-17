# AUTOMATED-REPORT-GENERATION

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: Gattadi Praneesh

*INTERN ID*: CT04DM1319

*DOMAIN*: Python Programming

*DURATION*: 4 Weeks

*MENTOR*: NEELA SANTOSH


# Employee Analytics Report Generator

## Overview

This project is a **Python-based reporting tool** developed as part of the CodTech Python Internship (Task 2). It reads employee data from a structured CSV file, performs comprehensive
analysis, and generates a well-formatted PDF report using the **FPDF** library.

The report includes key metrics such as average salary, performance ratings, and employee tenure, broken down by department. Additional sections present the top-performing employees,
tenure distribution, and a sample dataset table — all styled with clear, readable formatting. The project aims to demonstrate the capability to automate data analysis and reporting
through Python scripting.

This tool is intended for HR departments, team leads, or data analysts who require a fast and reliable way to process employee data and create actionable reports.

## Features

- 📊**Data Analysis**: Aggregates and calculates metrics like:
  - Average salary, rating, and tenure
  - Department-wise breakdown
  - Salary extremes (min/max)
  - Tenure distribution
  - Top 5 performers

- 🧾 **Formatted PDF Generation**:
  - Sectioned layout with titles and tables
  - Executive summary
  - Departmental analysis table
  - Top performer highlights
  - Employee tenure categorization
  - Sample employee data

- ✅ **Automated Execution**:
  - Runs as a standalone script
  - Error handling for missing/invalid files
  - Clean and reusable code structure

## Technologies Used

- **Python 3**
- **FPDF** (for PDF creation)
- **CSV** module (for reading input data)
- **Datetime** (for date and tenure calculations)

## File Structure

```
project-directory/
│
├── data.csv                         # Input CSV file with employee data
├── employee_analytics_report.pdf   # Generated report (sample output)
└── report_generator.py             # Main script (shared above)
```

## CSV Format (Input)

The script expects a `data.csv` file with the following headers:

- `Name`
- `Department`
- `Salary`
- `JoinDate` (Format: YYYY-MM-DD)
- `PerformanceRating`

Sample:

```csv
Name,Department,Salary,JoinDate,PerformanceRating
John Doe,Engineering,75000,2020-05-15,4.2
Jane Smith,Marketing,68000,2019-11-22,3.8
```

## How to Run

1. **Install dependencies**:
   ```
   pip install fpdf
   ```

2. **Ensure the CSV is named** `data.csv` and placed in the same directory.

3. **Run the script**:
   ```
   python report_generator.py
   ```

4. **Output**:
   A PDF report named `employee_analytics_report.pdf` will be generated in the same directory.

## Report Sections

The PDF is broken down into the following segments:

- **Title Page & Summary**:
  - Timestamped generation
  - Employee count, department count
  - A brief executive overview

- **Executive Summary**:
  - Average and extreme salary values
  - Average performance rating and tenure
  - Most and least tenured employees

- **Departmental Analysis**:
  - Employees per department
  - Average department salary, performance, and tenure

- **Top Performers**:
  - Top 5 employees based on rating and salary

- **Tenure Distribution**:
  - Employees grouped by:
    - `<1 year`
    - `1-3 years`
    - `3+ years`

- **Sample Data Table**:
  - Displays a preview of the first 10 employee records

## Error Handling

- If the CSV file is not found, the script will gracefully notify the user.
- Missing or malformed data entries are skipped or defaulted appropriately.
- All critical exceptions are caught and logged during runtime.


## License

This project is intended for educational and internship evaluation purposes. You are free to adapt or extend it for learning or internal use.

## Output

[employee_analytics_report.pdf](https://github.com/user-attachments/files/20265294/employee_analytics_report.pdf)
