import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QFileDialog, QSpinBox, QLabel, QComboBox, QFrame, QTextEdit, QRadioButton, QCheckBox
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors
sys.path.append('C:\Pythoncode\loadme\sweep_load')  # Replace with the actual directory path
import sweep_load as sl
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable





class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Create a central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout for the whole window
        self.layout = QVBoxLayout(self.central_widget)

        # Create a horizontal layout for the top part of the window
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        # Create a vertical layout for the directory button, combo box and spin box
        self.dir_combo_spinbox_layout = QVBoxLayout()
        self.top_layout.addLayout(self.dir_combo_spinbox_layout)

        # Create a vertical layout for the time and metadata
        self.dir_combo_time_meta = QVBoxLayout()
        self.top_layout.addLayout(self.dir_combo_time_meta)

        # Create a vertical layout for the plot settings
        self.plot_settings_layout = QVBoxLayout()
        self.top_layout.addLayout(self.plot_settings_layout)

        # Create a figure and a canvas
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)


        ## populate the dir_combo_spinbox_layout
        # Create a button for choosing the directory
        self.button = QPushButton('Choose mother directory')
        self.button.clicked.connect(self.choose_dir_button)  # Connect the button click event to the function
        self.dir_combo_spinbox_layout.addWidget(self.button)

        # create a box to display the directory
        self.dir_label = QLabel('Directory:')
        self.dir_combo_spinbox_layout.addWidget(self.dir_label)
        

        # Create a label and a spin box for the directory number
        self.sub_dir_label = QLabel('Sub Dir. Number:')
        self.sub_dir_spinbox = QSpinBox()
        self.sub_dir_spinbox.setRange(1, 10000)  # Set the range of the spin box
        self.dir_combo_spinbox_layout.addWidget(self.sub_dir_label)
        self.dir_combo_spinbox_layout.addWidget(self.sub_dir_spinbox)

        # connect the spin box to the load_meta function
        self.sub_dir_spinbox.valueChanged.connect(self.load_meta)

        # create a box to choose the x axis column from a list
        self.x_axis_label = QLabel('X Axis:')
        self.x_axis_combo = QComboBox()
        self.dir_combo_spinbox_layout.addWidget(self.x_axis_label)
        self.dir_combo_spinbox_layout.addWidget(self.x_axis_combo)
        
        # create a box to choose the y axis column 
        self.y_axis_label = QLabel('Y Axis:')
        self.y_axis_combo = QComboBox()
        self.dir_combo_spinbox_layout.addWidget(self.y_axis_label)
        self.dir_combo_spinbox_layout.addWidget(self.y_axis_combo)

        # create a box to choose the z axis column
        self.z_axis_label = QLabel('Z Axis (only for 2D data):')
        self.z_axis_combo = QComboBox()
        self.dir_combo_spinbox_layout.addWidget(self.z_axis_label)
        self.dir_combo_spinbox_layout.addWidget(self.z_axis_combo)
        
        # add a plot button
        self.button2 = QPushButton('Plot')
        self.button2.clicked.connect(self.plot_button)  # Connect the button click event to the function
        self.dir_combo_spinbox_layout.addWidget(self.button2)
        ### end of populate the dir_combo_spinbox_layout ###


        ### populate the time and metadata layout ###
        # create a frame for the time
        self.time_frame = QFrame()
        self.time_text = QTextEdit(self.time_frame)
        self.dir_combo_time_meta.addWidget(self.time_frame)
        
        # Create a frame for the metadata
        self.metadata_frame = QFrame()
        self.metadata_text = QTextEdit(self.metadata_frame)
        self.dir_combo_time_meta.addWidget(self.metadata_frame)
        ### end of populate the time and metadata layout ###




        # Create a horizontal layout
        log_layout = QHBoxLayout()

        # Create checkboxes for logx, logy, and logz
        self.logx_checkbox = QCheckBox("logx")
        self.logy_checkbox = QCheckBox("logy")
        self.logz_checkbox = QCheckBox("logz")

        # Add checkboxes to the layout
        log_layout.addWidget(self.logx_checkbox)
        log_layout.addWidget(self.logy_checkbox)
        log_layout.addWidget(self.logz_checkbox)

        # Add the horizontal layout to the main layout
        self.plot_settings_layout.addLayout(log_layout)



        # Create a horizontal layout for auto clim
        self.clim_layout = QHBoxLayout()
        self.auto_clim_checkbox = QCheckBox("Auto clim")
        self.clim_layout.addWidget(self.auto_clim_checkbox)
        self.plot_settings_layout.addLayout(self.clim_layout)
        # check auto clim by default
        self.auto_clim_checkbox.setChecked(True)

        # create a vertical layout for clim min and clim max
        self.clim_min_max_layout = QVBoxLayout()
        self.clim_layout.addLayout(self.clim_min_max_layout)

        # Create a horizontal layout for clim min
        self.clim_min_layout = QHBoxLayout()
        clim_min_label = QLabel("clim min")
        self.clim_min_text = QTextEdit()
        self.clim_min_text.setFixedHeight(35)
        self.clim_min_layout.addWidget(clim_min_label)
        self.clim_min_layout.addWidget(self.clim_min_text)
        self.clim_min_max_layout.addLayout(self.clim_min_layout)

        # Create a horizontal layout for clim max
        clim_max_layout = QHBoxLayout()
        clim_max_label = QLabel("clim max")
        self.clim_max_text = QTextEdit()
        self.clim_max_text.setFixedHeight(35)
        clim_max_layout.addWidget(clim_max_label)
        clim_max_layout.addWidget(self.clim_max_text)
        self.clim_min_max_layout.addLayout(clim_max_layout)




        # # create a button for manual clim on off
        # self.auto_clim_checkbox = QCheckBox("Auto Clim")
        # self.plot_settings_layout.addWidget(self.auto_clim_checkbox)

        # # Create a horizontal layout
        # clim_min_layout = QHBoxLayout()

        # # Create a label
        # clim_min_label = QLabel("clim min")
        # clim_min_layout.addWidget(clim_min_label)

        # # Create a text edit for the clim min value
        # self.clim_min_text = QTextEdit()
        # self.clim_min_text.setFixedHeight(35) 
        # clim_min_layout.addWidget(self.clim_min_text)

        # # Add the horizontal layout to the main layout
        # self.plot_settings_layout.addLayout(clim_min_layout)

        # # Create a horizontal layout
        # clim_max_layout = QHBoxLayout()

        # # Create a label
        # clim_max_label = QLabel("clim max")
        # clim_max_layout.addWidget(clim_max_label)

        # # Create a text edit for the clim max value
        # self.clim_max_text = QTextEdit()
        # self.clim_max_text.setFixedHeight(35) 
        # clim_max_layout.addWidget(self.clim_max_text)

        # # Add the horizontal layout to the main layout
        # self.plot_settings_layout.addLayout(clim_max_layout)










        # create a button for multiple lines on off
        self.waterfall_checkbox = QCheckBox("Waterfall")
        self.plot_settings_layout.addWidget(self.waterfall_checkbox)        

        # create a button for grid on off
        self.grid_checkbox = QCheckBox("Grid")
        self.plot_settings_layout.addWidget(self.grid_checkbox)

        # create a list of colormaps
        self.colormap_label = QLabel('Colormap:')
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(['viridis', 'seismic', 'inferno', 'plasma', 'magma', 'cividis', 'Spectral', 'Spectral_r', 'seismic_r'])
        self.plot_settings_layout.addWidget(self.colormap_label)
        self.plot_settings_layout.addWidget(self.colormap_combo)

        ### end of populate the plot settings layout ###

        # add a save button
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_button)  # Connect the button click event to the function
        self.layout.addWidget(self.save_button)

        # add a save directory text box
        self.save_dir_text = QTextEdit()
        self.save_dir_text.setFixedHeight(35)
        self.layout.addWidget(self.save_dir_text)
        
        # Set the layout of the central widget
        self.central_widget.setLayout(self.layout)


    # if colormap_combo is clicked, set the colormap
    def colormap_combo_clicked(self):
        self.colormap = self.colormap_combo.currentText()
            

    def choose_dir_button(self):
        self.datadir = QFileDialog.getExistingDirectory(self, 'Select Directory')  # Open a dialog to choose the directory
        self.sub_dir = self.sub_dir_spinbox.value()  # Get the value of the spin box
        # display the directory on the gui
        self.dir_label.setText(f'Directory: {self.datadir}')
        # when the choose dir button is clicked, load the metadata
        self.load_meta()

       
    # load the metadata
    def load_meta(self):
        # if the directory is not set, return
        if not hasattr(self, 'datadir'):
            # display message to choose directory
            self.dir_label.setText('Please choose mother directory')
            return
                
        self.sub_dir = self.sub_dir_spinbox.value()  # Get the value of the spin box
        data = sl.load_meta(self.datadir, self.sub_dir)
        
        # get the start time
        if 'start_time' in data:
            start_time = data['start_time']
        else:
            start_time = 0
        if 'end_time' in data:
            end_time = data['end_time']
        else:
            end_time = 0
        start_time = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        
        # add to the metadata text the start time and end time in the format year-month-day hour:minute:second
        self.time_text.setText(f'start_time: {start_time}')
        self.time_text.append(f'end_time: {end_time}')

        # display the metadata on the gui, separated by newlines. don't display the setpoints, columns, start_time, or end_time
        self.metadata_text.setText('\n'.join([f'{k}: {v}' for k, v in data.items() if k not in ['setpoints', 'columns', 'start_time', 'end_time']]))

        # set data_type to 1D or 2D according to the metadata type field
        self.data_type = data['type']

        # set the columns to the columns field of the metadata
        self.columns = data['columns']

        # put columns in the combo boxes, replacing the current items
        self.x_axis_combo.clear()        
        self.x_axis_combo.addItems(self.columns)
        self.y_axis_combo.clear()
        self.y_axis_combo.addItems(self.columns)
        if self.data_type == '2D':
            self.z_axis_combo.clear()
            self.z_axis_combo.addItems(self.columns)
        else:
            self.z_axis_combo.clear()
    
    # if plot_button is clicked, plot the data
    def plot_button(self):
        self.sub_dir = self.sub_dir_spinbox.value()
        self.plot_data(self.datadir, self.sub_dir)

    # plot the data
    def plot_data(self, datadir, sub_dir):
        if self.data_type == '1D':
            data = sl.pload1d(datadir, sub_dir)
        else:
            data = sl.pload2d(datadir, sub_dir)

        # Clear the axes
        self.ax.clear()
        
        # Get the state of the logx checkbox
        logx = self.logx_checkbox.isChecked()
        logy = self.logy_checkbox.isChecked()
        logz = self.logz_checkbox.isChecked()
        grid = self.grid_checkbox.isChecked()
        auto_clim = self.auto_clim_checkbox.isChecked()
        waterfall = self.waterfall_checkbox.isChecked()

        # get the plot settings from the buttons
        clim_min = self.clim_min_text.toPlainText()
        print('clim_min: ', clim_min)
        clim_max = self.clim_max_text.toPlainText()
        print('clim_max: ', clim_max)
        colormap = self.colormap_combo.currentText()
        
        # Redraw the plots
        x_axis = self.x_axis_combo.currentText()
        y_axis = self.y_axis_combo.currentText()
        if self.data_type == '2D':
            z_axis = self.z_axis_combo.currentText()
            # verify compliance with pcolormesh - equi length
            if not (len(data[x_axis]) == len(data[z_axis]) and len(data[y_axis]) == len(data[z_axis])):
                return
            # verify compliance with pcolormesh - no non-fininte values
            if not (all([all([np.isfinite(i) for i in j]) for j in data[z_axis]])):
                return
            
            if logz == True:
                # make sure clim_min and clim_max are numbers
                if auto_clim == False and not (clim_min.replace('.', '', 1).isdigit() and clim_max.replace('.', '', 1).isdigit()):
                    norm = matplotlib.colors.LogNorm(vmin=clim_min, vmax=clim_max)    
                else:
                    norm = matplotlib.colors.LogNorm()
                props = dict(rasterized=True, cmap=colormap, norm=norm) 
            else:
                if auto_clim == False and not (clim_min.replace('.', '', 1).isdigit() and clim_max.replace('.', '', 1).isdigit()):
                    props = dict(rasterized=True, vmin=clim_min,vmax=clim_max, cmap=colormap) 
                else:
                    props = dict(rasterized=True, cmap=colormap) 
                    
            
            self.ax.pcolormesh(data[x_axis], data[y_axis], data[z_axis], **props)
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            # define the title of the plot to be the the directory\sub dir, new line, z axis
            self.ax.set_title(f'{datadir}/{sub_dir}\n{z_axis}')

            # set grid
            if grid == True:
                self.ax.grid()
            else:
                self.ax.grid(False)

            # remove existing colorbar
            if hasattr(self, 'cax'):
                self.cax.remove()
                
            # add colorbar
            divider = make_axes_locatable(self.ax) # make room for the colorbar
            self.cax = divider.append_axes("right", size="5%", pad=0.05)
            plt.colorbar(self.ax.collections[0], cax=self.cax)

        else:
            self.ax.plot(data[x_axis], data[y_axis], '.')
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            self.ax.set_title(y_axis)

        # set the logx, logy, logz settings
        if logx == True:
            self.ax.set_xscale('log')
        else:
            self.ax.set_xscale('linear')

        if logy == True:
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')

        # Redraw the canvas
        self.canvas.draw()

# Create the application
app = QApplication(sys.argv)
# Create the main window
main = MainWindow()
main.show()
# Start the application
sys.exit(app.exec_())



# Additions
# 1. plot multiple data sets as multiple lines
