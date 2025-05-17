from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name
    

class Album(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    image = models.ImageField(upload_to='albums/')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return self.name
    
class Song(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    text = models.TextField()
    story = models.TextField()
    genre = models.CharField(max_length=50)
    date = models.DateField()
    time = models.CharField(max_length=10)
    link = models.URLField()
    liked = models.ManyToManyField(User, related_name='liked_songs', blank=True)
    
    def __str__(self):
        return self.title
 
class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.song.name}"
    