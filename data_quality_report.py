import pandas as pd
import csv

# Path to your file
FILE_PATH = "data/data_quality_report.csv"   # change to your actual file

def view_csv_file(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    print("\nAvailable Columns:", df.columns.tolist())
    print("\nFirst 5 Rows:")
    print(df.head())

    # Read each sheet
    for sheet in xls.sheet_names:
        print(f"\n===== Sheet: {sheet} =====")
        df = pd.read_csv(file_path, sheet_name=sheet)
        print(df.head())   # show first 5 rows

if __name__ == "__main__":
    view_csv(FILE_PATH)




#---------------
import pandas as pd
import csv

FILE_PATH = "data/customer_data.xlsx"   # update path

def data_quality_report(file_path):
    xls = pd.ExcelFile(file_path)
    print("\nSheets found:", xls.sheet_names)

    for sheet in xls.sheet_names:
        print(f"\n==============================")
        print(f"📄 DATA QUALITY REPORT — {sheet}")
        print(f"==============================")

        df = pd.read_excel(file_path, sheet_name=sheet)

        print("\n▶ Shape:", df.shape)

        print("\n▶ Column Data Types:")
        print(df.dtypes)

        print("\n▶ Missing Values:")
        print(df.isna().sum())

        print("\n▶ Duplicate Rows:")
        print(df.duplicated().sum())

        print("\n▶ Basic Statistics:")
        print(df.describe(include="all"))

        print("\n----------------------------------")

if __name__ == "__main__":
    data_quality_report(FILE_PATH)
