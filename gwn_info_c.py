import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Define the login URL, target URL, and login credentials
login_url = "https://pfm.smartcitylk.org/wp-login.php"
target_url = "https://pfm.smartcitylk.org/wp-admin/admin.php?page=generalInfo"
username = "kiruba00004@gmail.com"
password = "TAFpfm#99283"

# Create a session to persist cookies across requests
session = requests.Session()

# Perform login
login_data = {
    'log': username,
    'pwd': password,
    'wp-submit': 'Log In',
    'redirect_to': target_url,
}
login_response = session.post(login_url, data=login_data)

# Check if the login was successful (check for a successful login response)
if 'wp-admin' in login_response.url:
    # Now, you can make a request to the target URL and scrape data
    target_response = session.get(target_url)

    # Check if the request to the target URL was successful (status code 200)
    if target_response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(target_response.content, 'html.parser')

        # Find the table with the specified ID
        table = soup.find('table', {'id': 'table26'})

        # Initialize a list to store the extracted data
        data = []

        # Iterate through the rows of the table
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')

            # Check if there are enough columns
            if len(columns) >= 4:
                vehicle_type = columns[0].text.strip()

                # Check if the input elements exist
                input_2 = columns[2].find('input')
                input_3 = columns[3].find('input')

                if input_2 and input_3:
                    in_running_condition = int(input_2.get('value', 0))
                    not_running_condition = int(input_3.get('value', 0))

                    # Append the data to the list
                    data.append({
                        'Vehicle Type': vehicle_type,
                        'In Running Condition': in_running_condition,
                        'Not Running Condition': not_running_condition
                    })

        # Print the extracted data in a table format
        if data:
            headers = data[0].keys()
            table_data = [[entry[col] for col in headers] for entry in data]

            # Print the data in a table format
            table = tabulate(table_data, headers, tablefmt='pretty')
            print(table)
        else:
            print("No data to display.")
    else:
        print(f"Failed to retrieve the target webpage. Status code: {target_response.status_code}")
else:
    print("Login failed. Please check your credentials.")
