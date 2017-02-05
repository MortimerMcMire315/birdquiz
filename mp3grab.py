import certifi
import urllib.request
import subprocess
import os
from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
from util import print_error, normalize
import html

def find_mp3_url(page, birdname):
    soup = BeautifulSoup(page, 'html.parser')
    try:
        firstResult = soup.find(id="speciesResults").find_all('li')[0]
        audio_url = firstResult.find_all("audio")[0]["src"]
        web_birdname = firstResult.find_all("a", class_="pull-left")[0].contents[0]
    except (IndexError, KeyError):
        print_error("No results found for \"" + birdname + "\".")
        return None

    if normalize(birdname) != normalize(web_birdname):
        print_error("Error: No results found for \"" + birdname + "\". Closest match is \"" + web_birdname + "\".")
        return None

    return audio_url

def play_mp3_from_birdname(birdname, session):
    '''
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    response = http.request("GET","http://www.allaboutbirds.org/search/?q=" + birdname)
    '''

    esub = EntitySubstitution()
    escaped = esub.substitute_html(birdname)

    session.visit("http://www.allaboutbirds.org/search/?q=" + escaped)
    try:
        page = session.body()
    except:
        return None

    mp3_url = find_mp3_url(page,birdname)
    if mp3_url is None:
        return None

    (mp3_path, headers) = urllib.request.urlretrieve(mp3_url)
    return play_mp3(mp3_path)

def play_mp3(mp3_path):
    print("Playing mp3 file...")
    with open(os.devnull, 'w') as o:
        with open(os.devnull, 'w') as e:
            with open(os.devnull, 'w') as i:
                #return (subprocess.Popen(['mpg123', '-q', mp3_path], stdout=o, stderr=e, stdin=i), mp3_path)
                return (subprocess.Popen(['vlc',  mp3_path], stdout=o, stderr=e, stdin=i), mp3_path)
