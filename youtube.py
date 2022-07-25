from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def get_display_name(broadcaster_name: str) -> str:
    """Changes twitch username to display name"""
    if broadcaster_name.lower() == 'delordione':
        broadcaster_name = 'Delord'
    elif broadcaster_name.lower() == 'h2p_gucio':
        broadcaster_name = 'Gucio'
    elif broadcaster_name.lower() == 'rybsonlol_':
        broadcaster_name = 'Rybson'
    elif broadcaster_name.lower() == 'parisplatynov':
        broadcaster_name = 'Paris Platynov'
    elif broadcaster_name.lower() == 'randombrucetv':
        broadcaster_name = 'RandomBruce'
    elif broadcaster_name.lower() == 'sawardega':
        broadcaster_name = 'Wardęga'
    elif broadcaster_name.lower() == 'xayoo_':
        broadcaster_name = 'Xayoo'
    elif broadcaster_name.lower() == 'cinkrofwest':
        broadcaster_name = 'Cinkrof'
    elif broadcaster_name.lower() == 'bagietkayt':
        broadcaster_name = 'Bagietka'
    elif broadcaster_name.lower() == 'revo_toja':
        broadcaster_name = 'Revo'
    elif broadcaster_name.lower() == 'rafonixszef':
        broadcaster_name = 'Rafonix'
    elif broadcaster_name.lower() == 'majakstasko':
        broadcaster_name = 'Maja Staśko'

    return broadcaster_name


def upload_clips(clips: list):
    """Upload all downloaded clips"""
    for clip in clips:
        broadcaster_name = get_display_name(clip[0].broadcaster_name)

        request_body = {
            'snippet': {
                'categoryI': 22,
                'title': f"{broadcaster_name} - {clip[0].title}",
                'description': f"Daj suba po więcej\nhttps://twitch.tv/{clip[0].broadcaster_name}\n\n"
                               f"Pozdrawiam klubowiczów Harambe 7",
                'tags': ["twitch", "shoty", "delord", "franio", "arquel", "klub r", "harambe", broadcaster_name]
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            },
            'notifySubscribers': False
        }

        media_file = MediaFileUpload(clip[1])

        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        ).execute()
