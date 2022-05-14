import sqlite3

def get_connection():
    connection = sqlite3.connect('songs.db')
    connection.row_factory = sqlite3.Row
    return connection


def get_songs():
    connection = get_connection()
    songs = connection.execute("select id, name, artist_id, album_id from songs").fetchall()
    connection.close()
    return songs

def get_song_by_id(id):
    connection = get_connection()
    song = connection.execute("""
        select songs.id, songs.name, songs.artist_id, songs.album_id, artists.name as artist_name from songs 
        inner join artists on artists.id = songs.artist_id
        where songs.id = ?
    """, (id,)).fetchone()
    connection.close()
    return song


def get_reactions():
    connection = get_connection()
    reactions = connection.execute("select id, content, rating, song_id from reactions").fetchall()
    connection.close()
    return reactions

def get_songs_with_reactions():
    connection = get_connection()
    songs = connection.execute("select id, name, artist_id, album_id from songs").fetchall()
    all_reactions = connection.execute("select id, content, rating, username, song_id from reactions").fetchall()
    all_artists = connection.execute("select id, name from artists").fetchall()
    all_albums = connection.execute("select id, name from albums").fetchall()
    connection.close()

    songs_with_reactions = []

    for song in songs:
        current_song_reactions = []

        for reaction in all_reactions:
            if reaction["song_id"] == song["id"]:
                current_song_reactions.append({
                    "rating": reaction["rating"],
                    "username": reaction["username"],
                    "content": reaction["content"],
                })

        if len(current_song_reactions) > 0:
            average_rating = sum(s["rating"] for s in current_song_reactions) / len(current_song_reactions)
        else:
            average_rating = None

        current_artist = next(artist 
                                for artist in all_artists 
                                if artist['id'] == song['artist_id'])

        current_album = next(album 
                                for album in all_albums 
                                if album['id'] == song['album_id'])
                                
        current_song_with_reactions = {
            'id': song['id'],
            'name': song['name'],
            'artist_id': song['artist_id'],
            'artist_name': current_artist['name'],
            'album_name': current_album['name'],
            'reactions': current_song_reactions,
            'average_rating': average_rating
        }

        songs_with_reactions.append(current_song_with_reactions)
    return songs_with_reactions

def create_review(username, score, review, song_id):
    connection = get_connection()
    connection.execute('insert into reactions (username, content, rating, song_id) values (?, ?, ?, ?);', (username, review, score, song_id))
    connection.commit()
    connection.close()