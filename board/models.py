from django.db import models
from django.db.models import Q


class Board(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class Thread(models.Model):
    is_closed = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now=True)
    # board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def open_post(self):
        return self.post_set.last()

    def last_post_in_each_thread(self):
        return self.post_set.first()

    def last_posts(self):
        res = self.post_set.filter(Q(op=True) | Q(id__in=[a.id for a in self.post_set.all()[:3]]))
        return res[::-1]

    def delete_thread(self):
        self.post_set.all().delete()
        self.delete()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-published"]


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    text = models.TextField()
    name = models.CharField(default='Аноним', max_length=30)
    email = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images')
    op = models.BooleanField(default=False)
    bump = models.BooleanField(default=True)
    published = models.DateTimeField(auto_now=True)
    board = models.ManyToManyField(Board)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return '%s %s' % (self.title, self.thread)
