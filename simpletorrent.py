# -*- coding: utf-8 -*-

#@markdown <h4>⬅️ Click here to START server</h4>
#@markdown <br><center><img src='https://i.imgur.com/DOoxSuO.png' height="50" alt="netdata"/></center>
#@markdown <center><h3>SimpleTorrent is a a self-hosted remote torrent client.</h3></center><br>

import os
import time
import pathlib 
import urllib.request
from IPython.display import clear_output

# script version
Version = '1.0'

#####################################
USE_FREE_TOKEN = False 
TOKEN = ""
HOME = os.path.expanduser("~")

if not os.path.exists(f"{HOME}/.ipython/ttmg.py"):
    hCode = "https://raw.githubusercontent.com/imgload/" \
                "simple-torrent/master/res/ttmg.py"
    urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ttmg.py")

from ttmg import (
    runSh,
    findProcess,
    loadingAn,
    updateCheck,
    ngrok
)
# making enviroment for simple-torrent
pathlib.Path('downloads').mkdir(mode=0o777, exist_ok=True)
pathlib.Path('torrents').mkdir(mode=0o777, exist_ok=True)
  
configPath = pathlib.Path('cloud-torrent.json')
configsdata = r"""
{{
  "AutoStart": true,
  "EngineDebug": false,
  "MuteEngineLog": true,
  "ObfsPreferred": true,
  "ObfsRequirePreferred": false,
  "DisableTrackers": false,
  "DisableIPv6": false,
  "DownloadDirectory": "downloads/",
  "WatchDirectory": "torrents/",
  "EnableUpload": true,
  "EnableSeeding": false,
  "IncomingPort": 50007,
  "DoneCmd": "{}/doneCMD.sh",
  "SeedRatio": 1.5,
  "UploadRate": "High",
  "DownloadRate": "Unlimited",
  "TrackerListURL": "https://trackerslist.com/best.txt",
  "AlwaysAddTrackers": true,
  "ProxyURL": ""
}}
""".format(HOME)
with open(configPath, "w+") as configFile:
  configFile.write(configsdata)
#####################################

if updateCheck("Checking updates ...", Version):  # VERSION CHECKING ...
    !kill -9 -1 &
clear_output()

# Simple Torrent installing ...
loadingAn()
if os.path.isfile("/usr/local/bin/cloud-torrent") is False:
  dcmd = "wget -qq https://raw.githubusercontent.com/imgload/" \
          "simple-torrent/master/res/scripts/" \
          "simpleCloudInstaller.sh -O ./simpleCloudInstaller.sh"
  runSh(dcmd)
  runSh('bash ./simpleCloudInstaller.sh')
  runSh('rm -rf ./simpleCloudInstaller.sh')

#Opening cloud-torrent in background
if not findProcess("cloud-torrent", "cloud-torrent"):
  PORT = 4444
  try:
    urllib.request.urlopen(f"http://localhost:{PORT}")
  except:
    cmdC = f'cloud-torrent --port {PORT} ' \
        '-t "SimpleTorrent" ' \
        '-c cloud-torrent.json ' \
        '--host 0.0.0.0 --disable-log-time ' \
        '&'
    for run in range(10):    
      runSh(cmdC, shell=True)
      time.sleep(3)
      try:
        urllib.request.urlopen(f"http://localhost:{PORT}")
        break
      except:
        print("Error: Simple-Torrent not starting. Retrying ...")

# START_SERVER
clear_output()
Server = ngrok(
    TOKEN, USE_FREE_TOKEN, [['simple-torrent', 4444, 'http'], 
    ['peerflix-server', 4445, 'http']], 'us', 
    [f"{HOME}/.ngrok2/ngrok01.yml", 4040]
).start('simple-torrent')