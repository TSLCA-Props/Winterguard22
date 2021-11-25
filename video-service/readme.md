# VLC service
The video service is a rest api micro-service wrapping the VLC media player.

## Service port
**5000**

example:
```
http://xxx.xxx.xxx.xxx:5000/api/v1/list
```
## API
___
### Play
`POST /api/v1/play?file=[media file name]`

Play a media file in VLC. Use the `list` api to see a list of media files on the server.

Response:
* 200 on success
* otherwise error code with description in the body
___

___
### Stop
`POST /api/v1/stop`

Stop the current media file in VLC.

Response:
* 200 on success
* otherwise error code with description in the body
___

___
### List
`GET /api/v1/list`

Return an array of media file names available on the server.

Response:
* 200 on success
  * Json body (Just an array of strings)
  ```
  [
    "banksy001.gif",
    "banksy002.gif",
    "banksy003.gif",
    "testvid.mov"
  ]
  ```
* otherwise error code with description in the body
___

___
### Status
`POST /api/v1/status`

Return the current VLC status

Response:
* 200 on success
  * Json body
```
{
  "file": "file:///C:/git-repo/tslc/video-server/media/testvid.mov",
  "state": "Playing"
}  
```

  * state value
    * 'NothingSpecial',
    * 'Opening',
    * 'Buffering',
    * 'Playing',
    * 'Paused',
    * 'Stopped',
    * 'Ended',
    * 'Error'

* otherwise error code with description in the body
___


# Running
```
python vlc-service.py
```
**Note:** Assumes the required modules have been installed. (VLC, pip modules).  Also, if using venv, then the virtual environment should be start prior to running.


# Requirements
* [Python](https://www.python.org/downloads/) 3.7 and above
* Pip Modules
	* [python-vlc](https://pypi.org/project/python-vlc/)
	* [flask](https://pypi.org/project/Flask/)
	* [waitress](https://pypi.org/project/waitress/)

___
  **Note:** python modules should be installed using venv.  They can be put in the global modules, but versioning issue can occur in the future.
___
* [VLC](https://www.videolan.org/) (VideoLAN Organization)
  * [Linux install](https://www.videolan.org/vlc/download-debian.html) -  `sudo apt install vlc` 
  * [Windows Install](https://www.videolan.org/vlc/download-windows.html) - download installer

* [Visual Studio Code](https://code.visualstudio.com/) (optional)
  * [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  * [GitHub Repositories](https://marketplace.visualstudio.com/items?itemName=GitHub.remotehub) -- Or some other git extension
  * [Kite Autocomplete Plugin for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=kiteco.kite) -- Auto code complete for python.  Similar to Code Pilot.
  * [Markdown Support for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)
  * [Visual Studio Code Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
    * Remote SSH
    * Remote WSL
    * Remote Editing
* [Postman](https://www.postman.com/) - Rest API tool (optional)
	