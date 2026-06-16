#import argparse
from datetime import datetime#, tzinfo
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps tab of https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'DEVKEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class YouTube:
    """A class to search YouTube and return video IDs"""

    # Initialize youtube search instance
    def __init__(self, ll, rad, live, pub_after, pub_before,keyword,source):

        self.source = source
        self.live_event = live

        if ll:
            self.lat_long = ll
        else:
            self.lat_long = ""

        if rad:
            self.radius = rad + "m"
        else:
            self.radius = ""

        if pub_after:
            self.pub_after = datetime.strptime(pub_after,'%Y-%m-%d').replace(microsecond=0).isoformat("T")+".0Z"  #2018-08-01T00:00:00.0Z
        else:
            self.pub_after = '2005-01-01T00:00:00.000Z'

        if pub_before:
            self.pub_before = datetime.strptime(pub_before,'%Y-%m-%d').replace(microsecond=0).isoformat("T")+".0Z"  #2018-08-01T00:00:00.0Z
        else:
            self.pub_before = '2099-01-01T00:00:00.000Z'

        if keyword:
            self.keyword = keyword
        else:
            self.keyword =""

# ----------- End of class YoutTube ----------------------------


    # Do a youtube search using intialized variables
    def search(self):

        # Setup youtube
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        # Number of pages of results to return
        # num_result_pages * max_results = results limit
        num_result_pages = 20

        # Call the search.list method to retrieve results matching the specified query term.
        if self.source == 'index':
            if self.live_event:
                search_response = youtube.search().list(
                    type='video',
                    q=self.keyword,                                #Search term:       default='kittens'
                    eventType='live',                              #Event type:        default='live'  #completed,live,upcoming
                    location=self.lat_long,                        #Location:          default='43.21771312896356,3.069356378086354'
                    locationRadius=self.radius,                    #Radius:            default='12000m' #80km=50m  1.5km=1m
                    #publishedBefore=options.pubBefore,            #Published before:  default='2018-10-15T18:06:28.187Z'
                    #publishedAfter=options.pubAfter,              #Published after:   default='2018-10-10T18:06:28.187Z'
                    part='snippet',
                    order='viewCount',
                    maxResults=50                             #Max Results:       default=50
                ).execute()
            else:
                search_response = youtube.search().list(
                    part="snippet",
                    location=self.lat_long,
                    locationRadius=self.radius,
                    #publishedBefore=self.pub_before,
                    publishedAfter=self.pub_after,
                    order='viewCount',
                    q=self.keyword,
                    type="video",
                    maxResults=50
                ).execute()

        #print('index search_response: ',search_response)

        if self.source == 'index2' or self.source == 'index3':
            if self.live_event:
                search_response = youtube.search().list(
                    type='video',
                    q=self.keyword,                                #Search term:       default='kittens'
                    eventType='live',                              #Event type:        default='live'  #completed,live,upcoming
                    #publishedBefore=options.pubBefore,            #Published before:  default='2018-10-15T18:06:28.187Z'
                    #publishedAfter=options.pubAfter,              #Published after:   default='2018-10-10T18:06:28.187Z'
                    part='snippet',
                    order='viewCount',
                    maxResults=50                                #Max Results:       default=50
                ).execute()
            else:
                search_response = youtube.search().list(
                    type='video',
                    q=self.keyword,
                    #eventType='live',
                    publishedBefore=self.pub_before,
                    publishedAfter=self.pub_after,
                    part='snippet',
                    order='viewCount',
                    maxResults=50
                ).execute()

        self.all_ids = []
        self.list_ids = []
        self.list_titles = []
        self.list_stats = []
        self.total_results = 0

        self.ids = []
        titles = []
        stats = []
        count = 0
        nextPageToken = ''

        print('search_response: ',search_response)

        # Check that any videos were returned
        if 'nextPageToken' in search_response:
            if (len(search_response['items']) > 0):
                nextPageToken = search_response['nextPageToken']
            else:
                nextPageToken = 'done'
                #print('More Results...')
        else:
            nextPageToken = 'done'
            print('No next page')

        # Number of youtube results meeting criteria
        self.total_results = search_response['pageInfo']['totalResults']

        # Number of results my site will show (num_result_pages * maxResults)
        self.show_results = self.total_results * num_result_pages

        print('\nNumber of Results: ', search_response['pageInfo']['resultsPerPage'])
        print('Total Results: ', search_response['pageInfo']['totalResults'])
        print('Next Page Token: ', nextPageToken)

        # Populate youtube vid IDs
        for search_result in search_response.get('items', []):
            self.ids.append(search_result['id']['videoId'])
            self.list_ids.append(search_result['id']['videoId'])

        video_ids = ','.join(self.ids)

        self.all_ids = video_ids

        # Call the videos.list method to retrieve view details for each video.
        video_response = youtube.videos().list(
            id=video_ids,
            part='snippet, statistics'
        ).execute()

        for videos in video_response.get('items', []):
            titles.append(videos['snippet']['title'])
            self.list_titles.append(videos['snippet']['title'])
            stats.append(videos['statistics']['viewCount'])
            self.list_stats.append(videos['statistics']['viewCount'])

        #print('\nVideos:')
        #for x in range(len(titles)):
            #print(titles[x],stats[x],'https://www.youtube.com/watch?v='+self.ids[x])


        #print(title.encode('utf8'))

  #---------------------------------------------
  #---------------------------------------------

        while (nextPageToken != 'done' and count < num_result_pages):

            ids2 = []
            titles2 = []
            stats2 = []

            ids2.clear()
            titles2.clear()
            stats2.clear()

            count = count + 1

            #print('\n******* Next Page of Results *******')
            print('Next Page Token: ', nextPageToken)
            print('Page #: ',count)

            if self.source == 'index':
                if self.live_event:
                    search_response2 = youtube.search().list(
                        type='video',
                        q=self.keyword,
                        eventType='live',
                        location=self.lat_long,
                        locationRadius=self.radius,
                        #publishedBefore=options.pubBefore,
                        #publishedAfter=options.pubAfter,
                        pageToken=nextPageToken,
                        part='snippet',
                        order='viewCount',
                        maxResults=50
                    ).execute()
                else:
                    search_response2 = youtube.search().list(
                        part="snippet",
                        type="video",
                        q=self.keyword,
                        #eventType='live',
                        location=self.lat_long,
                        locationRadius=self.radius,
                        #publishedBefore=self.pub_before,
                        publishedAfter=self.pub_after,
                        pageToken=nextPageToken,
                        order="viewCount",
                        maxResults=50
                    ).execute()

            if self.source == 'index2' or self.source == 'index3':
                if self.live_event:
                    search_response2 = youtube.search().list(
                        type='video',
                        #q=self.keyword,
                        eventType='live',
                        #publishedBefore=options.pubBefore,
                        #publishedAfter=options.pubAfter,
                        pageToken=nextPageToken,
                        part='snippet',
                        order='viewCount',
                        maxResults=50
                    ).execute()
                else:
                    search_response2 = youtube.search().list(
                        type='video',
                        q=self.keyword,
                        #eventType='live',
                        #publishedBefore=self.pub_before,
                        publishedAfter=self.pub_after,
                        pageToken=nextPageToken,
                        part='snippet',
                        order='viewCount',
                        maxResults=50
                    ).execute()

            print('Num Items: ',len(search_response2['items']))
            nextPageToken = ''  #new-comment out

            if 'nextPageToken' in search_response2:  #change back to search_response???? DEBUG
                if (len(search_response2['items']) > 0):
                    nextPageToken = search_response2['nextPageToken']
                    #print('More Results...')
                    #print('\nVideos:\n')
                else:
                    nextPageToken = 'done'
                    print('No more Results...')
            else:
                nextPageToken = 'done'
                print('No more Results...')

            for search_result2 in search_response2.get('items', []):
                ids2.append(search_result2['id']['videoId'])
                self.list_ids.append(search_result2['id']['videoId'])

            video_ids2 = ','.join(ids2)

            #self.all_ids = self.all_ids + video_ids2

            # Call the videos.list method to retrieve location details for each video.
            video_response2 = youtube.videos().list(
                id=video_ids2,
                part='snippet, statistics'
            ).execute()

            for videos2 in video_response2.get('items', []):
                #titles2.append(videos2['snippet']['title'])
                self.list_titles.append(videos2['snippet']['title'])

                if 'viewCount' in videos2['statistics']:
                    #stats2.append(videos2['statistics']['viewCount'])
                    self.list_stats.append(videos2['statistics']['viewCount'])
                else:
                    #stats2.append('n/a')
                    self.list_stats.append('n/a')

            #for z in range(len(titles2)):
                #print(titles2[z],stats2[z],'https://www.youtube.com/watch?v='+ids2[z])

            search_response2.clear()

            #print('IDs: ',self.all_ids)

  #---------------------------------------------
  #---------------------------------------------


#if __name__ == '__main__':
  #parser = argparse.ArgumentParser()
  #parser.add_argument('--q', help='Search term', default='')
  #parser.add_argument('--location', help='Location', default='43.21771312896356,3.069356378086354')
  #parser.add_argument('--location-radius', help='Location radius', default='12000m')  #80km=50m  1.5km=1m
  #parser.add_argument('--pubAfter', help='Published after date', default='2018-10-15T18:06:28.187Z')  #2016-06-01T11:33:54.000Z
  #parser.add_argument('--pubBefore', help='Published before date', default='2018-10-01T20:00:00.000Z')  #YYYY-MM-DDThh:mm:ss.sZ
  #parser.add_argument('--event', help='Event type', default='live')    #completed,live,upcoming
  #parser.add_argument('--max-results', help='Max results', default=50)
  #parser.add_argument('--max-views', help='Max # of Views', default=2000)
  #args = parser.parse_args()

  #try:
    #youtube_search(args)
  #except HttpError as e:
    #print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))