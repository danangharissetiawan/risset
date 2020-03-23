from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='user/profile', default='default.jpg', blank=True, null=True)
    alamat = models.CharField(max_length=250, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    follower = models.IntegerField(blank=True, null=True)



    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.foto.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.foto.path)


    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
