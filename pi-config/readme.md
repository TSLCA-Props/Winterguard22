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

Also on the same menu, change the `GL Driver` to `Legacy`

![Graphics Driver](raspi-config-graphics-driver.png "Graphics Driver")

## Other Configuration

## Desktop Setup

Set the background to black.

Right click on desktop and select `Desktop Preferences`
![Desktop Menu](desktop-menu.png "Desktop Menu")

Change the `Wallpaper mode` to `Fill with background color only` and set `Background color` to black.
![Desktop Preferences](desktop-preferences.png "Desktop Menu")
