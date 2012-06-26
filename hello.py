from flask import Flask, render_template
import glob, os
app = Flask(__name__)


@app.route('/<path:folder>')
def folder_display(folder=None):
	os.chdir('/var/maps/')
	if folder == None:
		filelist = [os.path.split(fileitem)[1] for fileitem in glob.glob('*')]
	else:
		filelist = glob.glob(str(folder) + '/*')
	filelist.sort()
	return render_template('filelist.html', filelist=filelist)

url_for('static', filename='css/bootstrap.css')


if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0')