from django.db import models
from django.contrib.auth.models import User
from uuslug import uuslug
from django.core.urlresolvers import reverse
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts_created')
    name = models.CharField(max_length=200, verbose_name='歌名')
    slug = models.CharField(max_length=500, blank=True)
    description = models.TextField(verbose_name='描述')
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    # 音乐风格
    MUSIC_GENRE_CHOICES = (
        ('classic', '经典'),
        ('country', '乡村'),
        ('electronic', '电子音乐'),
        ('folk', '民族'),
        ('blues', '蓝调'),
        ('jazz', '爵士'),
        ('pop', '流行'),
        ('r_and_b','R&B'),
        ('rock', '摇滚'),
        ('other', '其他'),
    )
    genre = models.CharField(max_length=200, choices=MUSIC_GENRE_CHOICES, default='pop', verbose_name='风格')
    audio_file = models.FileField(upload_to='audios/%Y/%m/%d', verbose_name='音乐文件')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dkmusic:detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(User, related_name='comments_created')
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(verbose_name='评论')
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} commented by {}'.format(self.post, self.user)
