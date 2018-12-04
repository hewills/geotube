from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from config import Config
from app.forms import LoginForm, SearchDateForm, SearchLiveForm
from app.youtube import YouTube

app = Flask(__name__)
app.config.from_object(Config)

# Run Youtube search by Location -----------
def search_location(form):
    version = app.config['VERSION']

    ll = request.form['lat_long']
    rad = request.form['radius']
    pub_before = request.form.get('pub_before')
    pub_after = request.form.get('pub_after') #Returns format 2018-09-01
    keyword = request.form.get('keyword')
    live = request.form.get('live_only')

    # Youtube search based on location and radius
    yt = YouTube(ll,rad,live,pub_after,pub_before,keyword,'index')
    yt.search()

    return render_template('vids.html', title='RESULTS',version=version,lat_long=ll,radius=rad, yt=yt)

# Run Youtube search by Date -----------
def search_date(form):
    version = app.config['VERSION']

    pub_before = request.form.get('pub_before')
    pub_after = request.form.get('pub_after') #Returns format 2018-09-01
    keyword = request.form.get('keyword')
    live = request.form.get('live_only')

    # Youtube search based on location and radius
    yt = YouTube('','',live,pub_after,pub_before,keyword,'index2')
    yt.search()

    return render_template('vids.html', title='RESULTS',version=version,lat_long='',radius='', yt=yt)
    
# Run Youtube search Live Only -----------
def search_live(form):
    version = app.config['VERSION']

    keyword = request.form.get('keyword')
    live = 'y'
    
    # Youtube search based on location and radius
    yt = YouTube('','',live,'','',keyword,'index3')
    yt.search()

    return render_template('vids.html', title='RESULTS',version=version,lat_long='',radius='', yt=yt)

# Index - Home Page (videos by Location)
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    version = app.config['VERSION']
    map_key = app.config['MAP_KEY']

    form = LoginForm()

    if form.validate_on_submit():
        return search_location(form)

    return render_template('index.html', title='Home', version=version, form=form, map_key=map_key)

# Index - Page (videos by Date and Keyword)
@app.route('/index2', methods=['GET', 'POST'])

def index2():
    version = app.config['VERSION']

    form = SearchDateForm()

    if form.validate_on_submit():
        return search_date(form)

    return render_template('index2.html', title='Home-by Date', version=version, form=form)
    
# Index - Page (Live Only videos by Keyword)
@app.route('/index3', methods=['GET', 'POST'])

def index3():
    version = app.config['VERSION']

    form = SearchLiveForm()

    if form.validate_on_submit():
        return search_live(form)

    return render_template('index3.html', title='Home-Live Only', version=version, form=form)

# About Form --------------------
@app.route('/about')

def about():
    version = app.config['VERSION']
    return render_template('about.html', title="About", version=version)
