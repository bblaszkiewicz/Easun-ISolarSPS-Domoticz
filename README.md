# Domoticz & EAsun ISolar SPS integration

![domoticz_logotyp_mini-330x220](https://github.com/user-attachments/assets/6140e90a-1314-438c-84c9-5bc1fdcc595b)</br>
<img src=https://github.com/user-attachments/assets/e15dbf2d-0e31-4608-95f3-75a2a1bdb771 width=200 />

Plugin for reading data from the EAsun inverter via RS232. Tested on Raspbery Pi 4B with [RS485 RS232 HAT extension](https://www.waveshare.com/wiki/RS485_RS232_HAT). Currently, it allows reading grid voltage, output voltage, battery voltage, PV current, battery discharge current, output power and heat sink temperature
## Electrical connection
The inverter has an RS232 port on an 8P8C (RJ45) connector. Below is a diagram of the connection cable.
![image](https://github.com/user-attachments/assets/3382f8d2-5554-4c20-b098-b665d3bf75fe)

## Installation
Navigate to the plugin directory and install the plugin straight from github
```
cd domoticz/plugins
git clone https://github.com/bblaszkiewicz/Easun-ISolarSPS-Domoticz.git EAsun
```
Next, restart Domoticz so that it will find the plugin
```
sudo systemctl restart domoticz.service
```
## Plugin update
Go to plugin folder and pull new version
```
cd domoticz/plugins/EAsun
git pull
```
Restart domoticz
```
sudo systemctl restart domoticz.service
```
