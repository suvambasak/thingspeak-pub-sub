from tkinter import *
from tkinter import ttk
from matplotlib import pyplot as plt
import pymysql
import threading
import time
import Adafruit_DHT

# Test
# import random


class Database:
    '''
    MySQL Database
    '''

    def __init__(self):
        # Total entry count.
        self.entry_count = 0

        # Credentials
        self.host = 'localhost'
        # self.user = 'admin'
        # self.password = 'admin'
        # self.dbname = '20mcmb08'

        self.user = 'phpmyadmin'
        self.password = 'scisnks99'
        self.dbname = 'phpmyadmin'

        # Connect
        try:
            self.db = pymysql.connect(
                self.host, self.user, self.password, self.dbname)
            print("[*] Database Connected.")
        except Exception as e:
            print("\n\n[**] Exception :: __init__ :: " + str(e))
            print('\n\n')

        # Auto commit and cursor.
        self.db.autocommit(True)
        self.cursor = self.db.cursor()

    def fetch_all(self):
        # Function to fetch all data from the table dht.

        SQL = "SELECT * FROM `dht`"

        # Execute and fetch result.
        try:
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()
            # print('fetch_all: ', result)
            return result
        except Exception as e:
            print('\n[**] Database :: fetch_all :: ' + str(e))
            return None

    def add_new(self, temperature, humidity):
        # Function to insert new data.

        SQL = "INSERT INTO `dht` (`id`, `time`, `temperature`, `humidity`) VALUES (NULL, NULL, '%s', '%s')" % (
            temperature, humidity)

        # Execute
        try:
            self.cursor.execute(SQL)
            self.entry_count += 1
            print('add_new:', temperature, humidity)
        except Exception as e:
            print('\n[**] Exception :: add_new :: ' + str(e))

    def get_entry_count(self):
        # Function to get total data entry.
        return self.entry_count


class Sensor:
    '''
    DHT11 Sensor
    '''

    def __init__(self):
        # Thread control
        self.control = None
        self.sensor_threat = None

        # Set sensor type : Options are DHT11,DHT22 or AM2302
        self.sensor = Adafruit_DHT.DHT11

        # Set GPIO sensor is connected to
        self.gpio = 4

        # Database object
        self.db = Database()

    def sense(self):
        # Thread to sense and store data in database.
        while self.control:
            try:
                time.sleep(3)

                # Use read_retry method. This will retry up to 15 times to
                # get a sensor reading (waiting 2 seconds between each retry).
                humidity, temperature = Adafruit_DHT.read_retry(
                    self.sensor, self.gpio)

                # TEST
                # humidity = random.randint(0, 50)
                # temperature = random.randint(0, 50)

                if humidity is not None and temperature is not None:
                    print(
                        'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

                    # Insert data
                    self.db.add_new(temperature, humidity)
                else:
                    print('Failed to get reading. Try again!')

            except Exception as e:
                print('Sense:', str(e))

    def start(self):
        # Function to start the thread
        self.control = True
        self.sensor_threat = threading.Thread(target=self.sense)
        self.sensor_threat.start()

    def stop(self):
        # Function to stop the thread
        self.control = False
        self.sensor_threat.join()

        # return total data entry
        return self.db.get_entry_count()


class GUI:
    '''
    Graphical User Interface
    '''

    def __init__(self):
        # Sensor object
        self.flag = True
        self.sensor = Sensor()

        self.root = Tk()
        self.root.title('Problem 2')

        # create frame for start publishing
        self.pub_frame = LabelFrame(
            self.root, text='MySQL DB Store', padx=50, pady=50)
        self.pub_frame.grid(row=0, column=0, padx=10, pady=10)

        # Status View
        self.status_text = StringVar()
        self.status_text.set('Current Status')
        self.status_view = Label(self.pub_frame, textvariable=self.status_text)
        self.status_view.grid(row=0, column=0)

        # Progress bar
        self.pub_prog = ttk.Progressbar(self.pub_frame, orient=HORIZONTAL,
                                        length=150, mode='indeterminate')
        self.pub_prog.grid(row=1, column=0, pady=20)

        # adding button in publishing frame.
        self.start = Button(self.pub_frame, text='Start',
                            command=self.start_pub)
        self.start.grid(row=2, column=0)

        self.stop = Button(self.pub_frame, text='Stop', command=self.stop_pub)
        self.stop.grid(row=3, column=0)

        self.plot = Button(
            self.pub_frame, text='Plot Graph', command=self.graph)
        self.plot.grid(row=4, column=0, pady=10)

        self.root.mainloop()

    def graph(self):
        # Fetch all data from database and show the graph

        result = Database().fetch_all()

        if None == result:
            print('Error: GUI graph..')
            return

        # X-axis values
        time = []
        # Y-axis values
        temperature = []
        humidity = []

        # make list of time, temperature, humidity
        for row in result:
            time.append(row[1])
            temperature.append(row[2])
            humidity.append(row[3])

        # plot
        plt.plot(time, temperature, label='Temperature Line')
        plt.plot(time, humidity, label='Humidity Line')

        plt.xlabel('Time')
        plt.ylabel('Temperature & Humidity')

        plt.title('DHT Sensor')
        plt.legend()

        # function to show the plot
        plt.show()

    def start_pub(self):
        # Start button click event handle
        # Starting the thread on click

        if self.flag:
            self.flag = False

            print('Start pub')
            self.sensor.start()

            # Start progress bar and change status view
            self.pub_prog.start(20)
            self.status_text.set('Started..')

    def stop_pub(self):
        # Stop button clickevent handle
        # Stoping the thread on click

        if not self.flag:
            self.flag = True

            print('Stop pub')
            entry = self.sensor.stop()
            self.pub_prog.stop()

            self.status_text.set('Stopped..')
            time.sleep(1.5)

            # Show total entry
            self.status_text.set('Total Entry: '+str(entry))


# Start GUI
GUI()
