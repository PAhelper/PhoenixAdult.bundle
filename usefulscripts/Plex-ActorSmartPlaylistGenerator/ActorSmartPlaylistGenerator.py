from plexapi.server import PlexServer, Playlist

BASEURL = ''  # Your Plex URL. If at localhost you can use 'http://127.0.0.1:port/'
TOKEN = ''  # Your Plex Token. To find your token please follow this guide https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
LIBRARY = ''  # Enter Here your title of your library. For example 'XXXMedia' if your library is named XXXMedia


def create_playlist():
    plex = PlexServer(BASEURL, TOKEN)
    plex_library = plex.library.section(LIBRARY)
    plex_playlists = [playlist.title for playlist in plex.playlists()]
    scenes = plex_library.all()

    actors = []
    for scene in scenes:
        for actor in scene.actors:
            actor_name = actor.tag

            if actor_name and actor_name not in actors:
                actors.append(actor_name)

    for actor_name in actors:
        if actor_name not in plex_playlists:
            Playlist.create(plex, title=actor_name, section=LIBRARY, smart=True, actor=actor_name)

if __name__ == '__main__':
    create_playlist()
