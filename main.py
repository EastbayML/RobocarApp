from flask import Flask, flash, redirect, render_template,request,session 
from  subprocess import Popen,PIPE
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('first.html')

@app.route("/runInitScripts")
def runScripts():
        dirpath  = request.values.get("dir")
        print dirpath
        cmd = ["scripts/test.sh"] 
        p = Popen(cmd,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        with p.stdout:
		for line in iter(p.stdout.readline,b''):
			print line
        p.wait()
	return "Processing Complete"

if __name__ == "__main__":
	app.run()
