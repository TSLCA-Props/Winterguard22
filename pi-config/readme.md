# Raspberry Pi 3 Config

## Configuration tools

```bash
sudo raspi-config
```

See: [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#raspi-config)

![Main screen](raspi-config-main.png "Main Screen")

### Boot option

Select the `Desktop Autologin` option
![System Options](raspi-config-boot.png "System Options")

**Note** The default user is `pi` and password is `raspberry`.
We may want to change the password.

See: [Raspberry Pi Documentation Linux](https://www.raspberrypi.com/documentation/computers/using_linux.html)

### Display Options

Disable Screen blanking (Alway keep the screen on)

![Display Options](raspi-config-display.png "Display Options")

### Interface options

Select the required interface needed for the specific pi.
All should turn on the `SSH` and `VNC` interfaces which might be required for trouble shooting.

![Interface Options](raspi-config-interface.png "Interface Options")

### Advanced Options

The PI 3 required the `Glamor` option for hardware acceleration.

![Advanced Options](raspi-config-advanced.png "Advanced Options")

Also on the same menu, change the `GL Driver`

![Graphics Driver](raspi-config-graphics-driver.png "Graphics Driver")

## Other Configuration

### config.txt

The raspberry PI does not drive video output if the TV (HDMI device) is not on during power up.  This can be forced by adding the following lines to the `/boot/config.txt` file.

```text
hdmi_force_hotplug=1
hdmi_group=1
hdmi_mode=16
```

**Note:** The key are already in the config.txt file.
They just need to be uncommented and the correct value added.

See: [Documentation config.txt: HDMI Mode](https://www.raspberrypi.com/documentation/computers/config_txt.html#hdmi-mode)

## Desktop Setup

Set the background to black.

Right click on desktop and select `Desktop Preferences`
![Desktop Menu](desktop-menu.png "Desktop Menu")

Change the `Wallpaper mode` to `Fill with background color only` and set `Background color` to black.
![Desktop Preferences](desktop-preferences.png "Desktop Menu")
