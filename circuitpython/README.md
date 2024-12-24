# Clock

## Library Install

The library steps here may not be 100% correct as I am writing this well after I got the clock working. I know for a fact that I had to install tzdb.

- [tzdb documentation](https://circuitpython-tzdb.readthedocs.io/en/latest/)

The [timezone database can be referenced by looking in the Github repo](https://github.com/evindunn/circuitpython_tzdb/tree/main/tzdb/_zones).

Using `circup` to manage software on the device.
<https://github.com/adafruit/circup>

```
circup update
circup install tzdb
circup install adafruit_ntp
circup install socketpool
```

## CircuitPython documentation

The library files in the 'lib' directory are originally from Adafruit's bundle of handy CircuitPython code. The version that ships with the Tiny TRS-80s was released on 5 September 2023. You can find that bundle on the [release page for that day](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20230905) with the file name 'adafruit-circuitpython-bundle-8.x-mpy-20230905.zip'. [direct link](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20230905/adafruit-circuitpython-bundle-8.x-mpy-20230905.zip)

To add a library, unzip that bundle and find the referenced library (e.g. `adafruit_ble_radio.mpy`) and copy it into the `lib` directory on your tiny model III. Your code.py file will then be able to import that library like `import adafruit_ble_radio`..

To set up WiFi, copy settings.toml.example to settings.toml (in the same directory) and then edit it to enter your WiFi SSID and password.
