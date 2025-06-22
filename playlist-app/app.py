from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


# --------------- #
# Playlist routes #
# --------------- #

@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    playlist = Playlist.query.get_or_404(playlist_id)

    return render_template("playlist.html", playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # CODE HERE FOR THIS ROUTE TO WORK
    
    #Get LOGIC
    form = PlaylistForm()

    # POST LOGIC
    if form.validate_on_submit():
        playlist = Playlist(name=form.name.data,
                    description=form.description.data)
        db.session.add(playlist)
        db.session.commit()
        flash(f"Added Playlist: {playlist.name} with a description of {playlist.description}")
        return redirect("/playlists")

    return render_template("new_playlist.html", form=form)


# ------------ #
# Song routes  #
# ------------ #

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    #Get LOGIC
    form = SongForm()

    # POST LOGIC
    if form.validate_on_submit():
        song = Song(title=form.title.data,
                    artist=form.artist.data,
                    album=form.album.data)
        db.session.add(song)
        db.session.commit()
        flash(f"Added song: {song.title} by {song.artist}")
        return redirect("/songs")

    return render_template("new_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])

def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    # Get the current playlist's songs
    curr_playlist_songs = [ps.song_id for ps in playlist.playlist_songs]
    # Get all songs in the database
    all_songs = Song.query.all()
    # Filter out songs that are already in the playlist with a list comprehension
    remaining_songs = [song for song in all_songs if song.id not in curr_playlist_songs]
    # Dynamically set choices for the song field in the form 
    form.song.choices = [(song.id, song.title) for song in remaining_songs]

    # POST LOGIC
    if form.validate_on_submit():

          # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
        song = Song.query.get(form.song.data)
        if not song:
            flash("Song not found.", "error")
            return redirect(f"/playlists/{playlist_id}/add-song")
            
        new_playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=song.id)
        db.session.add(new_playlist_song)
        db.session.commit()
        flash(f"Added song: {song.title} to playlist: {playlist.name}")
        # Redirect to the playlist detail page after adding the song
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
