import os
import pandas as pd

def compare_results():
    # Define the base directory
    base_dir = "Shift_Explanation/Results_Experiments"

    # List to hold DataFrames
    dfs = []
    baseline_df = None

    # Helper function to read and process CSV files
    def read_and_process_csv(file_path, name):
        df = pd.read_csv(file_path)
        df.set_index('Measurement', inplace=True)  # Set 'Measurement' as the index
        df.rename(columns={"Values": name}, inplace=True)  # Rename 'Values' column to the folder name
        return df

    # Handle the Baseline folder separately
    baseline_csv_path = os.path.join(base_dir, "Baseline", "Shift_Explanation", "regression_results.csv")
    if os.path.exists(baseline_csv_path):
        baseline_df = read_and_process_csv(baseline_csv_path, "Baseline")
    else:
        raise ValueError("Baseline folder not found.")

    # Iterate through all directories in the base directory
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            # Check if directory name starts with "Set_"
            if dir_name.startswith("Set_"):
                # Construct the path to the target CSV file
                csv_path = os.path.join(root, dir_name, "Shift_Explanation", "regression_results.csv")
                # Check if the file exists
                if os.path.exists(csv_path):
                    # Read and process the CSV file
                    df = read_and_process_csv(csv_path, dir_name)
                    dfs.append(df)

    # Ensure the baseline_df is the first dataframe in the list for concatenation
    dfs.insert(0, baseline_df)

    # Merge all DataFrames on the index ('Measurement' column)
    combined_df = pd.concat(dfs, axis=1)
    print(combined_df)

    # Define the output path
    output_path = os.path.join(base_dir, "combined_regression_results.csv")

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_path)

    print(f"Combined CSV saved to {output_path}")

# compare_results()
