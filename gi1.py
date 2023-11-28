import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

login_url = "https://pfm.smartcitylk.org/wp-login.php"
target_url = "https://pfm.smartcitylk.org/wp-admin/admin.php?page=generalInfo"
username = "kiruba00004@gmail.com"
password = "TAFpfm#99283"

session = requests.Session()

login_data = {
    'log': username,
    'pwd': password,
    'wp-submit': 'Log In',
    'redirect_to': target_url,
}
login_response = session.post(login_url, data=login_data)

if 'wp-admin' in login_response.url:
    target_response = session.get(target_url)

    if target_response.status_code == 200:
        soup = BeautifulSoup(target_response.content, 'html.parser')
        table = soup.find('table', {'id': 'table26'})

        data = []

        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')

            if len(columns) >= 4:
                vehicle_type = columns[0].text.strip()

                input_2 = columns[2].find('input')
                input_3 = columns[3].find('input')

                in_running_condition = int(input_2['value']) if input_2 and 'value' in input_2.attrs and input_2['value'].isdigit() else None

                not_running_condition = None
                if input_3 and 'value' in input_3.attrs:
                    not_running_condition = int(input_3['value']) if input_3['value'].isdigit() else None

                data.append({
                    'Vehicle Type': vehicle_type,
                    'In Running Condition': in_running_condition,
                    'Not Running Condition': not_running_condition
                })

        if data:
            # Check if the Excel file exists, if not create a new one
            try:
                df = pd.read_excel('output_data.xlsx')
            except FileNotFoundError:
                df = pd.DataFrame()

            new_data = pd.DataFrame(data)
            df = pd.concat([df, new_data], axis=1)

            # Save the DataFrame to an Excel file
            df.to_excel('output_data.xlsx', index=False)
            print("Data saved to output_data.xlsx")
        else:
            print("No data to display.")
    else:
        print(f"Failed to retrieve the target webpage. Status code: {target_response.status_code}")
else:
    print("Login failed. Please check your credentials.")
