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
        # set an minimum width
        self.setMinimumWidth(800)
        # name the window
        self.setWindowTitle('Plotme')

        # Create a horizontal layout for the central widget
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create a vertical layout for the directory button, combo box and spin box
        self.col1_layout = QVBoxLayout()
        self.layout.addLayout(self.col1_layout)

        # Create a vertical layout for the plot settings
        self.col2_layout = QVBoxLayout()
        self.layout.addLayout(self.col2_layout)

        # Create a vertical layout for the time and metadata
        self.col3_layout = QVBoxLayout()
        self.layout.addLayout(self.col3_layout)

        # Create a new window for the figure
        self.figure_window = QWidget()
        self.figure_window.setWindowTitle('Figure Window')
        # set the minimum width and height of the figure window
        self.figure_window.setMinimumWidth(800)
        self.figure_window.setMinimumHeight(600)
        
        # Create a layout for the new window
        self.figure_window_layout = QVBoxLayout()
        self.figure_window.setLayout(self.figure_window_layout)

        # Show the new window
        self.figure_window.show()

        # add a canvas and figure to the figure window
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.figure_window_layout.addWidget(self.canvas)
        

        
        ## populate the col1_layout
        # Create a button for choosing the directory
        self.directory_button = QPushButton('Choose parent directory')
        self.directory_button.clicked.connect(self.directory_button_clicked)  # Connect the button click event to the function
        self.col1_layout.addWidget(self.directory_button)

        # create a box to display the directory
        self.dir_label = QLabel('Directory:')
        self.col1_layout.addWidget(self.dir_label)
        
        # Create a label and a spin box for the directory number
        self.sub_dir_label = QLabel('Sub Dir. Number:')
        self.sub_dir_spinbox = QSpinBox()
        self.sub_dir_spinbox.setRange(1, 10000)  # Set the range of the spin box
        self.col1_layout.addWidget(self.sub_dir_label)
        self.col1_layout.addWidget(self.sub_dir_spinbox)

        # connect the spin box to the load_meta function
        self.sub_dir_spinbox.valueChanged.connect(self.load_meta)

        # create a box to choose the x axis column from a list
        self.x_axis_label = QLabel('X Axis:')
        self.x_axis_combo = QComboBox()
        self.col1_layout.addWidget(self.x_axis_label)
        self.col1_layout.addWidget(self.x_axis_combo)
        
        # create a box to choose the y axis column 
        self.y_axis_label = QLabel('Y Axis:')
        self.y_axis_combo = QComboBox()
        self.col1_layout.addWidget(self.y_axis_label)
        self.col1_layout.addWidget(self.y_axis_combo)

        # create a box to choose the z axis column
        self.z_axis_label = QLabel('Z Axis (only for 2D data):')
        self.z_axis_combo = QComboBox()
        self.col1_layout.addWidget(self.z_axis_label)
        self.col1_layout.addWidget(self.z_axis_combo)
        
        # create a box to choose the div channel
        self.div_channel_label = QLabel('Div Channel:')
        self.div_channel_combo = QComboBox()
        self.col1_layout.addWidget(self.div_channel_label)
        self.col1_layout.addWidget(self.div_channel_combo)

        # add a plot button
        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot_button_clicked)  # Connect the button click event to the function
        self.col1_layout.addWidget(self.plot_button)
        # set minimum height of the plot button
        self.plot_button.setFixedHeight(100)
        # make the plot botton bold font and 2 point outline, white background
        self.plot_button.setStyleSheet("font: bold; border: 2px solid black; background-color: white;")
        ### end of populate the col1_layout ###


        ### populate the central column layout ###
        # create a frame for the time
        self.time_frame = QFrame()
        self.time_text = QTextEdit(self.time_frame)
        self.col3_layout.addWidget(self.time_frame)
        
        # Create a frame for the metadata
        self.metadata_frame = QFrame()
        self.metadata_text = QTextEdit(self.metadata_frame)
        self.col3_layout.addWidget(self.metadata_frame)
        ### end of populate the central column layout ###

        ### populate the right column layout ###
        # Create a vertical layout
        log_layout = QVBoxLayout()

        # Create checkboxes for logx, logy, and logz
        self.logx_checkbox = QCheckBox("logx")
        self.logy_checkbox = QCheckBox("logy")
        self.logz_checkbox = QCheckBox("logz")

        # Add checkboxes to the layout
        log_layout.addWidget(self.logx_checkbox)
        log_layout.addWidget(self.logy_checkbox)
        log_layout.addWidget(self.logz_checkbox)

        # Add the log layout to the right column layout
        self.col2_layout.addLayout(log_layout)

        # Create a horizontal layout for clim
        # self.clim_layout = QHBoxLayout()
        # self.col2_layout.addLayout(self.clim_layout)

        # Create a checkbox for auto clim
        self.auto_clim_checkbox = QCheckBox("Auto clim")
        self.col2_layout.addWidget(self.auto_clim_checkbox)
        # check auto clim by default
        self.auto_clim_checkbox.setChecked(True)

        # create a vertical layout for clim min and clim max
        self.clim_min_max_layout = QVBoxLayout()
        self.col2_layout.addLayout(self.clim_min_max_layout)

        # Create a horizontal layout for clim min
        # self.clim_min_layout = QHBoxLayout()
        self.clim_min_label = QLabel("clim min")
        self.clim_min_text = QTextEdit()
        self.clim_min_text.setFixedHeight(35)
        self.clim_min_text.setFixedWidth(200)
        self.col2_layout.addWidget(self.clim_min_label)
        self.col2_layout.addWidget(self.clim_min_text) ## BRING THIS LINE BACK
        # self.clim_min_max_layout.addLayout(self.clim_min_layout)

        # Create a horizontal layout for clim max
        # self.clim_max_layout = QHBoxLayout()
        self.clim_max_label = QLabel("clim max")
        self.clim_max_text = QTextEdit()
        self.clim_max_text.setFixedHeight(35)
        self.clim_max_text.setFixedWidth(200)
        self.col2_layout.addWidget(self.clim_max_label)
        self.col2_layout.addWidget(self.clim_max_text)
        # self.clim_min_max_layout.addLayout(self.clim_max_layout)

        # create a button for multiple lines on off
        self.waterfall_checkbox = QCheckBox("Waterfall")
        self.col2_layout.addWidget(self.waterfall_checkbox)

        # create a button for grid on off
        self.grid_checkbox = QCheckBox("Grid")
        self.col2_layout.addWidget(self.grid_checkbox)

        # create a list of colormaps
        self.colormap_label = QLabel('Colormap:')
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(['viridis', 'seismic', 'inferno', 'plasma', 'magma', 'cividis', 'Spectral', 'Spectral_r', 'seismic_r'])
        self.col2_layout.addWidget(self.colormap_label)
        self.col2_layout.addWidget(self.colormap_combo)

        ### end of populate the plot settings layout ###

        # add a button to choose a save directory
        self.save_dir_button = QPushButton('Choose save directory')
        self.save_dir_button.clicked.connect(self.save_directory_button_clicked)
        self.col2_layout.addWidget(self.save_dir_button)

        # add a save directory label
        self.save_dir_label = QLabel('Save Directory:')
        self.col2_layout.addWidget(self.save_dir_label)

        # add a filename label
        self.filename_label = QLabel('Export filename:')
        self.col2_layout.addWidget(self.filename_label)
        
        # add a filename text box
        self.filename_text = QTextEdit()
        self.filename_text.setFixedHeight(35)
        self.filename_text.setFixedWidth(200)
        self.col2_layout.addWidget(self.filename_text)
        
        # add a save button
        self.export_fig_button = QPushButton('Export figure as pdf')
        self.export_fig_button.clicked.connect(self.export_fig_button_clicked)
        self.col2_layout.addWidget(self.export_fig_button)
        
        # Set the layout of the central widget
        self.central_widget.setLayout(self.layout)

              


    # if colormap_combo is clicked, set the colormap
    def colormap_combo_clicked(self):
        self.colormap = self.colormap_combo.currentText()


    def directory_button_clicked(self):
        selected_dir = QFileDialog.getExistingDirectory(self, 'Select Directory')  # Open a dialog to choose the directory
        # if no directory was seleced, return
        if selected_dir == '':
            return
        self.datadir = selected_dir  # Set the datadir to the selected directory
        # display the directory on the gui
        self.dir_label.setText(f'Directory: {self.datadir}')
        # set font to black
        self.dir_label.setStyleSheet("color: black")
        # when the choose dir button is clicked, load the metadata
        self.load_meta()

    def save_directory_button_clicked(self):
        selected_dir = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if selected_dir == '':
            return
        self.savedir = selected_dir
        # display the save directory on the gui
        self.save_dir_label.setText(f'Save Directory: {self.savedir}')

    # save the figure as a pdf
    def export_fig_button_clicked(self):
        if not hasattr(self, 'savedir'):
            # display message to choose directory
            self.save_dir_label.setText('Please choose save directory')
            return
        if self.filename_text.toPlainText() == '':
            print('im here')
            str1 = str(self.sub_dir_spinbox.value())
            if self.data_type == '1D':
                str2 = self.y_axis_combo.currentText()
            else:
                str2 = self.z_axis_combo.currentText()
            string = str1 + '_' + str2 + '.pdf'
            self.filename_text.setText(string)
        # set ofn to be the save_dir_label + filename
        print(self.filename_text.toPlainText())
        ofn = self.savedir + '/' + self.filename_text.toPlainText()
        savedict = dict(dpi=300)
        self.fig.savefig(ofn, **savedict)
        print('saved figure --> {}'.format(ofn))
       
    # load the metadata
    def load_meta(self):
        # if the directory is not set, return
        if not hasattr(self, 'datadir'):
            # display message to choose directory
            self.dir_label.setText('Please choose parent directory')
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
        self.div_channel_combo.clear()
        self.div_channel_combo.addItems(['1'])
        self.div_channel_combo.addItems(self.columns)

    # if plot_button is clicked, plot the data
    def plot_button_clicked(self):
        # if the directory is not set, return
        if not hasattr(self, 'datadir'):
            # display message to choose directory
            self.dir_label.setText('Please choose parent directory')
            # set font to red
            self.dir_label.setStyleSheet("color: red")
            return
        self.sub_dir = self.sub_dir_spinbox.value()
        self.plot_data(self.datadir, self.sub_dir)
        # try to bring the figure window to the front. This depends on the OS
        self.figure_window.raise_()
        self.figure_window.activateWindow()

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
        clim_max = self.clim_max_text.toPlainText()
        # convert the clim min and max to floats
        try:
            clim_min = float(clim_min)
            clim_max = float(clim_max)
        except:
            pass
        colormap = self.colormap_combo.currentText()
        
        # Redraw the plots
        x_axis = self.x_axis_combo.currentText()
        y_axis = self.y_axis_combo.currentText()
        div_channel = self.div_channel_combo.currentText()

        if self.data_type == '2D':
            z_axis = self.z_axis_combo.currentText()
            # verify compliance with pcolormesh - equi length
            if not (len(data[x_axis]) == len(data[z_axis]) and len(data[y_axis]) == len(data[z_axis])):
                return
            # verify compliance with pcolormesh - no non-fininte values
            if not (all([all([np.isfinite(i) for i in j]) for j in data[z_axis]])):
                return
            
            if logz == True:
                # make sure clim_min and clim_max are floats
                if auto_clim == False and isinstance(clim_min, float) and isinstance(clim_max, float):
                    norm = matplotlib.colors.LogNorm(vmin=clim_min, vmax=clim_max)    
                else:
                    norm = matplotlib.colors.LogNorm()
                props = dict(rasterized=True, cmap=colormap, norm=norm) 
            else:
                if auto_clim == False and isinstance(clim_min, float) and isinstance(clim_max, float):
                    props = dict(rasterized=True, vmin=clim_min,vmax=clim_max, cmap=colormap) 
                else:
                    props = dict(rasterized=True, cmap=colormap) 
                    
            if div_channel == '1':
                self.ax.pcolormesh(data[x_axis], data[y_axis], data[z_axis], **props)
            else:
                self.ax.pcolormesh(data[x_axis], data[y_axis], data[z_axis]/data[div_channel], **props)
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
            if div_channel == '1':
                self.ax.plot(data[x_axis], data[y_axis], '.')
            else:
                self.ax.plot(data[x_axis], data[y_axis]/data[div_channel], '.')
            self.ax.set_xlabel(x_axis)
            self.ax.set_ylabel(y_axis)
            self.ax.set_title(y_axis)
            # if clim not set to auto, set the ylimits according to clim_min and clim_max
            if auto_clim == False:
                self.ax.set_ylim(clim_min, clim_max)
                            


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
# 2. add a save button and save directory text box