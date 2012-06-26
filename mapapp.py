from flask import Flask, render_template, url_for, request
from mapfilecreation import Mapfile
import glob, os
app = Flask(__name__)

@app.route('/wms_creator/')
def index():
	return render_template('index.html')

@app.route('/wms_creator/dirs/')
@app.route('/wms_creator/dirs/<path:folder>')
def folder_display(folder=None):
	os.chdir('/var/maps/')
	if folder == None:
		filelist = os.walk('./').next()[1]
		folder = './'
	else:
		filelist = glob.glob(str(folder) + '/*')
	filelist.sort()
	url_for('static', filename='css/bootstrap.min.css')
	url_for('static', filename='css/bootstrap-responsive.min.css')
	url_for('static', filename='css/bootstrap-responsive.min.css')
	url_for('static', filename='js/bootstrap.min.js')
	url_for('static', filename='js/bootstrap.min.js')
	return render_template('filelist.html', filelist=filelist)

@app.route('/wms', methods=['POST', 'GET'])
def create_wms():
	error = None
	if request.method == 'POST':
		title = request.form['wms_title']
		directory = '/var/maps/' + request.form['directory'] + '/'
		try:
			if request.form['tiled'] == 'on':
				tiles = True
		except:
			tiles = False
		new_mapfile = Mapfile(title, directory, tiles)
	return render_template('wms.html', wms_title=title, directory=directory)

if __name__ == "__main__":
	app.debug = True
	app.run('0.0.0.0')