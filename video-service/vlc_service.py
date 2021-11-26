# pylint: disable=broad-except
'''
Micro-service for VLC.
'''
import os
import vlc
from flask import Flask
from flask import json
from flask import request


app = Flask(__name__)

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
            return error_response('/api/v1/play', 'No file name provided', 400)

        media_file_name = os.path.join('media', media_file_arg)
        if not os.path.isfile(media_file_name):
            return error_response('/api/v1/play', 'File does not exist ' + media_file_name, 400)

        media_player.set_media(vlcInstance.media_new(media_file_name))
        media_player.set_fullscreen(True)
        media_player.play()
        return ('',200)
    except Exception as ex:
        return error_response(request.path, ex.args[1], 500)


@app.route('/api/v1/stop', methods=['POST'])
def stop():
    '''
    Stop the media player.
    '''
    try:
        media_player.stop()
        return '',200
    except Exception as ex:
        return error_response(request.path,  ex.args[1], 500)


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
        return error_response(request.path,  ex.args[1], 500)


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

        file = media_player.get_media().get_mrl()
        resp = app.response_class(
            response=json.dumps({'state': state, 'file': file}),
            status=200,
            mimetype='application/json'
        )
        return resp
    except Exception as ex:
        return error_response(request.path,  ex.args[1], 500)

# creating vlc media player object
vlcInstance = vlc.Instance()

# don't run on top when debugging
#vlcInstane = vlc.Instance('--video-on-top')

media_player = vlcInstance.media_player_new()
media_player.toggle_fullscreen()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
