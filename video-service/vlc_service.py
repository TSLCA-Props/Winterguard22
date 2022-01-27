# pylint: disable=broad-except
'''
Micro-service for VLC.
'''
import ctypes
from datetime import datetime
from datetime import timedelta
import os
import  platform
import tkinter as tk
from threading import Thread
import vlc
from flask import Flask
from flask import json
from flask import request
from flask import make_response
from flask import Response
from waitress import serve


app = Flask(__name__)

VERSION='1.0.10splash'
SERVICE_PORT=5000

class WaitressThread(Thread):
    '''
    Thread class for waitress
    '''

    def __init__(self):
        super().__init__()
        # Make daemon so system run forever
        self.daemon = True

    def run(self):
        serve(app, host='0.0.0.0', port=SERVICE_PORT)


def error_response(path : str, message: str, status_code : int) -> Response:
    '''
    Return a JSON response with an error message.
    '''
    return make_response({'path': path, 'error': message}, status_code)


@app.route('/api/v1/play', methods=['POST'])
def play() -> Response:
    '''
    Play a media file.
    url parameters:
        - file: media file to play
        - start: start video on load, true or false.  Default is true.
    '''
    try:
        # test for valid parameters
        valid_params = ['file', 'start']
        params = request.args
        for param in params:
            if param not in valid_params:
                return error_response(request.path, 'Unknown parameter: ' + param, 400)

        media_file_arg =  request.args.get('file')
        if media_file_arg is None:
            return error_response(request.path, 'No file name provided', 400)

        media_file_name = os.path.join('media', media_file_arg)
        if not os.path.isfile(media_file_name):
            return error_response(request.path, 'File does not exist ' + media_file_name, 400)

        start_video = True
        if 'start' in request.args:
            if request.args.get('start') == 'true':
                start_video = True
            elif request.args.get('start') == 'false':
                start_video = False
            else:
                status_msg = 'start parameter must be equal true or false.  Input was {0}'
                return error_response(request.path,status_msg.format(request.args.get('start')),400)

        play_media_file(media_file_name, start_video)
        return ('',200)
    except Exception as ex:
        return error_response(request.path, str(ex), 500)

def play_media_file(media_file_name : str, start_video : bool) -> None:
    """ Play media file """
    media_input = vlcInstance.media_new(media_file_name)
    if not start_video:
        media_input.add_option(':start-paused')

    media_player.set_media(media_input)
    media_player.set_fullscreen(True)
    media_player.play()


@app.route('/api/v1/position', methods=['POST'])
def position() -> Response:
    '''
    Play a media file at a specific position.
    url parameters:
        - percent: position in percent to play
        - time: position in time to play
    '''
    try:
        # test for valid parameters
        valid_params = ['percent', 'time']
        params = request.args
        for param in params:
            if param not in valid_params:
                return error_response(request.path, 'Unknown parameter: ' + param, 400)

        position_arg =  request.args.get('percent')
        timedelta_arg = request.args.get('time')
        if position_arg is None and timedelta_arg is None:
            return error_response(request.path, 'No Position or time provided', 400)


        if (media_player.get_state() == vlc.State.Ended or
             media_player.get_state() == vlc.State.Stopped):
            media_player.set_media(media_player.get_media())
            media_player.play()

        position_value = 0.0
        if timedelta_arg is not None:
            time_d = datetime.strptime(timedelta_arg,"%H:%M:%S.%f")
            time_position = timedelta(  hours=time_d.hour,
                                        minutes=time_d.minute,
                                        seconds=time_d.second,
                                        microseconds=time_d.microsecond).total_seconds() * 1000
            media_length = media_player.get_media().get_duration()
            if time_position > media_length:
                return error_response(request.path, 'Time provided greater than media length', 400)
            position_value = time_position / media_length
        elif position_arg is not None:
            position_value = float(position_arg)
            if (position_value < 0.0) or (position_value > 1.0):
                return error_response(request.path, 'Position must be between 0 and 1.00', 400)

        media_player.set_position(position_value)
        if media_player.get_state() == vlc.State.Paused:
            media_player.pause()

        return ('',200)
    except Exception as ex:
        return error_response(request.path, str(ex), 500)

@app.route('/api/v1/pause', methods=['POST'])
def pause_resume() -> Response:
    '''
    Pause the media file. Resume if already paused.
    '''
    try:
        media_player.pause()
        return ('',200)
    except Exception as ex:
        return error_response(request.path, str(ex), 500)



