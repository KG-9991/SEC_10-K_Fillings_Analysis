import os
from extract_debt_to_equity import Extract_Debt_To_Equity
def list_subdirectories(directory):
    """List only the subdirectories in the given directory."""
    # List all items in the directory
    all_items = os.listdir(directory)
    # Filter and keep only directories
    subdirs = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]
    return subdirs

def main():
    directory_for_msft = "./sec-edgar-filings/MSFT/10-K"
    directory_for_tsla = "./sec-edgar-filings/TSLA/10-K"
    subdirectories_for_msft = list_subdirectories(directory_for_msft)
    subdirectories_for_tsla = list_subdirectories(directory_for_tsla)

    dte_vals_tsla = {}
    dte_vals_msft = {}

    for sub_dir in subdirectories_for_tsla:
        year = sub_dir.split('-')[1]
        file_path_tsla = f'{directory_for_tsla}/{sub_dir}/full-submission.txt'
        liab_and_equity = Extract_Debt_To_Equity("TSLA",file_path_tsla)
        dte_vals_tsla[year] = liab_and_equity.extract_dte_ratio()
    print(dte_vals_tsla)

# Example usage
if __name__ == "__main__":
    main()
