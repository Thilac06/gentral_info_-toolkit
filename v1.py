
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pfm.smartcitylk.org/wp-login.php"
target_url = "https://pfm.smartcitylk.org/wp-admin/admin.php?page=generalInfo"
username = "kiruba00004@gmail.com"
password = "TAFpfm#99283"

payload = {
    'log': username,
    'pwd': password
}

session = requests.Session()

try:
    response = session.post(url, data=payload)
    response.raise_for_status()

    if response.ok:
        print("Login successful.")

        # Retrieve and print the form data
        page_response = session.get(target_url)
        page_response.raise_for_status()

        soup = BeautifulSoup(page_response.content, 'html.parser')
        form = soup.find('form', {'id': 't10'})

        if form:
            form_data = {}

            # Extract values from input fields
            input_fields = form.find_all('input')
            for field in input_fields:
                field_name = field.get('name')
                field_value = field.get('value')
                form_data[field_name] = field_value

            # Extract values from dropdowns
            select_fields = form.find_all('select')
            for field in select_fields:
                field_name = field.get('name')
                field_value = field.find('option', {'selected': 'selected'}).get('value')
                form_data[field_name] = field_value

            # Create a DataFrame from the extracted data
            df = pd.DataFrame(list(form_data.items()), columns=['Field', 'Value'])

            # Transpose the DataFrame for a vertical display
            df_transposed = df.transpose()

            # Print the transposed DataFrame
            print(tabulate(df_transposed, headers='firstrow', tablefmt='fancy_grid'))

            # Specify the Excel file pathr
            excel_file_path = 'output_data.xlsx'

            # Export the DataFrame to Excel using openpyxl
            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Print a message indicating successful export
            print(f"Data has been exported to {excel_file_path}")
        else:
            print("No form found on the page.")

    else:
        print(f"Login failed with status code {response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")

finally:
    session.close()
