# Raspberry PI desktop Auto Start

## Auto start using lxsession user mode

Desktop Apps/Scripts can be started after the GUI desktop and the default user is logged in to the system.

* Make sure the raspi-config is setup for
  * System Option/Boot Auto Login/Desktop Auto Login - pi  
* Add an autostart file to the .config/lxsession/LXDE-pi directory.
  * A sample is provided in this directory
  * Any scripts will need to be executable
    * `chmod a+rwx [script name]`
    * Make sure script file start with
    * `#!/usr/bin`
* An example of a startup script can be found in `../scripts`

## Desktop wall paper

* An example of setting the desktop wallpaper (`TSLCA Color guard`) can be found in
`.config/pcmanfm/LXDE/desktop-items-0.conf`

## References

* [STICKY: How to use Autostart - Raspberry Pi (OS Desktop)](https://forums.raspberrypi.com/viewtopic.php?t=294014)
* [LXDE Autostart](https://wiki.archlinux.org/title/LXDE#Autostart)
