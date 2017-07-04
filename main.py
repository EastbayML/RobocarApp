from flask import Flask, render_template, request, Response
from subprocess import Popen, PIPE
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('first.html')

@app.route("/runInitScripts")
def runScripts():
  dirpath  = request.values.get("dir")
  print(dirpath)
  def inner():
    cmd = ["scripts/test.sh"] 
    proc = Popen(cmd,stdout=PIPE,stderr=PIPE,stdin=PIPE)
    for line in iter(proc.stdout.readline,''):
      yield line.rstrip() + '<br/>\n'
	
  return Response(inner(), mimetype='text/html')	
        

@app.route("/train")
def train():
  def inner():
    proc = Popen(
        ["processes/train.py"],             #call something with a lot of output so we can see it
        shell=True,
        stdout=PIPE
    )

    for line in iter(proc.stdout.readline,''):
        yield line.rstrip() + '<br/>\n'

  return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show the page


if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080)
 
