
import tekore as tk

def authorize():
     CLIENT_ID = "YOUR CLIENT ID"
     CLIENT_SECRET = "YOUR CLIENT SECRET ID"
     app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
     return tk.Spotify(app_token)
