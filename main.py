import userpaths
from datetime import timedelta, datetime
from pyrfc3339 import generate
import pytz
from twitch import *
from youtube import *

# create clips download path
downloads_folder = os.path.join(userpaths.get_downloads(), "clips")
if not os.path.isdir(downloads_folder):
    print('Creating download folder')
    os.mkdir(downloads_folder)

# how many clips to download
NUMBER_OF_TOP_CLIPS = 5

# format date to RFC3339
date_to_check = datetime.today() - timedelta(days=1)
date_to_check = generate(date_to_check.replace(tzinfo=pytz.utc))

all_clips = []

streamers = get_streamers_data('streamers.json')
best_clips = get_top_clips(streamers, date_to_check, NUMBER_OF_TOP_CLIPS)
downloaded_clips = download_clips(downloads_folder, best_clips)
#upload_clips(downloaded_clips)

delete_clips(downloads_folder)
