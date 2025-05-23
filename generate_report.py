from fpdf import FPDF
from datetime import datetime, date
import csv

# Define a custom PDF class using FPDF
class EmployeeAnalyticsReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_title("Employee Analytics Report")
        self.set_author("Reporting System")

    # Footer for each page (displays page number and generation time)
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 0, "C")

    # Add section title with styling
    def add_section(self, title):
        self.ln(10)
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.cell(0, 1, "", "T")
        self.ln(5)

    # Display metrics in a horizontal block
    def add_metrics(self, metrics):
        self.set_font("Arial", "", 11)
        col_width = 190 / len(metrics)
        for label, value in metrics:
            self.set_fill_color(230, 240, 255)
            self.cell(col_width, 8, f"{label}:", border=1, align="R", fill=True)
            self.set_fill_color(255, 255, 255)
            self.cell(col_width, 8, str(value), border=1, align="L", ln=False, fill=True)
        self.ln()

    # Create a table with headers and data rows
    def add_table(self, headers, rows, col_widths):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(220, 230, 255)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, align="C", fill=True)
        self.ln()
        self.set_font("Arial", "", 11)
        for row in rows:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 8, str(cell), border=1)
            self.ln()
        self.ln(5)

# Calculate years of service (tenure) from join date
def calculate_tenure(join_date):
    try:
        date_joined = datetime.strptime(join_date, "%Y-%m-%d").date()
        return (date.today() - date_joined).days / 365.25
    except:
        return 0

# Analyze the employee data and return summary and departmental metrics
def analyze_employees(data):
    departments = {}

    for emp in data:
        emp['Salary'] = float(emp.get('Salary', 0))
        emp['PerformanceRating'] = float(emp.get('PerformanceRating', 0))
        emp['Tenure'] = calculate_tenure(emp.get('JoinDate', ''))

        dept = emp['Department']
        if dept not in departments:
            departments[dept] = {'count': 0, 'salaries': [], 'ratings': [], 'tenures': [], 'employees': []}

        d = departments[dept]
        d['count'] += 1
        d['salaries'].append(emp['Salary'])
        d['ratings'].append(emp['PerformanceRating'])
        d['tenures'].append(emp['Tenure'])
        d['employees'].append(emp)

    # Calculate department averages
    for d in departments.values():
        d['avg_salary'] = sum(d['salaries']) / d['count']
        d['avg_rating'] = sum(d['ratings']) / d['count']
        d['avg_tenure'] = sum(d['tenures']) / d['count']

    salaries = [e['Salary'] for e in data]
    ratings = [e['PerformanceRating'] for e in data]
    tenures = [e['Tenure'] for e in data]

    return {
        'report_date': datetime.now().strftime("%B %d, %Y at %H:%M:%S"),
        'total_employees': len(data),
        'departments': departments,
        'overall': {
            'avg_salary': sum(salaries) / len(salaries),
            'avg_rating': sum(ratings) / len(ratings),
            'avg_tenure': sum(tenures) / len(tenures),
            'max_salary': max(salaries),
            'min_salary': min(salaries),
            'top_performers': sorted(data, key=lambda x: (-x['PerformanceRating'], -x['Salary']))[:5],
            'tenure_distribution': {
                '<1 year': len([t for t in tenures if t < 1]),
                '1-3 years': len([t for t in tenures if 1 <= t < 3]),
                '3+ years': len([t for t in tenures if t >= 3])
            }
        }
    }

# Main function to generate the report
def generate_report(input_csv="data.csv", output_pdf="employee_analytics_report.pdf"):
    try:
        # Read CSV data
        with open(input_csv, newline='') as file:
            reader = csv.DictReader(file)
            employees = [row for row in reader if row.get('Name')]

        if not employees:
            print("No data found.")
            return False

        # Analyze the data
        analysis = analyze_employees(employees)
        pdf = EmployeeAnalyticsReport()
        pdf.add_page()

        # Report title
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 15, "Employee Analytics Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Generated on: {analysis['report_date']}", ln=True, align="C")
        pdf.ln(10)
        pdf.multi_cell(0, 8, f"This report contains an analysis of {analysis['total_employees']} employees across {len(analysis['departments'])} departments.")

        # Executive Summary
        pdf.add_section("Executive Summary")
        pdf.add_metrics([
            ("Total Employees", analysis['total_employees']),
            ("Average Salary", f"${analysis['overall']['avg_salary']:,.2f}"),
            ("Average Rating", f"{analysis['overall']['avg_rating']:.1f}/5.0"),
            ("Average Tenure", f"{analysis['overall']['avg_tenure']:.1f} years")
        ])
        pdf.add_metrics([
            ("Highest Salary", f"${analysis['overall']['max_salary']:,.2f}"),
            ("Lowest Salary", f"${analysis['overall']['min_salary']:,.2f}"),
            ("Newest Employee", min(e['JoinDate'] for e in employees)),
            ("Most Tenured", max(e['JoinDate'] for e in employees))
        ])

        # Departmental Analysis
        pdf.add_section("Departmental Analysis")
        dept_rows = [
            [dept, d['count'], f"${d['avg_salary']:,.2f}", f"{d['avg_rating']:.1f}", f"{d['avg_tenure']:.1f} years"]
            for dept, d in analysis['departments'].items()
        ]
        pdf.add_table(["Department", "Employees", "Avg Salary", "Avg Rating", "Avg Tenure"], dept_rows, [50, 30, 40, 30, 40])

        # Top Performers
        pdf.add_section("Top Performers by Rating")
        top_rows = [
            [e['Name'], e['Department'], f"${e['Salary']:,.2f}", e['PerformanceRating'], f"{e['Tenure']:.1f} years"]
            for e in analysis['overall']['top_performers']
        ]
        pdf.add_table(["Name", "Department", "Salary", "Rating", "Tenure"], top_rows, [50, 30, 40, 30, 40])

        # Tenure Distribution
        pdf.add_section("Employee Tenure Distribution")
        dist_rows = [[k, v] for k, v in analysis['overall']['tenure_distribution'].items()]
        pdf.add_table(["Tenure Range", "Employee Count"], dist_rows, [60, 60])

        # Sample Data
        pdf.add_section("Employee Sample Data")
        sample_rows = [
            [e['Name'], e['Department'], f"${e['Salary']:,.2f}", e['JoinDate']]
            for e in employees[:10]
        ]
        pdf.add_table(["Name", "Department", "Salary", "Join Date"], sample_rows, [50, 40, 40, 60])

        # Output the PDF
        pdf.output(output_pdf)
        print(f"Report generated: {output_pdf}")
        return True

    except FileNotFoundError:
        print(f"File not found: {input_csv}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Entry point for the script
if __name__ == "__main__":
    generate_report()
