from flask import Flask, render_template, request, Response
from subprocess import Popen, PIPE, STDOUT
from argparse import ArgumentParser
import sys

app = Flask(__name__)

class Args(object):
  script = 'test.sh'

args = Args()

@app.route("/")
def hello():
  return render_template('first.html')

@app.route("/remoteCopy")
def remoteCopy():
  return render_template('remoteCopy.html')

@app.route("/runRemoteCopy")
def runRemoteCopy():
  from_dir  = request.values.get("from")
  to_dir  = request.values.get("to")
  def inner():
    cmd = ['rsync', '-razq', from_dir, to_dir] 
    try:
      proc = Popen(cmd,stdout=PIPE,stderr=STDOUT,stdin=PIPE)
      for line in iter(proc.stdout.readline,''):
        yield line.rstrip() + b'<br/>\n'
      proc.wait()
      yield 'All done'

    except BaseException as e:
      yield str(e) + '<br/>\n' 
	
  return Response(inner(), mimetype='text/html')	
        

@app.route("/runInitScripts")
def runScripts():
  dirpath  = request.values.get("dir")
  #print(dirpath)
  def inner():
    cmd = ['scripts/' + args.script, dirpath] 
    try:
      proc = Popen(cmd,stdout=PIPE,stderr=PIPE,stdin=PIPE)
      for line in iter(proc.stdout.readline,''):
        yield line.rstrip() + b'<br/>\n'
    except BaseException as e:
      yield str(e) + '<br/>\n' 
	
  return Response(inner(), mimetype='text/html')	
        

@app.route("/train")
def train():
  def inner():
    try:
      proc = Popen(
        ["processes/train.py"],   #call something with a lot of output so we can see it
        shell=True,
        stdout=PIPE
      )

      for line in iter(proc.stdout.readline,''):
        yield line.rstrip() + b'<br/>\n'

    except BaseException as e:
      yield str(e) + '<br/>\n' 


  return Response(inner(), mimetype='text/html')  # text/html is required for most browsers to show the page


if __name__ == "__main__":
  parser = ArgumentParser(description='Run a web server that starts local scripts')
  parser.add_argument('--script', '-s', default='test.sh', help='Script to run')
  parser.parse_args(sys.argv[1:], args)

  try:
    app.run(host='0.0.0.0',port=8080)
  except KeyboardInterrupt:
    pass
 
