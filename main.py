import requests
from bs4 import BeautifulSoup
from pprint import pprint
from ast import literal_eval
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

#https://www.youtube.com/watch?v=

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_viewcount(id):
    video_url = 'https://www.youtube.com/watch?v=' + id
    contents = requests.get(video_url).text
    soup = BeautifulSoup(contents, 'lxml')
    views = soup.select_one('meta[itemprop="interactionCount"][content]')['content']
    return views


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def update_video(youtube, vid_id, viewcount):
  # Call the API's videos.list method to retrieve the video resource.
    videos_list_response = youtube.videos().list(
        id=vid_id,
        part='snippet'
    ).execute()
    videos_list_snippet = videos_list_response['items'][0]['snippet']
    videos_list_snippet['title'] = 'This video has : ' + str(viewcount) + " views"
    videos_update_response = youtube.videos().update(
        part='snippet',
        body=dict(
        snippet=videos_list_snippet,
        id=vid_id
    )).execute()

if __name__ == "__main__":
    youtube = get_authenticated_service()
    video_id = input('Please enter video id : ')
    try:
        views = get_viewcount(video_id)
        update_video(youtube, video_id, views)
        print('Video title updated to : This video has : '+ str(views) + 'views')
    except Exception as e:
        print(e)
