#!flask/bin/python
from flask import Flask, send_file, render_template
import MicroserviceBackend.DataViewService.viewclustering as pclustview
import MicroserviceBackend.DataViewService.plotclustering as pclust

app = Flask(__name__)

@app.route('/')
def index():

    pclust.plotClustering()

    return "You have just executed the Clustering Plotting Service!"

@app.route('/main.png')
def main_plot():
    """The view for rendering the scatter chart"""
    img = pclustview.viewClustering()
    return send_file(img, mimetype='image/png', cache_timeout=0)

@app.route('/mainpage')
def main():
    """Entry point; the view for the main page"""
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True, port=5002)

