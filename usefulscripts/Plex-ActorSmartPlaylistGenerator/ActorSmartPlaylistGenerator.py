from plexapi.server import PlexServer, Playlist

BASEURL = ''  # Your Plex URL. If at localhost you can use 'http://127.0.0.1:port/'
TOKEN = ''  # Your Plex Token. To find your token please follow this guide https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
LIBRARIES = []  # Enter Here your titles of yours libraries. For example ['XXXMedia', 'XXXMedia 2'] if you're libraries is named XXXMedia and XXXMedia 2


def create_playlists():
    plex = PlexServer(BASEURL, TOKEN)

    plex_scenes = {}
    plex_playlists = {}

    for library_name in LIBRARIES:
        plex_library = plex.library.section(library_name)
        plex_playlists[plex_library] = [playlist for playlist in plex.playlists() if playlist.smart and playlist.items() and playlist.items()[0].section() == plex_library]
        plex_scenes[plex_library] = plex_library.all()

    plex_actors = {}

    for library in plex_scenes:
        plex_actors[library] = []
        for scene in plex_scenes[library]:
            for actor in scene.actors:
                actor_name = actor.tag

                if actor_name and actor_name not in plex_actors[library]:
                    plex_actors[library].append(actor_name)

    for library in plex_scenes:
        playlist_titles = [playlist.title for playlist in plex_playlists[library]]
        for actor_name in plex_actors[library]:
            if actor_name not in playlist_titles:
                Playlist.create(plex, title=actor_name, section=library, smart=True, actor=actor_name)

if __name__ == '__main__':
    create_playlists()
