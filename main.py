import os,requests
import eyed3
import numpy as np

class MP3MetadataMaker:
    def __init__(self,path) -> None:
        self.files = None
        self.path = None
        if os.path.isdir(path):
            self.files = []
            extensions = [file.split(".")[-1] for file in os.listdir(path)]
            extensions_counts = {extensions.count(ext) : ext for ext in np.unique(extensions)}
            dominant_ext = extensions_counts.get(max(extensions_counts.keys()))
            for file in os.listdir(path):
                if file.endswith(dominant_ext):
                    print(f'load {path + "/" + file}')
                    audiofile = eyed3.load(path + "/" + file)
                    print(audiofile)
                    self.files.append((file.replace("_"," ").replace(f".{dominant_ext}",""),path + "/" + file,audiofile))
        else:
            self.path = path
            self.audiofile = eyed3.load(self.path)
        pass

    def set_api_key(self,api_key : str):
        self.api_key = api_key
        pass
        
    def process(self):
        if not self.api_key:
            raise KeyError("You need to specify an api key using set_api_key() !")
        url = "https://deezerdevs-deezer.p.rapidapi.com/search"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }
        song_id = None

        if self.path:
            querystring = {"q" : self.path.split("/")[-1].split(".")[0]}
            response = requests.get(url, headers=headers, params=querystring)
            json =  response.json().get("data")[0]

            song_id = json.get("id")
            artist = json.get("artist")
            album = json.get("album")
            self.audiofile.tag.artist = artist.get("name")
            self.audiofile.tag.album = album.get("title")
            self.audiofile.tag.title = json.get("title")
            url = f"https://deezerdevs-deezer.p.rapidapi.com/track/{song_id}"
            response = requests.get(url, headers=headers)
            json = response.json()
            self.audiofile.tag.track_num = json.get("track_position")
            self.audiofile.tag.release_date = json.get("release_date")
            self.audiofile.tag.save()
        else:
            for title,_,audiofile in self.files:
                print(f"searching for {title}")
                querystring = {"q" : title}
                url = "https://deezerdevs-deezer.p.rapidapi.com/search"
                response = requests.get(url, headers=headers, params=querystring)
                json =  response.json().get("data")[0]
                artist = json.get("artist")
                album = json.get("album")
                song_id = json.get("id")
                audiofile.tag.artist = artist.get("name")
                audiofile.tag.album = album.get("title")
                audiofile.tag.title = json.get("title")
                url = f"https://deezerdevs-deezer.p.rapidapi.com/track/{song_id}"
                response = requests.get(url, headers=headers)
                json = response.json()
                audiofile.tag.track_num = json.get("track_position")
                audiofile.tag.release_date = json.get("release_date")
                audiofile.tag.save()
