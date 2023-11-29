import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget
import pandas as pd

login_url = "https://pfm.smartcitylk.org/wp-login.php"
target_url = "https://pfm.smartcitylk.org/wp-admin/admin.php?page=generalInfo"
username = "kiruba00004@gmail.com"
password = "TAFpfm#99283"

data = []

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
        target_table = soup.find('table', {'id': 'table26'})
        x, y, z = 'Local Authority', 'Other Key', 'Another Key'
        local_authority_info = {cols[0].text.strip(): cols[1].text.strip() for cols in [row.find_all('td') for row in soup.find('table').find_all('tr') if len(row.find_all('td')) == 2]}

        N = (local_authority_info.get(x, f"{x} not found"))

        for row in target_table.find_all('tr')[1:]:
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

    else:
        print(f"Failed to retrieve the target webpage. Status code: {target_response.status_code}")
else:
    print("Login failed. Please check your credentials.")

# GUI Initialization
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('PFM App')

login_button = QPushButton('Login')
table = QTableWidget()
table.setColumnCount(3)
table.setHorizontalHeaderLabels(['Vehicle Type', f'In Running Condition: {N}', f'Not Running Condition: {N}'])
save_button = QPushButton('Save Data')

layout = QVBoxLayout()
layout.addWidget(login_button)
layout.addWidget(table)
layout.addWidget(save_button)

central_widget = QWidget()
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

table.setRowCount(len(data))

for i, row_data in enumerate(data):
    table.setItem(i, 0, QTableWidgetItem(row_data['Vehicle Type']))
    table.setItem(i, 1, QTableWidgetItem(str(row_data['In Running Condition'])))
    table.setItem(i, 2, QTableWidgetItem(str(row_data['Not Running Condition'])))

def save_data():
    if data:
        try:
            df = pd.read_excel('output_data.xlsx')
        except FileNotFoundError:
            df = pd.DataFrame()

        new_data = pd.DataFrame(data)
        df = pd.concat([df, new_data], axis=1)

        df.to_excel('output_data.xlsx', index=False)
        print("Data saved to output_data.xlsx")
    else:
        print("No data to display.")

save_button.clicked.connect(save_data)

window.show()
sys.exit(app.exec_())
