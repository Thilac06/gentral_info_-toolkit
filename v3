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

            # Transpose the DataFrame for a horizontal display
            df_transposed = df.transpose()

            # Rename columns to be numerical
            df_transposed.columns = range(1, len(df_transposed.columns) + 1)

            # Print the transposed DataFrame
            print(tabulate(df_transposed, headers='firstrow', tablefmt='fancy_grid'))

            # Specify the Excel file path for form data
            excel_file_path = 'form_data_output.xlsx'

            # Export the transposed DataFrame to Excel using openpyxl
            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                df_transposed.to_excel(writer, index=False, sheet_name='FormData')

            # Print a message indicating successful export
            print(f"Form data has been exported to {excel_file_path}")

            # Extract details from the HTML structure
            details = {}

            sections = soup.find_all('section', {'class': 'content-header'})
            for section in sections:
                header = section.find('h3')
                if header and "Part B : Service related assets and infrastructure of LAs" in header.text:
                    form = section.find('form', {'id': 't37'})
                    if form:
                        tables = form.find_all('table')
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows:
                                columns = row.find_all(['td', 'th'])
                                if len(columns) == 3:
                                    field_name = columns[0].text.strip()
                                    input_tag = columns[2].find('input')
                                    if input_tag:
                                        field_value = input_tag.get('value', '').strip()
                                        details[field_name] = field_value

            # Create a DataFrame from the extracted details
            details_df = pd.DataFrame(list(details.items()), columns=['Field', 'Value'])

            # Transpose the DataFrame for a horizontal display
            details_df_transposed = details_df.transpose()

            # Rename columns to be numerical
            details_df_transposed.columns = range(1, len(details_df_transposed.columns) + 1)

            # Print the transposed DataFrame
            print(tabulate(details_df_transposed, headers='firstrow', tablefmt='fancy_grid'))

            # Specify the Excel file path for details
            details_excel_file_path = 'details_output.xlsx'

            # Export the transposed DataFrame to Excel using openpyxl
            with pd.ExcelWriter(details_excel_file_path, engine='openpyxl') as writer:
                details_df_transposed.to_excel(writer, index=False, sheet_name='Details')

            # Print a message indicating successful export
            print(f"Details have been exported to {details_excel_file_path}")

        else:
            print("No form found on the page.")

    else:
        print(f"Login failed with status code {response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")

finally:
    session.close()
