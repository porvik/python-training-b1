import flask
import os
import json

webserver = flask.Flask(__name__)

def get_built_packages():
    files_to_server = [os.path.basename(entry) for entry in os.scandir('../../module_2/dist')]
    return files_to_server

@webserver.route('/')
def index():
    return flask.render_template('index.html', files_to_serve=get_built_packages())

@webserver.route('/files')
def get_file_list():
    return json.dumps(get_built_packages())

@webserver.route('/files/<path:path>')
def serve_a_file(path):
    print('../../module_2/dist/{}'.format(path))
    return flask.send_file('../../../module_2/dist/{}'.format(path))

if __name__ == '__main__':
    webserver.run(host='0.0.0.0', port=5000)
