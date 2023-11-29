import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget
import pandas as pd

class PFMApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.login_url = "https://pfm.smartcitylk.org/wp-login.php"
        self.target_url = "https://pfm.smartcitylk.org/wp-admin/admin.php?page=generalInfo"
        self.username = "kiruba00004@gmail.com"
        self.password = "TAFpfm#99283"

        self.data = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PFM App')

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([f'Vehicle Type', 'In Running Condition', 'Not Running Condition'])

        save_button = QPushButton('Save Data', self)
        save_button.clicked.connect(self.save_data)

        layout = QVBoxLayout()
        layout.addWidget(login_button)
        layout.addWidget(self.table)
        layout.addWidget(save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login(self):
        session = requests.Session()

        login_data = {
            'log': self.username,
            'pwd': self.password,
            'wp-submit': 'Log In',
            'redirect_to': self.target_url,
        }

        login_response = session.post(self.login_url, data=login_data)

        if 'wp-admin' in login_response.url:
            target_response = session.get(self.target_url)

            if target_response.status_code == 200:
                soup = BeautifulSoup(target_response.content, 'html.parser')
                table = soup.find('table', {'id': 'table26'})
                x, y, z = 'Local Authority', 'Other Key', 'Another Key'
                local_authority_info = {cols[0].text.strip(): cols[1].text.strip() for cols in [row.find_all('td') for row in soup.find('table').find_all('tr') if len(row.find_all('td')) == 2]}
                N = (local_authority_info.get(x, f"{x} not found"))

                self.data = []

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

                        self.data.append({
                            'Vehicle Type': vehicle_type,
                            'In Running Condition': in_running_condition,
                            'Not Running Condition': not_running_condition
                        })

                self.display_data()
            else:
                print(f"Failed to retrieve the target webpage. Status code: {target_response.status_code}")
        else:
            print("Login failed. Please check your credentials.")

    def display_data(self):
        self.table.setRowCount(len(self.data))

        for i, row_data in enumerate(self.data):
            self.table.setItem(i, 0, QTableWidgetItem(row_data['Vehicle Type']))
            self.table.setItem(i, 1, QTableWidgetItem(str(row_data['In Running Condition'])))
            self.table.setItem(i, 2, QTableWidgetItem(str(row_data['Not Running Condition'])))

    def save_data(self):
        if self.data:
            try:
                df = pd.read_excel('output_data.xlsx')
            except FileNotFoundError:
                df = pd.DataFrame()

            new_data = pd.DataFrame(self.data)
            df = pd.concat([df, new_data], axis=1)

            df.to_excel('output_data.xlsx', index=False)
            print("Data saved to output_data.xlsx")
        else:
            print("No data to display.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pfm_app = PFMApp()
    pfm_app.show()
    sys.exit(app.exec_())
