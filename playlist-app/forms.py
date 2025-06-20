"""Forms for playlist app."""

from wtforms import SelectField, SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    # Add the necessary code to use this form
    name = StringField('Playlist Name', validators=[InputRequired(), Length(max=100)])
    description = StringField('Description', validators=[Length(max=200)])


class SongForm(FlaskForm):
    """Form for adding songs."""

    # Add the necessary code to use this form
    # Note: Quick Search for the longest song name in characters, results noted
    #  Hoagland Carmichael is the holder of the Guinness Book of Records longest
    #  song name at 30 words or 167 characters. 
    title = StringField('Title', validators=[InputRequired(), Length(max=175)])
    artist = StringField('Artist', validators=[InputRequired(), Length(max=100)])
    album = StringField('Album', validators=[Length(max=150)])



# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    # playList = SelectField('Choose Playlist', choices=[], coerce=int, validators=[InputRequired()])
    song = SelectField('Choose Song', choices=[], coerce=int,validators=[InputRequired()])
