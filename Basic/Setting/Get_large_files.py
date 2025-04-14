import os
import pandas as pd
from datetime import datetime

def get_large_excel_files(folder_path, min_size_mb=10):
    excel_extensions = ('.xls', '.xlsx', '.xlsm', '.xlsb', '.csv','.ipynb','.pdf')
    data = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(excel_extensions):
                file_path = os.path.join(root, file)
                size_bytes = os.path.getsize(file_path)

                # Convert bytes to megabytes
                size_mb = size_bytes / (1024 * 1024)

                if size_mb >= min_size_mb:
                    size_mb = round(size_mb, 1)
                    file_name = file
                    folder = root
                    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")

                    data.append([
                        file_name,
                        folder,
                        modified_time,
                        size_mb
                    ])

    df = pd.DataFrame(data, columns=['File_Name', 'Folder', 'Modified_Date', 'Size(MB)'])
    df.sort_values(by='Size(MB)', ascending=False, inplace=True)
    df = df.reset_index(drop=True)

    return df

if __name__ == "__main__":
    target_folder = r"C:\Users\ky090\OneDrive - The University of Texas at Austin"
    df = get_large_excel_files(target_folder, min_size_mb=1)
    display(df)
