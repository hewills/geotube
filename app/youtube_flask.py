from datetime import datetime, date, time
from googleapiclient.discovery import build

# ------------------- CONFIG -------------------
DEVELOPER_KEY = 'DEVKEY'  # Replace with your API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULTS_PER_PAGE = 50    # YouTube API max per page
MAX_PAGES = 20               # Max pages to fetch
# ---------------------------------------------

def safe_int(value):
    try:
         # Remove commas if present
        return int(str(value).replace(',', ''))
    except (ValueError, TypeError):
        return 0

class YouTubeSearch:
    """Search YouTube videos by location, keywords, date, and optional subscriber/comment filters."""

    def __init__(self, lat_long=None, rad=None, live=False, pub_after=None, pub_before=None, keyword="",
                 max_subscribers=None, max_comments=None, max_views=None):
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY,cache_discovery=False)
        self.lat_long = lat_long or ""
        self.radius = f"{rad}m" if rad else ""
        self.live_event = live
        self.keyword = keyword or ''
        self.max_subscribers = max_subscribers
        self.max_comments = max_comments
        self.max_views = max_views

        # pub_after and pub_before could be datetime.date or string
        # Convert both to datetime.date first
        if isinstance(pub_after, str):
            pub_after = datetime.strptime(pub_after, "%Y-%m-%d").date()
        if isinstance(pub_before, str):
            pub_before = datetime.strptime(pub_before, "%Y-%m-%d").date()

        # Convert to ISO 8601 format string for YouTube API
        self.pub_after = datetime.combine(pub_after, time.min).isoformat("T") + "Z" if pub_after else None
        self.pub_before = datetime.combine(pub_before, time.min).isoformat("T") + "Z" if pub_before else None

        # Results storage
        self.video_ids = []
        self.video_titles = []
        self.video_views = []
        self.video_comments = []
        self.video_subs = []

        # Results for Flask
        self.list_ids = []
        self.list_titles = []
        self.list_views = []
        self.list_subs = []
        self.list_comments = []

        self.total_results = 0

    # ------------------- HELPER -------------------
    def _batch_channels_stats(self, channel_ids):
        """Fetch subscriber counts in batches of 50."""
        subs_dict = {}

        for i in range(0, len(channel_ids), 50):
            batch_ids = ",".join(channel_ids[i:i+50])
            response = self.youtube.channels().list(
                part="statistics",
                id=batch_ids
            ).execute()
            for item in response.get("items", []):
                subs = int(item["statistics"].get("subscriberCount", 0))
                subs_dict[item["id"]] = subs
        return subs_dict

    # ------------------- SEARCH -------------------
    def search(self):
        next_page_token = None
        page_count = 0

        while page_count < MAX_PAGES:
            search_params = {
                "part": "snippet",
                "type": "video",
                "q": self.keyword,
                "maxResults": MAX_RESULTS_PER_PAGE,
                "order": "viewCount"
            }

            if self.live_event:
                # YouTube API rejects eventType combined with location/locationRadius
                # or publishedAfter/publishedBefore, so live searches skip those.
                search_params["eventType"] = "live"
            else:
                if self.lat_long:
                    search_params["location"] = self.lat_long
                if self.radius:
                    search_params["locationRadius"] = self.radius
                if self.pub_after:
                    search_params["publishedAfter"] = self.pub_after
                if self.pub_before:
                    search_params["publishedBefore"] = self.pub_before

            if next_page_token:
                search_params["pageToken"] = next_page_token

            print(f'search_params: {search_params}')

            search_response = self.youtube.search().list(**search_params).execute()
            # Store total results from YouTube API (only needs to be done once)
            if page_count == 0:
                self.total_results = search_response.get('pageInfo', {}).get('totalResults', 0)

            video_ids_page = [item["id"]["videoId"] for item in search_response.get("items", [])]
            if not video_ids_page:
                break

            # ------------------- VIDEO DETAILS -------------------
            # Always fetch statistics for display; max_views/max_comments/max_subscribers
            # are just optional filters applied below, not gates on fetching the data.
            video_parts = ["snippet", "statistics"]

            video_response = self.youtube.videos().list(
                    part=",".join(video_parts),
                    id=",".join(video_ids_page)
                    ).execute()

            # Collect channel IDs to look up subscriber counts for display
            channel_ids = [v["snippet"]["channelId"] for v in video_response.get("items", [])]
            subs_dict = self._batch_channels_stats(channel_ids)

            for video in video_response.get("items", []):
                title = video["snippet"]["title"]
                views = int(video["statistics"].get("viewCount", 0))
                comments = int(video["statistics"].get("commentCount", 0))
                channel_id = video["snippet"]["channelId"]
                subs = subs_dict.get(channel_id, None)

                # Apply optional filters
                if self.max_subscribers is not None and subs is not None and subs > self.max_subscribers:
                    continue
                if self.max_comments is not None and comments is not None and comments > self.max_comments:
                    continue
                if self.max_views is not None and views is not None and views > self.max_views:
                    continue

                # Store results
                self.video_ids.append(video["id"])
                self.video_titles.append(title)
                self.video_views.append(views)
                self.video_comments.append(comments)
                self.video_subs.append(subs)

            page_count += 1
            next_page_token = search_response.get("nextPageToken", None)
            if not next_page_token:
                break

        self.get_results()

    # ------------------- OUTPUT -------------------
    def get_results(self):

        for i in range(len(self.video_ids)):
            views = safe_int(self.video_views[i])
            subs = safe_int(self.video_subs[i])
            comments = safe_int(self.video_comments[i])

            if self.max_views is not None and views > self.max_views:
                continue
            if self.max_subscribers is not None and subs > self.max_subscribers:
                continue
            if self.max_comments is not None and comments > self.max_comments:
                continue

            self.list_titles.append(self.video_titles[i])
            self.list_views.append(views)
            self.list_subs.append(subs)
            self.list_comments.append(comments)
            self.list_ids.append(self.video_ids[i])

# ------------------- RUN EXAMPLE -------------------
#if __name__ == "__main__":
    #yt = YouTubeSearch(
        #ll="43.21771312896356,3.069356378086354",
        #rad="8000",
        #live=False,
        #pub_after="2020-01-01",
       # pub_before="2020-10-20",
        #keyword="",
        #max_subscribers=None,  # Optional: set to int or None
        #max_comments=None,     # Optional: set to int or None
        #max_views=10           # Optional: set to int or None
    #)
    #yt.search()