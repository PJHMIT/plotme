import sys
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QFileDialog, QSpinBox, QLabel, QComboBox, QFrame, QTextEdit, QRadioButton, QCheckBox
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors
sys.path.append('C:\Pythoncode\measureme\sweep')  # Replace with the actual directory path
import sweep_load as sl
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

# To do:
# 1. plot multiple data sets as multiple lines
# 2. if the div channel isn't set to 1, add it to the title

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
        
        # add a figure and canvas to the figure window
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Create a container widget for the toolbar and canvas
        toolbar_canvas_widget = QtWidgets.QWidget()
        toolbar_canvas_layout = QtWidgets.QVBoxLayout(toolbar_canvas_widget)
        toolbar_canvas_layout.addWidget(self.toolbar)
        toolbar_canvas_layout.addWidget(self.canvas)

        # Add the container widget to the layout of the figure window
        self.figure_window.layout().addWidget(toolbar_canvas_widget)

        ## populate column 1 layout
        # create a vertical box for the directory button and label
        self.directory_layout = QVBoxLayout()
        self.col1_layout.addLayout(self.directory_layout)
        
        # Create a button for choosing the directory
        self.directory_button = QPushButton('Choose parent directory')
        self.directory_button.clicked.connect(self.directory_button_clicked)  # Connect the button click event to the function
        self.directory_layout.addWidget(self.directory_button)

        # create a box to display the directory
        self.dir_label = QLabel('Directory:')
        self.directory_layout.addWidget(self.dir_label)
        # wrap the text in the dir_label
        self.dir_label.setWordWrap(True)
        
        # create a box to host the sub dir label and spin box
        self.sub_dir_layout = QHBoxLayout()
        self.directory_layout.addLayout(self.sub_dir_layout)

        # Create a label and a spin box for the directory number
        self.sub_dir_label = QLabel('Sub Dir. Number:')
        self.sub_dir_spinbox = QSpinBox()
        self.sub_dir_spinbox.setRange(1, 10000)  # Set the range of the spin box
        self.sub_dir_layout.addWidget(self.sub_dir_label)
        self.sub_dir_layout.addWidget(self.sub_dir_spinbox)

        # connect the spin box to the load_meta function
        self.sub_dir_spinbox.valueChanged.connect(self.load_meta)

        # crate a box to host the x axis, y axis, z axis, and div channel combo boxes
        self.axis_layout = QVBoxLayout()
        self.col1_layout.addLayout(self.axis_layout)

        # create a horizontal layout for the x axis combo box
        self.x_axis_layout = QHBoxLayout()
        self.axis_layout.addLayout(self.x_axis_layout)
        # create a horizontal layout for the y axis combo box
        self.y_axis_layout = QHBoxLayout()
        self.axis_layout.addLayout(self.y_axis_layout)
        # create a horizontal layout for the z axis combo box
        self.z_axis_layout = QHBoxLayout()
        self.axis_layout.addLayout(self.z_axis_layout)
        # create a horizontal layout for the div channel combo box
        self.div_channel_layout = QHBoxLayout()
        self.axis_layout.addLayout(self.div_channel_layout)
        
        # create a box to choose the x axis column from a list
        self.x_axis_label = QLabel('X Axis:')
        self.x_axis_combo = QComboBox()
        self.x_axis_layout.addWidget(self.x_axis_label)
        self.x_axis_layout.addWidget(self.x_axis_combo)
        
        # create a box to choose the y axis column 
        self.y_axis_label = QLabel('Y Axis:')
        self.y_axis_combo = QComboBox()
        self.y_axis_layout.addWidget(self.y_axis_label)
        self.y_axis_layout.addWidget(self.y_axis_combo)

        # create a box to choose the z axis column
        self.z_axis_label = QLabel('Z Axis (2D data only):')
        self.z_axis_combo = QComboBox()
        self.z_axis_layout.addWidget(self.z_axis_label)
        self.z_axis_layout.addWidget(self.z_axis_combo)
        
        # create a box to choose the div channel
        self.div_channel_label = QLabel('Div Channel:')
        self.div_channel_combo = QComboBox()
        self.div_channel_layout.addWidget(self.div_channel_label)
        self.div_channel_layout.addWidget(self.div_channel_combo)

        # add a plot button
        self.plot_button = QPushButton('Plot')
        self.plot_button.clicked.connect(self.plot_button_clicked)  # Connect the button click event to the function
        self.col1_layout.addWidget(self.plot_button)
        # set minimum height of the plot button
        self.plot_button.setFixedHeight(100)
        # make the plot botton bold font and 2 point outline, white background, font 18
        self.plot_button.setStyleSheet("font: bold 18px; color: black; background-color: white; border: 2px solid black;")
        ### end of populate the column 1 layout ###


        ### populate column 2 layout ###
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

        # Create a checkbox for auto clim
        self.auto_clim_checkbox = QCheckBox("Auto clim")
        self.col2_layout.addWidget(self.auto_clim_checkbox)
        # check auto clim by default
        self.auto_clim_checkbox.setChecked(True)

        # create a vertical layout for clim min and clim max
        self.clim_min_max_layout = QVBoxLayout()
        self.col2_layout.addLayout(self.clim_min_max_layout)

        self.clim_min_label = QLabel("clim min")
        self.clim_min_text = QTextEdit()
        self.clim_min_text.setFixedHeight(35)
        self.clim_min_text.setFixedWidth(200)
        self.col2_layout.addWidget(self.clim_min_label)
        self.col2_layout.addWidget(self.clim_min_text) ## BRING THIS LINE BACK

        self.clim_max_label = QLabel("clim max")
        self.clim_max_text = QTextEdit()
        self.clim_max_text.setFixedHeight(35)
        self.clim_max_text.setFixedWidth(200)
        self.col2_layout.addWidget(self.clim_max_label)
        self.col2_layout.addWidget(self.clim_max_text)

        # create a button for multiple lines on off
        self.waterfall_checkbox = QCheckBox("Waterfall")
        self.col2_layout.addWidget(self.waterfall_checkbox)

        # create a button for grid on off
        self.grid_checkbox = QCheckBox("Grid")
        self.col2_layout.addWidget(self.grid_checkbox)

        # create a colormap horizontal layout
        self.colormap_layout = QHBoxLayout()
        self.col2_layout.addLayout(self.colormap_layout)

        # create a list of colormaps
        self.colormap_label = QLabel('Colormap:')
        self.colormap_combo = QComboBox()
        self.colormap_combo.addItems(['viridis', 'seismic', 'inferno', 'plasma', 'magma', 'cividis', 'Spectral', 'Spectral_r', 'seismic_r'])
        self.colormap_layout.addWidget(self.colormap_label)
        self.colormap_layout.addWidget(self.colormap_combo)

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
        self.filename_text.setFixedWidth(250)
        self.col2_layout.addWidget(self.filename_text)
        
        # create an export filetype horizontal layout
        self.export_filetype_layout = QHBoxLayout()
        self.col2_layout.addLayout(self.export_filetype_layout)

        # add an export filetype combo box
        self.export_filetype_label = QLabel('Export filetype:')
        self.export_filetype_combo = QComboBox()
        self.export_filetype_combo.addItems(['jpg', 'png', 'pdf', 'svg'])
        # set the default export filetype to jpg
        self.export_filetype_combo.setCurrentText('jpg')
        # add the export filetype label and combo box to the layout       
        self.export_filetype_layout.addWidget(self.export_filetype_label)
        self.export_filetype_layout.addWidget(self.export_filetype_combo)
        
        # add a save button
        self.export_fig_button = QPushButton('Export figure')
        self.export_fig_button.clicked.connect(self.export_fig_button_clicked)
        self.col2_layout.addWidget(self.export_fig_button)
        ### end of populate column 2 layout ###


        ### populate column 3 layout ###
        # create a frame for the time
        self.time_frame = QFrame()
        self.time_text = QTextEdit(self.time_frame)
        self.col3_layout.addWidget(self.time_frame)
        # set the height of the time frame
        self.time_frame.setFixedHeight(50)
        
        # Create a frame for the metadata
        self.metadata_frame = QFrame()
        self.metadata_text = QTextEdit(self.metadata_frame)
        self.col3_layout.addWidget(self.metadata_frame)

        # create a frame for the measurement config
        self.measurement_config_frame = QFrame()
        self.measurement_config_text = QTextEdit(self.measurement_config_frame)
        self.col3_layout.addWidget(self.measurement_config_frame)
        
        # add a slow param label
        self.slow_param_label = QLabel('')
        self.col3_layout.addWidget(self.slow_param_label)
        # set height of the slow_param label
        self.slow_param_label.setFixedHeight(35)

        # create a frame for the slow_setpoints
        self.slow_setpoints_frame = QFrame()
        self.slow_setpoints_text = QTextEdit(self.slow_setpoints_frame)
        self.col3_layout.addWidget(self.slow_setpoints_frame)
        # set the height of the fast_setpoints frame
        self.slow_setpoints_frame.setFixedHeight(100)
        ### end of populate column 3 layout ###

        # add a fast param label
        self.fast_param_label = QLabel('')
        self.col3_layout.addWidget(self.fast_param_label)
        # set height of the fast_param label
        self.fast_param_label.setFixedHeight(35)

        # create a frame for the fast_setpoints
        self.fast_setpoints_frame = QFrame()
        self.fast_setpoints_text = QTextEdit(self.fast_setpoints_frame)
        self.col3_layout.addWidget(self.fast_setpoints_frame)
        # set the height of the slow_setpoints frame
        self.fast_setpoints_frame.setFixedHeight(100)

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
        # set font to black
        self.save_dir_label.setStyleSheet("color: black")

    # save the figure as a pdf
    def export_fig_button_clicked(self):
        if not hasattr(self, 'savedir'):
            # display message to choose directory
            self.save_dir_label.setText('Please choose save directory')
            # set font to red
            self.save_dir_label.setStyleSheet("color: red")
            return
        if self.filename_text.toPlainText() == '':
            str1 = str(self.sub_dir_spinbox.value())
            if self.data_type == '1D':
                str2 = self.y_axis_combo.currentText()
            else:
                str2 = self.z_axis_combo.currentText()
            
            # set the file extension according to the export filetype combo box
            ftype = self.export_filetype_combo.currentText()
            string = str1 + '_' + str2 + '.' + ftype
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

        # display the metadata on the gui, separated by newlines
        self.metadata_text.setText('\n'.join([f'{k}: {v}' for k, v in data.items() if k in ['comments', 'type', 'function', 'slow_delay', 'fast_delay']]))
        # set data_type to 1D or 2D according to the metadata type field
        self.data_type = data['type']

        # parse the measurement_config field of the metadata
        if 'measurement_config' in data:
            self.measurement_config = data['measurement_config']
            self.measurement_config_text.setText('\n'.join([f'{k}: {v}' for k, v in self.measurement_config.items()]))
            # print(self.measurement_config)
            # value = self.measurement_config['SR860_A']
            # print(value)  # Outputs: '6-20'
        
        # add text slow_param label
        if 'slow_param' in data:
            self.slow_param_label.setText(f'slow_param: {data["slow_param"]}')
        elif 'param' in data:
            self.slow_param_label.setText(f'param: {data["param"]}')
            self.fast_param_label.setText(f'')

        # add the fast_param label
        if 'fast_param' in data:
            self.fast_param_label.setText(f'fast_param: {data["fast_param"]}')

        # parse the slow_setpoints field of the metadata
        if 'slow_setpoints' in data:
            self.slow_setpoints = data['slow_setpoints']
            self.slow_setpoints_text.setText('\n'.join(map(str, self.slow_setpoints)))
        elif 'setpoints' in data:
            self.setpoints = data['setpoints']
            self.slow_setpoints_text.setText('\n'.join(map(str, self.setpoints)))
            self.fast_setpoints_text.setText('')                


        # parse the fast_setpoints field of the metadata
        if 'fast_setpoints' in data:
            self.fast_setpoints = data['fast_setpoints']
            self.fast_setpoints_text.setText('\n'.join(map(str, self.fast_setpoints)))                
        
        # set the columns to the columns field of the metadata
        self.columns = data['columns']

        # put columns in the combo boxes, replacing the current items
        self.x_axis_combo.clear()        
        self.x_axis_combo.addItems(self.columns)
        self.y_axis_combo.clear()
        self.y_axis_combo.addItems(self.columns)
        meta_text = self.metadata_text.toPlainText()
        if self.data_type == '2D':
            self.z_axis_combo.clear()
            self.z_axis_combo.addItems(self.columns)
            # set the x axis to be the slow axis from the metadata
            # find the string 'slow_param' in the meta_text and set the x axis to be the following string
            if 'slow_param' in data:
                # fine the corresponding dict value
                slow_param = data['slow_param']
                # if slow_param is a list, set the x axis to be the first element of the list
                if isinstance(slow_param, list):
                    slow_param = slow_param[0]
                # set the x axis to be the slow axis from the metadata
                self.x_axis_combo.setCurrentText(slow_param)
            if 'fast_param' in data:
                # fine the corresponding dict value
                fast_param = data['fast_param']
                # if fast_param is a list, set the y axis to be the first element of the list
                if isinstance(fast_param, list):
                    fast_param = fast_param[0]
                # set the y axis to be the fast axis from the metadata
                self.y_axis_combo.setCurrentText(fast_param)
        else:
            self.z_axis_combo.clear()
            # set the x axis to be the slow axis from the metadata
            # find the string 'param' in the columns and set the x axis to be the following string
            if 'param' in data:
                # fine the corresponding dict value
                param = data['param']
                # set the x axis to be the param from the metadata
                self.x_axis_combo.setCurrentText(param)
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
        data = sl.pload(datadir, sub_dir)

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
                    norm = matplotlib.colors.SymLogNorm(vmin=clim_min, vmax=clim_max)    
                else:
                    norm = matplotlib.colors.SymLogNorm()
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
            self.ax.set_title(f'{datadir}/{sub_dir}\n{y_axis}')
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


