# Presenter Trainer - FIOT6 Challenge #

https://github.com/CiABAMBA/fiot6-hackathon.git

## Instructions

### IR Blaster

A mandatory component for our solution is the IR Blaster. We use an "Universal 
WLAN Remote Control." Please have a look at the [online documentation](https://www.heise.de/ct/artikel/Pearls-WLAN-Universalfernbedienung-mit-MQTT-nutzen-4505906.html) (in German).

As an update: you must download the sonoff.bin for v6.5.0. We tried newer versions,
but we could not make them work. In the guide, they recommend to use the [flasher webiste](https://tasmota.github.io/install), 
which must access the UART interface in your computer (only possible via Chrome or Firefox).
Since the blaster is an ESP8266, I doubt it is a good choice.

For flashing, please install ESP-IDF v5.2, once you set it up, you can use `esptool.py`
to flash `sonoff.bin` as shown in the online documentation above. Moreover, you
must connect the IR Blaster to your laptop **correctly**! 

To flash it, you need:

* USB-to-UART bridge, something with CP210x chip 
* Jumper cables
* MicroUSB cable.

Connect the IR Blaster the following:

| IR Blaster | UART Bridge |
|------------|-------------|
|    3V3     | No Connect  |
|    GND     | No Connect  |
|     RX     |     TX      |
|     TX     |     RX      |
|    IO0     |     GND     |

Use the MicroUSB port in the IR Blaster to power it from your laptop. This
powers the ESP8266 correctly. Connecting IO0 to GND puts the ESP8266 in download
mode, necessary for flashing.

Once it is connected correctly, you will se the proper serial device under
`/dev/ttyUSBx` (Linux), `/dev/cu.xxx` (MacOS), or `COMx` (Windows). You can pass
the serial device to `esptool.py` by using `-p <serial device>`. Once the flashing
finishes, you can disconnect the IO0 from GND, and reconnect the MicroUSB; 
the device should start.

You can monitor it by using `screen <serial device> 115200`. You should also see
the WiFi network called `tasmota_xxx` or `sonoffxxxx`. Connect to it, and access
the configuration website via `192.168.4.1`

#### Configuration Website

In this website, there is a plethora of options. However, you **must** configure two.
First, connect the IR Blaster to your WiFi network by providing the WiFi Credentials.
Once this occurs, you can access the IR Blaster whenever it is connected to the
configured network.

Using the IP for the IR Blaster within the WiFi Network, visit it again to display
the configuration website. Here, you must configure the module:

1. Configuration
2. Configure Module
3. YFT IR Bridge

> The device will restart once you save the configuration.

Once it is configured as an IR Blaster, now you can configure the MQTT parameters.
For this, visit:

1. Configuration
2. Configure MQTT
3. Enter the IP and Port for the MQTT Broker.

      3.1 We use a private broker by installing `mosquitto` in the Raspberry Pi.
         Please look at the [documentation](./assets/HOWTO_mqtt_broker_on_pi.txt) on how
         to setup the broker in the Raspberry Pi.

> Note: Do not change other parameters, especially the topic, as it is preconfigured
> for receiving IR Blaster commands. The topic field in the configuration page
> only changes the base topic.

Once you have set all desired parameters, you can save it. The IR Blaster will 
reboot once again. After this, you can use our code.

> The possible commands to send via IR are available [here](assets/clock_commands.json)


### iDotMatrix

This device is simple to use as you can connect to it via BT. The necessary code
resides [here](./idotmatrix/)

The code here already communicates with the iDotMatrix. It can send images, gifs,
and set countdowns.

### Main code.

To run the code, you only `Miniconda3` and `python3.12`. Once you have created 
the virtual environement, activate and run the following: `pip install -r requirements.txt`.
This should install all necessary dependecies.


With all necessary dependencies installed, you can run the code via `python3 main.py`.

Once this is running, the sentiment analysis, face detection, and website conmtrol components can run, 
which will start sending the emotions to be displayed or the time. Please have a 
look to their documentation to determine how to integrate it.

More configurations for other devices can be found [here](./assets/CONFIGS). 
Although, we did not use them.
