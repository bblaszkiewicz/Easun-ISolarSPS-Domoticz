# FoxESS & EAsun ISolar SPS integration

![domoticz_logotyp_mini-330x220](https://github.com/user-attachments/assets/6140e90a-1314-438c-84c9-5bc1fdcc595b)</br>
<img src=https://github.com/user-attachments/assets/e15dbf2d-0e31-4608-95f3-75a2a1bdb771 width=200 />

Plugin for reading data from the EAsun inverter. Currently, it allows reading grid voltage, output voltage, battery voltage, PV current, battery discharge current, output power and heat sink temperature
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
