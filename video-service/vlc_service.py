# pylint: disable=broad-except
'''
Micro-service for VLC.
'''
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
from waitress import serve


app = Flask(__name__)

VERSION='1.0.0'

class WaitressThread(Thread):
    '''
    Thread class for waitress
    '''

    def __init__(self):
        super().__init__()
        # Make daemon so system run forever
        self.daemon = True

    def run(self):
        serve(app, host='0.0.0.0', port=5000)


def error_response(path, message, status_code):
    '''
    Return a JSON response with an error message.
    '''
    response = json.dumps({'path': path, 'error': message})
    return response, status_code


@app.route('/api/v1/play', methods=['POST'])
def play():
    '''
    Play a media file.
    '''
    try:
        media_file_arg =  request.args.get('file')
        if media_file_arg is None:
            return error_response(request.path, 'No file name provided', 400)

        media_file_name = os.path.join('media', media_file_arg)
        if not os.path.isfile(media_file_name):
            return error_response(request.path, 'File does not exist ' + media_file_name, 400)

        media_player.set_media(vlcInstance.media_new(media_file_name))
        media_player.set_fullscreen(True)
        media_player.play()
        return ('',200)
    except Exception as ex:
        return error_response(request.path, str(ex), 500)


@app.route('/api/v1/position', methods=['POST'])
def position():
    '''
    Play a media file at a specific position.
    '''
    try:
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
            if time_position > media_player.get_length():
                return error_response(request.path, 'Time provided greater than media length', 400)
            position_value = time_position / media_player.get_length()
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
def pause_resume():
    '''
    Pause the media file. Resume if already paused.
    '''
    try:
        media_player.pause()
        return ('',200)
    except Exception as ex:
        return error_response(request.path, str(ex), 500)



@app.route('/api/v1/stop', methods=['POST'])
def stop():
    '''
    Stop the media player.
    '''
    try:
        media_player.stop()
        return '',200
    except Exception as ex:
        return error_response(request.path,  str(ex), 500)


@app.route('/api/v1/list', methods=['GET'])
def list_media():
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


@app.route('/api/v1/status', methods=['GET'])
def status():
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
            media_length = str(timedelta(milliseconds=media_player.get_length()))

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
#vlcInstane = vlc.Instance('--video-on-top')

media_player = vlcInstance.media_player_new()

# TK stuff for windows
tkRoot = tk.Tk()
tkRoot.configure(bg='black')
tkRoot.wm_attributes('-fullscreen','true')

media_player.set_xwindow(tkRoot.winfo_id())

media_player.toggle_fullscreen()

if __name__ == '__main__':
    # Run waitress in it own thread so TK can be in the main
    waitressThread = WaitressThread()
    waitressThread.start()

    tkRoot.mainloop()
