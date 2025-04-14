import os
import pandas as pd
from datetime import datetime

def find_folders_with_problematic_chars(target_folder):
    # List of characters that may cause issues; adjust if needed.
    problematic_chars = [
        # " ",  # Space
        # ".",  # Dot
        "(", ")",  # Parentheses
        "[", "]"   # Square brackets
    ]

    results = []

    # Recursively traverse through subfolders in the target folder
    for root, dirs, files in os.walk(target_folder):
        for d in dirs:
            folder_path = os.path.join(root, d)
            # Exclude if the folder is exactly the target folder
            if os.path.abspath(folder_path) == os.path.abspath(target_folder):
                continue
            # Check if the folder name contains any problematic character
            if any(char in d for char in problematic_chars):
                mtime = os.path.getmtime(folder_path)
                # Format the modification date as "yyyy-mm-dd hh:mm"
                updated_at = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                results.append([folder_path, updated_at])

    # Convert the list into a pandas DataFrame
    df = pd.DataFrame(results, columns=["Path", "Modified Date"])
    # Remove the target_folder part from each Path, returning relative paths
    df["Path"] = df["Path"].apply(lambda x: os.path.relpath(x, target_folder))
    return df

if __name__ == "__main__":
    target_folder = r"C:\Users\ky090\OneDrive - The University of Texas at Austin"
    df = find_folders_with_problematic_chars(target_folder)
    display(df.head(20))
