import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem, 
                             QFileDialog, QTabWidget, QTextEdit, QHeaderView, QSplitter, 
                             QRadioButton, QButtonGroup, QLineEdit, QHBoxLayout, QSlider)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import griddata
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

class MatLayoutPlanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mat Layout Plan')
        self.setGeometry(100, 100, 1200, 800)

        # Create the main tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.create_mat_layout_tab()
        self.create_help_tab()

        # Status bar to show messages, occupying 20% of window height and full width
        self.status_bar = QTextEdit(self)
        self.status_bar.setFixedHeight(int(self.height() * 0.20))  # 20% of the window height
        self.status_bar.setReadOnly(True)
        self.status_bar.setPlaceholderText("Status messages will appear here...")
        self.status_bar.setStyleSheet("background-color: #f0f0f0; font-family: 'Courier';")
        self.status_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.statusBar().addPermanentWidget(self.status_bar, 1)  # Full width status bar
        self.popout_window = None
        self.popout_2d_window = None
        self.show()

    def create_mat_layout_tab(self):
        # Main widget for mat layout tab
        mat_layout_tab = QWidget()
        main_layout = QVBoxLayout()

        # Splitter to divide table and plot
        splitter = QSplitter(Qt.Horizontal)

        # Left section: Import data and data table
        left_section = QVBoxLayout()
        import_button = QPushButton('Import Data')
        import_button.clicked.connect(self.import_data)
        left_section.addWidget(import_button)

        # Instructions for correct data format
        instructions = QLabel("Data format should be CSV with columns: x, y, z.")
        left_section.addWidget(instructions)

        self.table_widget = QTableWidget(0, 3)
        self.table_widget.setHorizontalHeaderLabels(['x', 'y', 'z'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_section.addWidget(self.table_widget)

        left_widget = QWidget()
        left_widget.setLayout(left_section)
        
        # Add the left section (2/3 of the width)
        splitter.addWidget(left_widget)

        # Right section: Plot area
        right_section = QVBoxLayout()
        plot_button = QPushButton('Plot Graph')
        plot_button.clicked.connect(self.plot_graph)
        right_section.addWidget(plot_button)

        # Radio buttons to select 2D plane, arranged in a horizontal layout
        radio_button_layout = QHBoxLayout()  # Horizontal layout for radio buttons
        plane_group = QButtonGroup(self)
        self.xy_plane_radio = QRadioButton("XY Plane", checked=True)
        self.xz_plane_radio = QRadioButton("XZ Plane")
        self.yz_plane_radio = QRadioButton("YZ Plane")

        plane_group.addButton(self.xy_plane_radio)
        plane_group.addButton(self.xz_plane_radio)
        plane_group.addButton(self.yz_plane_radio)

        # Add radio buttons to the horizontal layout
        radio_button_layout.addWidget(self.xy_plane_radio)
        radio_button_layout.addWidget(self.xz_plane_radio)
        radio_button_layout.addWidget(self.yz_plane_radio)

        # Add the radio button layout to the right section
        right_section.addLayout(radio_button_layout)

        # Plot sections
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        right_section.addWidget(self.canvas)

        self.figure_2d = plt.figure()
        self.canvas_2d = FigureCanvas(self.figure_2d)
        right_section.addWidget(self.canvas_2d)

        # Pop out button
        self.popout_button = QPushButton('Pop Out Graph')
        self.popout_button.clicked.connect(self.pop_out_graph)
        self.popout_button.setEnabled(False)
        right_section.addWidget(self.popout_button)

        right_widget = QWidget()
        right_widget.setLayout(right_section)
        
        # Add the right section (1/3 of the width)
        splitter.addWidget(right_widget)

        # Set proportions: Left section (2/3), Right section (1/3)
        splitter.setStretchFactor(0, 2)  # Left section gets 2/3
        splitter.setStretchFactor(1, 1)  # Right section gets 1/3

        main_layout.addWidget(splitter)
        mat_layout_tab.setLayout(main_layout)
        self.tabs.addTab(mat_layout_tab, "Mat Layout Plan")







    def create_help_tab(self):
        help_tab = QWidget()
        help_layout = QVBoxLayout()
        help_layout.addWidget(QLabel("Help information will be available here."))
        help_tab.setLayout(help_layout)
        self.tabs.addTab(help_tab, "Help")

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV file', '', 'CSV files (*.csv)')
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                if set(['x', 'y', 'z']).issubset(self.data.columns):
                    self.status_bar.append("Data imported successfully.")
                    self.display_data()
                else:
                    self.status_bar.append("Error: Incorrect data format. Required columns: x, y, z.")
            except Exception as e:
                self.status_bar.append(f"Error loading file: {e}")

    def display_data(self):
        self.table_widget.setRowCount(len(self.data))
        for i, row in self.data.iterrows():
            self.table_widget.setItem(i, 0, QTableWidgetItem(str(row['x'])))
            self.table_widget.setItem(i, 1, QTableWidgetItem(str(row['y'])))
            self.table_widget.setItem(i, 2, QTableWidgetItem(str(row['z'])))

    def plot_graph(self):
        self.plot_3d_graph()
        self.update_2d_plot()
        self.popout_button.setEnabled(True)
        self.status_bar.append("3D and 2D graphs plotted.")

    def plot_3d_graph(self, figure=None):
        try:
            if figure is None:
                figure = self.figure
            figure.clear()
            ax = figure.add_subplot(111, projection='3d')
            x, y, z = self.data['x'].values, self.data['y'].values, self.data['z'].values
            ax.plot_trisurf(x, y, z, cmap='viridis')
            if figure == self.figure:
                self.canvas.draw()
        except Exception as e:
            self.status_bar.append(f"Error plotting 3D graph: {e}")




    def update_2d_plot(self, figure_2d=None):
        try:
            if figure_2d is None:
                figure_2d = self.figure_2d
            figure_2d.clear()  # Clear any previous plots
            ax_2d = figure_2d.add_subplot(111)
            x, y, z = self.data['x'].values, self.data['y'].values, self.data['z'].values

            # Define grid points for interpolation
            grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

            # Use griddata to interpolate Z values
            grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

            if self.xy_plane_radio.isChecked():
                contour = ax_2d.contour(grid_x, grid_y, grid_z, cmap='viridis')  # Create the contour plot
                ax_2d.clabel(contour, inline=True, fontsize=10)  # Add labels to contour lines
                ax_2d.set_xlabel('X')
                ax_2d.set_ylabel('Y')
                ax_2d.set_title('Contour Plot')
                self.status_bar.append("2D XY Plane labeled contour plot created.")

            elif self.xz_plane_radio.isChecked():
                contour = ax_2d.contour(grid_x, grid_y, grid_z, cmap='plasma')
                ax_2d.clabel(contour, inline=True, fontsize=10)
                ax_2d.set_xlabel('X')
                ax_2d.set_ylabel('Z')
                ax_2d.set_title('Contour Plot')
                self.status_bar.append("2D XZ Plane labeled contour plot created.")

            elif self.yz_plane_radio.isChecked():
                contour = ax_2d.contour(grid_x, grid_y, grid_z, cmap='cividis')
                ax_2d.clabel(contour, inline=True, fontsize=10)
                ax_2d.set_xlabel('Y')
                ax_2d.set_ylabel('Z')
                ax_2d.set_title('Contour Plot')
                self.status_bar.append("2D YZ Plane labeled contour plot created.")

            # Draw the 2D plot
            self.canvas_2d.draw()

        except Exception as e:
            self.status_bar.append(f"Error creating 2D plot: {e}")




    def pop_out_graph(self):
        # Create separate pop-out windows for both 3D and 2D graphs
        self.create_popout_window("3D Graph", self.plot_3d_graph)
        self.create_popout_window("2D Graph", self.update_2d_plot)

    
    
    

    def create_popout_window(self, title, plot_func):
        window = QMainWindow()
        window.setWindowTitle(f"Pop-out {title}")
        window.setGeometry(100, 100, 800, 600)

        # Create a new figure and canvas for the pop-out graph
        popout_figure = plt.figure()
        popout_canvas = FigureCanvas(popout_figure)

        # Create a toolbar for zoom, pan, and other features
        toolbar = NavigationToolbar(popout_canvas, window)

        # Layout for the pop-out window
        layout = QVBoxLayout()

        # Create axis range controls (scroll bars)
        axis_control_layout = QHBoxLayout()

        x_min_label = QLabel('X min:')
        x_min_slider = QSlider(Qt.Horizontal)
        x_min_slider.setRange(-10, 10)
        x_max_label = QLabel('X max:')
        x_max_slider = QSlider(Qt.Horizontal)
        x_max_slider.setRange(-10, 10)

        y_min_label = QLabel('Y min:')
        y_min_slider = QSlider(Qt.Horizontal)
        y_min_slider.setRange(-10, 10)
        y_max_label = QLabel('Y max:')
        y_max_slider = QSlider(Qt.Horizontal)
        y_max_slider.setRange(-10, 10)

        if "3D" in title:
            z_min_label = QLabel('Z min:')
            z_min_slider = QSlider(Qt.Horizontal)
            z_min_slider.setRange(-100, 100)
            z_max_label = QLabel('Z max:')
            z_max_slider = QSlider(Qt.Horizontal)
            z_max_slider.setRange(-100, 100)
            axis_control_layout.addWidget(z_min_label)
            axis_control_layout.addWidget(z_min_slider)
            axis_control_layout.addWidget(z_max_label)
            axis_control_layout.addWidget(z_max_slider)

        axis_control_layout.addWidget(x_min_label)
        axis_control_layout.addWidget(x_min_slider)
        axis_control_layout.addWidget(x_max_label)
        axis_control_layout.addWidget(x_max_slider)
        axis_control_layout.addWidget(y_min_label)
        axis_control_layout.addWidget(y_min_slider)
        axis_control_layout.addWidget(y_max_label)
        axis_control_layout.addWidget(y_max_slider)

        layout.addLayout(axis_control_layout)

        # Add the toolbar for zoom, pan, etc.
        layout.addWidget(toolbar)

        # Create the central widget with the pop-out graph
        layout.addWidget(popout_canvas)
        widget = QWidget()
        widget.setLayout(layout)
        window.setCentralWidget(widget)

        def plot_on_popout():
            popout_figure.clear()  # Clear any existing plot
            if title == "3D Graph":
                self.plot_3d_graph(popout_figure)
            else:
                self.update_2d_plot(popout_figure)
            popout_canvas.draw()

        plot_on_popout()

        # Function to update the axes based on slider input
        def update_axes():
            try:
                ax = popout_figure.gca()  # Get current axes
                ax.set_xlim(x_min_slider.value(), x_max_slider.value())
                ax.set_ylim(y_min_slider.value(), y_max_slider.value())
                if "3D" in title:
                    ax.set_zlim(z_min_slider.value(), z_max_slider.value())
                popout_canvas.draw()
            except ValueError:
                pass  # Ignore invalid input

        # Connect sliders to the axis adjustment function
        x_min_slider.valueChanged.connect(update_axes)
        x_max_slider.valueChanged.connect(update_axes)
        y_min_slider.valueChanged.connect(update_axes)
        y_max_slider.valueChanged.connect(update_axes)
        if "3D" in title:
            z_min_slider.valueChanged.connect(update_axes)
            z_max_slider.valueChanged.connect(update_axes)

        window.show()

        # Store the window reference to avoid garbage collection
        if title == "3D Graph":
            self.popout_window = window
        else:
            self.popout_2d_window = window






# Main program execution
def main():
    app = QApplication(sys.argv)
    window = MatLayoutPlanApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
