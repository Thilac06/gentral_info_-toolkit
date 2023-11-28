import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


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

       
        in_running_data = []
        not_running_data = []

      
        for row in table.find_all('tr')[1:]:  
            columns = row.find_all('td')

           
            if len(columns) >= 4:
                vehicle_type = columns[0].text.strip()

                
                input_2 = columns[2].find('input')
                input_3 = columns[3].find('input')

                if input_2 and input_3:
                    in_running_condition = int(input_2.get('value', 0))
                    not_running_condition = int(input_3.get('value', 0))

                    
                    in_running_data.append({
                        'Vehicle Type': vehicle_type,
                        'In Running Condition': in_running_condition,
                    })

                    not_running_data.append({
                        'Vehicle Type': vehicle_type,
                        'Not Running Condition': not_running_condition,
                    })


        if in_running_data and not_running_data:
            headers_in_running = list(in_running_data[0].keys())
            table_data_in_running = [[entry[col] for col in headers_in_running] for entry in in_running_data]

            headers_not_running = list(not_running_data[0].keys())
            table_data_not_running = [[entry[col] for col in headers_not_running] for entry in not_running_data]

           
            table_combined = [row_in_running + row_not_running for row_in_running, row_not_running in zip(table_data_in_running, table_data_not_running)]

           
            table_combined_headers = headers_in_running + headers_not_running
            table_combined_output = tabulate(table_combined, table_combined_headers, tablefmt='pretty')
            
           
            print("Combined Tables:")
            print(table_combined_output)

        elif in_running_data:
            headers = list(in_running_data[0].keys())
            table_data = [[entry[col] for col in headers] for entry in in_running_data]

           
            table_in_running = tabulate(table_data, headers, tablefmt='pretty')
            print("In Running Condition Table:")
            print(table_in_running)

        elif not_running_data:
            headers = list(not_running_data[0].keys())
            table_data = [[entry[col] for col in headers] for entry in not_running_data]

           
            table_not_running = tabulate(table_data, headers, tablefmt='pretty')
            print("Not Running Condition Table:")
            print(table_not_running)

        else:
            print("No data to display.")

    else:
        print(f"Failed to retrieve the target webpage. Status code: {target_response.status_code}")
else:
    print("Login failed. Please check your credentials.")
