from plexapi.server import *
baseurl = '' ## Your Plex URL. If at localhost you can use 'http://127.0.0.1:port/'
token = '' ## Your Plex Token. To find your token please follow this guide https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
plex = PlexServer(baseurl, token)
XXX = plex.library.section('') ## Enter Here your title of your library. For example 'XXXMedia' if your library is named XXXMedia
XXXScenes = XXX.all()
ActorsArray = []

for Scene in XXXScenes:
    if Scene.actors != []:
        for Actor in Scene.actors:
            Actor = (str(Actor)).split("<Role:")[1].replace(">","").replace("-"," ")
            if Actor not in ActorsArray:
                ActorsArray.append(Actor)
for Actor in ActorsArray:
    Playlist.create(plex,title = Actor, section='', smart=True, actor= Actor) ##<=========== HERE AT section='' change again to your title of your library

