activate_this = '/var/www/wms_creator/.env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/var/www/wms_creator/')
from mapapp import app as application 
