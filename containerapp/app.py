from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    jobID = data.get('jobId')
    object = data.get('object')

    # Setting environment variable in a subprocess
    command = f'export MEDIA={object}; /entrypoint.sh'
    subprocess.run(['/bin/bash', '-c', command])

    return 'Environment variable set successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
