# Geotube v1.0

**Find YouTube videos by location, keyword, or live status — built with Flask/Python.**

Geotube lets you drop a pin on a map and pull back YouTube videos published near that location, or search live streams by keyword. Originally built in 2018, now running on OpenStreetMap/Leaflet (migrated off Google Maps) and the YouTube Data API v3.

**Live demo:** http://geotube.pythonanywhere.com/

---

## Features

- 🗺️ **Search by location** — click a point on the map (or type coordinates) and set a radius to find geotagged videos nearby
- 🔴 **Live stream search** — search currently live videos by keyword
- 🎚️ **Optional filters** — narrow results by publish date range, keyword, max views, max subscribers, and max comments
- 📊 **Result details** — title, view count, channel subscriber count, comment count, and a direct link to each video
- 🔒 **No data storage** — searches and results are not logged, saved, or stored (see Privacy Policy in-app)

---

## Screenshots

### Search by map location (with optional filters)
![Search by location](/docs/geo1.png)

### Full Search Options
![Search live streams](/docs/geo3.png)

### Search Live videos by Keyword

![Results](/docs/geo4.png)

### Results page

![Results detail](/docs/geo5.png)

---

## Tech Stack

- **Backend:** Python, Flask, Flask-WTF
- **Frontend:** Leaflet.js + OpenStreetMap tiles
- **API:** [YouTube Data API v3](https://developers.google.com/youtube/v3) (`google-api-python-client`)

---

## Requirements

- Python 3.7+
- A [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) key

### Install dependencies

```bash
pip install flask flask-wtf wtforms google-api-python-client
```

---

## Configuration

Set your YouTube API key in `youtube_flask.py`:

```python
DEVELOPER_KEY = 'YOUR_YOUTUBE_API_KEY'
```

Set a Flask secret key via environment variable (recommended) or in `config.py`:

```bash
export SECRET_KEY='your-secret-key-here'
```

`config.py` also controls the app version string (`VERSION`).

---

## Running locally

```bash
python flask_app.py
```

Then visit `http://localhost:5000` in your browser.

---

## Usage notes

- Results are capped at the **first 1,000 results** per search. So use filters wisely.
- The "Move Map Pin Here" button syncs manually typed coordinates back to the map marker and radius circle.
- Recommended: Chrome with the [Google Translate extension](https://chrome.google.com/webstore/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb) for viewing videos in other languages.

---

## Privacy

This app uses YouTube API Services. Use of the app assumes agreement with the [YouTube Terms of Service](https://www.youtube.com/t/terms) and [Google Privacy Policy](http://www.google.com/policies/privacy). No search data or visitor data is collected, saved, or stored.

---

## License

For educational and entertainment purposes only.