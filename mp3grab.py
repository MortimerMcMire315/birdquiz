import subprocess
import os
import html
import json
import requests
from tempfile import mkstemp
from util import print_error, normalize, print_debug

class BirdNotFoundException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

def find_mp3_url(page, birdname):
    # The response is 'angular.callbacks_1(A BUNCH OF JSON DATA)', so by
    # removing the function call, we are left with only valid JSON.

    #remove everything before the left parenthesis
    json_dat = page.split('(',1)[1]
    #reverse and remove everything before the right parenthesis
    json_dat = json_dat[::-1].split(')', 1)[1]
    #reverse again, and we have valid json
    json_dat = json_dat[::-1]

    '''
    JSON Format:
    {
        "response": {
            --- etc. ---
            "docs" : [{
                "id" : "41"
                "title" : "Barred Owl"
                "thumbnail": "/guide/PHOTO/LARGE/barred_owl_glamor_ed_schneider.jpg",
                "permalink": "/guide/Barred_Owl",
                "profileSoundPath": "/guide/SOUND/SPECIES/315A.mp3",
                "score": 9.641996
            }, {
                --- etc. ---
            }]
        }
    }
    '''

    first_result = json.loads(json_dat)["response"]["docs"][0]
    audio_url = "https://www.allaboutbirds.org" + first_result["profileSoundPath"]
    web_birdname = first_result["title"]

    if normalize(birdname) != normalize(web_birdname):
        raise BirdNotFoundException("No results found for \"" + birdname +
                                    "\". Closest match is \"" + web_birdname
                                    + "\".")

    return audio_url

def play_mp3_from_birdname(birdname):
    url = "https://solr.allaboutbirds.net/solr/speciesGuide/select?defType=edismax&json.wrf=angular.callbacks._1&q=%s&rows=5&wt=json" % birdname
    r = requests.get(url)

    try:
        page = r.text
        if r.status_code != 200:
            raise IOError("Error: Web page could not be found.")
    except Exception as e:
        print(e)
        return(None)

    try:
        mp3_url = find_mp3_url(page,birdname)
    except BirdNotFoundException as e:
        print(e)
        return(None)
    except (json.decoder.JSONDecodeError,IndexError) as e:
        print_debug(e)
        return(None)

    (fd, tmpfile_abspath) = mkstemp(suffix=".mp3")
    remote_file = requests.get(mp3_url, stream=True)
    with open(tmpfile_abspath, 'wb') as local_file:
        for chunk in remote_file.iter_content(chunk_size=1024):
            if chunk:
                local_file.write(chunk)
        return play_mp3(tmpfile_abspath)

def play_mp3(mp3_path):
    print("Playing mp3 file...")
    with open(os.devnull, 'w') as hell:
        return (subprocess.Popen(['mpg123', '-q', mp3_path], stdout=hell, stderr=hell, stdin=hell), mp3_path)
