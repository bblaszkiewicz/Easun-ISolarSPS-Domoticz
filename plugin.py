"""
<plugin key="easun_inverter" name="Easun Inverter Plugin" version="0.1" author="BBlaszkiewicz">
  <description>
    Plugin do odczytywania danych z inwertera Easun poprzez port RS232/RS485.
  </description>
  
  <!-- Parametry konfiguracyjne -->
  <params>
   <param field="Mode1" label="Serial Port" width="200px" required="true" default="/dev/ttySC1"/>
   <param field="Mode2" label="Baudrate" width="100px" required="true">
     <options>
       <option label="2400" value="2400" default="true"/>
       <option label="4800" value="4800"/>
       <option label="9600" value="9600"/>
       <option label="19200" value="19200"/>
       <option label="38400" value="38400"/>
       <option label="57600" value="57600"/>
       <option label="115200" value="115200"/>
     </options>
   </param>
   <param field="Mode3" label="Debug" width="75px">
     <options>
       <option label="false" value="false" default="true"/>
       <option label="true" value="true"/>
     </options>
   </param>
</params>
</plugin>
"""

import Domoticz
import serial
import re
import time
import datetime

class BasePlugin:
    def __init__(self):
        self.serial_port = None
        self.baudrate = 2400  # Domyślny baudrate
        self.debug = False
        self.pollinterval = 60
        self.nextpoll = datetime.datetime.now()
        self.qpigs_command = b'\x51\x50\x49\x47\x53\xB7\xA9\x0D'

    def onStart(self):
        serial_port = Parameters["Mode1"]
        self.baudrate = int(Parameters["Mode2"]) if "Mode2" in Parameters else 2400
        self.debug = Parameters["Mode3"] == "true"

        if self.debug:
            Domoticz.Debug(f"Selected serial port: {serial_port}")
            Domoticz.Debug(f"Selected baudrate: {self.baudrate}")

        try:
            self.serial_port = serial.Serial(serial_port, self.baudrate, timeout=1, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            Domoticz.Log(f"Otworzono port {serial_port} z baudrate {self.baudrate}")
        except Exception as e:
            Domoticz.Error(f"Nie udało się otworzyć portu {serial_port}: {str(e)}")
            return
        
        # Odczyt danych po starcie
        self.readData()

    def readData(self):
        if self.serial_port is None:
            Domoticz.Error("Serial port is not open")
            return
        
        try:
            readData = self.serial_port.readline()
            #Domoticz.Log(readData)
            data = readData.decode('utf-8', 'ignore').strip()
            
            match = re.findall(r'\((\d+\.\d+ \d+\.\d+ \d+\.\d+ \d+\.\d+ \d+ \d+ \d+ \d+ \d+\.\d+ \d+ \d+ \d+ \d+ \d+\.\d+ \d+\.\d+ \d+ \d+ \d+ \d+ \d+ \d+)', data)
            
            if len(match) > 0:
                #Domoticz.Log(f"Otrzymane dane: {match[0]}")
                self.parseData(match[0])

        except Exception as e:
            Domoticz.Error(f"Data reading error: {str(e)}")
    
    def parseData(self, data):
        # Przyjmujemy, że dane są w formacie podobnym do: (224.0 50.0 228.0 ...)
        try:
            values = data[0:-1].split()
            Domoticz.Log(f"splitted: {values}")
                
            grid_voltage = float(values[0])
            ac_output_voltage = float(values[2])
            ac_output_power = float(values[5])
            battery_voltage = float(values[8])
            heatSinkTemp = float(values[11])*0.1
            pv_charging_power = float(values[12])
            bat_current = float(values[15])
            pv_voltage = float(values[13])
                
            if 1 in Devices:
                Devices[1].Update(0, str(grid_voltage))
            if 2 in Devices:
                Devices[2].Update(0, str(ac_output_voltage))
            if 3 in Devices:
                Devices[3].Update(0, f"{str(ac_output_power)};0")
            if 4 in Devices:
                Devices[4].Update(0, str(battery_voltage))
            if 5 in Devices:
                Devices[5].Update(0, str(pv_charging_power))
            if 6 in Devices:
                Devices[6].Update(0, str(bat_current))
            if 7 in Devices:
                Devices[7].Update(0, str(pv_voltage))
            if 8 in Devices:
                Devices[8].Update(0, str(heatSinkTemp))

        except Exception as e:
            Domoticz.Error(f"Data parsing error: {str(e)}")

    def onStop(self):
        if self.serial_port is not None:
            self.serial_port.close()
            Domoticz.Log("Port szeregowy został zamknięty.")

    def onHeartbeat(self):
        now = datetime.datetime.now()
        if now < self.nextpoll:
            Domoticz.Debug(f"Awaiting next poll: {self.nextpoll}")
            return
        
        self.serial_port.write(self.qpigs_command)
        time.sleep(2)
        self.readData()
        self.postponeNextPool(self.pollinterval)
        
    def postponeNextPool(self, seconds=3600):
        self.nextpoll = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        return self.nextpoll

# Funkcja rejestrująca urządzenia w Domoticz
def registerDevices():
    if 1 not in Devices:
        Domoticz.Device(Name="Grid Voltage", Unit=1, Type=243, Subtype=8).Create()
    if 2 not in Devices:
        Domoticz.Device(Name="AC Output Voltage", Unit=2, Type=243, Subtype=8).Create()
    if 3 not in Devices:
        Domoticz.Device(Name="AC Output Power", Unit=3, TypeName="kWh").Create()
    if 4 not in Devices:
        Domoticz.Device(Name="Battery Voltage", Unit=4, Type=243, Subtype=8).Create()
    if 5 not in Devices:
        Domoticz.Device(Name="PV Current", Unit=5, Type=243, Subtype=23).Create()
    if 6 not in Devices:
        Domoticz.Device(Name="Battery discharge current", Unit=6, Type=243, Subtype=23).Create()
    if 7 not in Devices:
        Domoticz.Device(Name="PV Voltage", Unit=7, Type=243, Subtype=8).Create()
    if 8 not in Devices:
        Domoticz.Device(Name="Heat sink temp.", Unit=8, TypeName="Temperature").Create()

# Wywoływana na starcie
def onStart():
    Domoticz.Log("Easun Inverter Plugin started")
    registerDevices()
    global _plugin
    _plugin = BasePlugin()
    _plugin.onStart()

# Wywoływana przy zatrzymaniu pluginu
def onStop():
    global _plugin
    if _plugin is not None:
        _plugin.onStop()

# Wywoływana na każdy heartbeat
def onHeartbeat():
    global _plugin
    if _plugin is not None:
        _plugin.onHeartbeat()

# Funkcje debugowania
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug(f"'{x}':'{str(Parameters[x])}'")
    Domoticz.Debug(f"Device count: {len(Devices)}")
    for x in Devices:
        Domoticz.Debug(f"Device: {str(x)} - {str(Devices[x])}")

