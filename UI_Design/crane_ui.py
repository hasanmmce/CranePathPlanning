import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, 
                             QVBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QFormLayout, QStackedWidget, QMessageBox, QCheckBox, 
                             QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

# Utility functions for credentials storage (as in previous example)
def load_saved_credentials():
    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
            return username, password
    return '', ''

def save_credentials(username, password):
    with open('credentials.txt', 'w') as f:
        f.write(f"{username}\n{password}\n")

def clear_credentials():
    if os.path.exists('credentials.txt'):
        os.remove('credentials.txt')

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Construction Planning Tool')
        self.setGeometry(100, 100, 800, 600)
        
        # Create a stacked widget to switch between login and main application
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Login and Main Application Widgets
        self.create_login_widget()
        self.create_main_application_widget()

        # Add both widgets to the stacked widget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_application_widget)
        
        # Show the login screen first
        self.stacked_widget.setCurrentWidget(self.login_widget)

        # Load saved credentials if any
        saved_username, saved_password = load_saved_credentials()
        if saved_username:
            self.username.setText(saved_username)
        if saved_password:
            self.password.setText(saved_password)
            self.save_password_checkbox.setChecked(True)

    def create_login_widget(self):
        # Login Widget
        self.login_widget = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Username and Password fields
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # Save Password Checkbox
        self.save_password_checkbox = QCheckBox('Save Password')

        form_layout.addRow('Username:', self.username)
        form_layout.addRow('Password:', self.password)
        form_layout.addRow('', self.save_password_checkbox)

        # Login Button
        self.login_button = QPushButton('Login')
        self.login_button.setFixedWidth(100)
        form_layout.addRow('', self.login_button)

        # Set margin for a more professional layout, aligning it at the top
        layout.setContentsMargins(100, 50, 100, 50)  # Add margin
        layout.addLayout(form_layout)
        layout.addStretch()

        self.login_button.clicked.connect(self.check_credentials)
        self.login_widget.setLayout(layout)

    def check_credentials(self):
        # For now, we're using fixed credentials. You can replace this with a more secure authentication method.
        if self.username.text() == 'admin' and self.password.text() == 'password':
            # If the "Save Password" checkbox is checked, save the credentials
            if self.save_password_checkbox.isChecked():
                save_credentials(self.username.text(), self.password.text())
            else:
                clear_credentials()
            # If login is successful, switch to the main application screen
            self.logged_in_user.setText(f"Logged in as: {self.username.text()}")  # Show logged-in user
            self.stacked_widget.setCurrentWidget(self.main_application_widget)
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect Username or Password')

    def create_main_application_widget(self):
        # Main Application Widget
        self.main_application_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top section to show the logged-in user
        self.logged_in_user = QLabel("")
        self.logged_in_user.setFont(QFont("Arial", 8, QFont.StyleItalic))
        # make the font color gray
        palette = QPalette()
        palette.setColor(QPalette.Foreground, QColor('gray')) 
        self.logged_in_user.setPalette(palette) # set the color
        
        main_layout.addWidget(self.logged_in_user)

        # Create Tabs
        self.tabs = QTabWidget()

        # Create Tabs: Applications and Info
        self.create_application_tab()
        self.create_info_tab()

        # Add logout button
        self.logout_button = QPushButton('Logout')
        self.logout_button.setFixedHeight(50)
        self.logout_button.clicked.connect(self.logout)

        # Footer message (gray text)
        footer_layout = QHBoxLayout()
        footer_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        footer_label = QLabel('©Monjurul Hasan')
        footer_label.setAlignment(Qt.AlignCenter)

        # Set gray color for the footer text
        palette = QPalette()
        palette.setColor(QPalette.Foreground, QColor('gray'))
        footer_label.setPalette(palette)

        footer_layout.addWidget(footer_label)

        # Add everything to the main layout
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.logout_button)
        main_layout.addLayout(footer_layout)

        
        self.main_application_widget.setLayout(main_layout)

    def logout(self):
        # Clear saved credentials on logout
        clear_credentials()
        self.username.clear()
        self.password.clear()
        self.save_password_checkbox.setChecked(False)
        self.logged_in_user.setText('')  # Clear logged-in user display
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def create_application_tab(self):
        # Application Tab
        self.application_tab = QWidget()
        self.tabs.addTab(self.application_tab, "Applications")

        layout = QVBoxLayout()

        # Mat Layout Planning (Enabled)
        self.mat_layout_button = QPushButton('Mat Layout Planning')
        self.mat_layout_button.setFixedHeight(50)
        self.mat_layout_button.clicked.connect(self.open_mat_layout_planning)
        layout.addWidget(self.mat_layout_button)
        
        # Mat Design (Enabled)
        self.mat_design_button = QPushButton('Mat Design')
        self.mat_design_button.setFixedHeight(50)
        self.mat_design_button.clicked.connect(self.open_mat_design)
        layout.addWidget(self.mat_design_button)
        
        # Crane Lift Calculation (Grayed out)
        self.crane_lift_button = QPushButton('Crane Lift Calculation')
        self.crane_lift_button.setEnabled(False)
        self.crane_lift_button.setFixedHeight(50)
        layout.addWidget(self.crane_lift_button)
        
        # Soil Bearing Capacity Calculation (Grayed out)
        self.soil_bearing_button = QPushButton('Soil Bearing Capacity Calculation')
        self.soil_bearing_button.setEnabled(False)
        self.soil_bearing_button.setFixedHeight(50)
        layout.addWidget(self.soil_bearing_button)
        
        layout.addStretch()
        self.application_tab.setLayout(layout)

    def create_info_tab(self):
        # Info Tab with Professional Layout
        self.info_tab = QWidget()
        self.tabs.addTab(self.info_tab, "Info")

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Contact Information")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 10))

        # Information labels with consistent font size and reduced spacing
        contact_info_layout = QFormLayout()
        contact_info_layout.setHorizontalSpacing(30)
        contact_info_layout.setVerticalSpacing(10)  # Reduced spacing

        # Set font style for each field
        info_font = QFont("Arial", 9)

        # Add the info labels with clickable website link
        developed_by = QLabel("Developed by:")
        developed_by.setFont(info_font)
        contact_info_layout.addRow(developed_by, QLabel("Monjurul Hasan, PhD, PEng, PMP"))

        email_label = QLabel("Email:")
        email_label.setFont(info_font)
        contact_info_layout.addRow(email_label, QLabel("monjurul.hasan@outlook.com"))

        website_label = QLabel("Website:")
        website_label.setFont(info_font)
        website_link = QLabel("<a href='https://sites.google.com/site/mmhasance'>https://sites.google.com/site/mmhasance</a>")
        website_link.setOpenExternalLinks(True)
        contact_info_layout.addRow(website_label, website_link)

        phone_label = QLabel("Phone:")
        phone_label.setFont(info_font)
        contact_info_layout.addRow(phone_label, QLabel("+17809191917"))

        # Set margins to align information at the top with a good margin
        layout.setContentsMargins(50, 20, 50, 20)  # Good margin on all sides
        
        # Center and add spacing
        #layout.addStretch()
        layout.addWidget(title_label)
        layout.addLayout(contact_info_layout)
        layout.addStretch()

        self.info_tab.setLayout(layout)

    # Function to open the Mat Layout Planning window
    def open_mat_layout_planning(self):
        self.mat_layout_window = QWidget()
        self.mat_layout_window.setWindowTitle("Mat Layout Planning")
        self.mat_layout_window.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Mat Layout Planning Interface'))
        self.mat_layout_window.setLayout(layout)
        self.mat_layout_window.show()

    # Function to open the Mat Design window
    def open_mat_design(self):
        self.mat_design_window = QWidget()
        self.mat_design_window.setWindowTitle("Mat Design")
        self.mat_design_window.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Mat Design Interface'))
        self.mat_design_window.setLayout(layout)
        self.mat_design_window.show()

# Main Program Execution
def main():
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
