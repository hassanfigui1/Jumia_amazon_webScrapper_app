from flask import Flask
from flask import render_template
from flask import request
import json
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('scraper.html')
    
@app.route('/run', methods=['POST'])
def run():
    category = request.form.get('category')
    
    settings = ''
    
    with open('settings.json', 'r') as f:
        for line in f.read():
            settings += line
    
    settings = json.loads(settings)
    
    settings['category'] = category
    
    with open('settings.json', 'w') as f:
        f.write(json.dumps(settings, indent=4))
    
    process2 = subprocess.Popen('python3 Amazon.py', shell=True)
    process2.wait()
    process = subprocess.Popen('python3 Jumia.py', shell=True)
    process.wait()

    output = ''
    
    with open('data.json', 'r') as f:
        for line in f.read():
            output += line    
    output = [json.loads(item + '\n}') for item in output.split('}\n')[0:-1]]
    
    return {'data': output}

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