@app.route('/api/v1/stop', methods=['POST'])
def stop() -> Response:
    '''
    Stop the media player.
    '''
    try:
        media_player.stop()
        return '',200
    except Exception as ex:
        return error_response(request.path,  str(ex), 500)


@app.route('/api/v1/list', methods=['GET'])
def list_media() -> Response:
    '''
    List all available media files.
    '''
    try:
        dir_list = os.listdir('media')
        resp = app.response_class(
            response=json.dumps(dir_list),
            status=200,
            mimetype='application/json'
        )
        return resp
    except Exception as ex:
        return error_response(request.path,  str(ex), 500)


@app.route('/api/v1/snapshot', methods=['GET'])
def take_snapshot() -> Response:
    '''
    Snapshot the current video frame.
    '''
    try:
        media_player.video_take_snapshot(0, 'snapshot.png', 0, 0)
        with open('snapshot.png', 'rb') as snapshot_file:
            png_data = snapshot_file.read()
        resp = app.response_class(
            response=png_data,
            status=200,
            mimetype='image/png'
        )
        return resp
    except Exception as ex:
        return error_response(request.path,  str(ex), 500)

@app.route('/api/v1/status', methods=['GET'])
def status() -> Response:
    '''
    Get the current status of the media player.
    '''
    try:
        state = None
        state_value = media_player.get_state()
        if state_value == vlc.State.Ended:
            state = 'Ended'
        elif state_value == vlc.State.Playing:
            state = 'Playing'
        elif state_value == vlc.State.Paused:
            state = 'Paused'
        elif state_value == vlc.State.Stopped:
            state = 'Stopped'
        elif state_value == vlc.State.Error:
            state = 'Error'
        elif state_value == vlc.State.Opening:
            state = 'Opening'
        elif state_value == vlc.State.Buffering:
            state = 'Buffering'
        elif state_value == vlc.State.NothingSpecial:
            state = 'NothingSpecial'

        load_media = media_player.get_media()
        if load_media is None:
            file = 'No file selected'
            current_position = 0.0
            time_position = "00:00:00.000"
            media_length = '0:00:00'
        else:
            file = load_media.get_mrl()
            current_position = media_player.get_position()
            time_position = str(timedelta(milliseconds=media_player.get_time()))
            media_length = str(timedelta(milliseconds=media_player.get_media().get_duration()))

        resp = app.response_class(
            response=json.dumps(
                {
                    'server_version': VERSION,
                    'vlc_version': str(vlc.libvlc_get_version()),
                    'os_version': str(platform.platform()),
                    'os': platform.system(),
                    'state': state,
                    'file': file,
                    'position_percent:': current_position,
                    'position_time': time_position,
                    'length' : media_length
                }),
            status=200,
            mimetype='application/json'
        )
        return resp
    except Exception as ex:
        return error_response(request.path,  str(ex), 500)

# creating vlc media player object
vlcInstance = vlc.Instance()

# don't run on top when debugging
#vlcInstance = vlc.Instance('--video-on-top')

media_player = vlcInstance.media_player_new()

# Make sure XInitThreads is called before any Xlib commands
if platform.system() == 'Linux':
    x11 = ctypes.CDLL('libX11.so')
    x11.XInitThreads()


# TK stuff to create a window to display video
tkRoot = tk.Tk()
tkRoot.configure(bg='black')
tkRoot.wm_attributes('-fullscreen','true')
main_frame = tk.Frame(tkRoot)
main_frame.config(background='black', cursor='none')
main_frame.pack(fill=tk.BOTH, expand=tk.TRUE)

if platform.system() == 'Linux':
    media_player.set_xwindow(main_frame.winfo_id())
elif platform.system() == 'Windows':
    media_player.set_hwnd(main_frame.winfo_id())

media_player.toggle_fullscreen()

# load the default image
try:
    startup_media_file_name = os.path.join('media', 'tarpon_TV_scaled_1920.png')
    play_media_file(startup_media_file_name, True)
except Exception as startup_ex:
    print(str(startup_ex))


if __name__ == '__main__':
    # Run waitress in it own thread so TK can be in the main
    waitressThread = WaitressThread()
    waitressThread.start()

    tkRoot.configure(cursor='none')
    tkRoot.mainloop()
