# qrcode
### QR code plugin for [RetroBBS](https://github.com/retrocomputacion/retrobbs), by Durandal/Retrocomputacion
</br>

This plugin will render a **QR code** in *PETSCII* semigraphic characters.

Maximum string length is 153 characters.

## Requirements:
 * QRCode
 
  use
  
  ```
  pip install qrcode
  ```
  
  to install.

## Installation:
Just copy `qr.py` to the `plugins` directory in your _RetroBBS_ installation.

If your BBS is running, you must restart it for the plugin to get loaded.

## Usage:

Use the following keys in your _RetroBBS_ configuration file.

| key | description
|:---:|:---
| `entryZtitle`[^1] | The text to be shown in the menu screen
| `entryZfunc` | Set the function to `QRCODE` to use this plugin
| `entryZtext` | The text to encode, max 153 characters in length


[^1]: Replace Z in the configuration file parameters with the adequate entry ID number.