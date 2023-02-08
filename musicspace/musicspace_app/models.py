from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from typing import Optional, Any
import uuid

from django.contrib.auth.models import AbstractUser

class MusicspaceUser(AbstractUser):

    def __str__(self):
        return self.username

    @property
    def provider(self) -> Optional[Any]:
        try:
            return self.provider_opt
        except:
            return None

class Address(models.Model):
    street_1 = models.CharField(
        max_length=128
    )

    street_2 = models.CharField(
        max_length=128,
        blank=True
    )

    city = models.CharField(
        max_length=128
    )

    state = models.CharField(
        max_length=64
    )

    zip = models.CharField(
        max_length=16
    )

    @property
    def short(self) -> str:
        return f'{self.city}, {self.state}'

    @property
    def full(self) -> str:
        lines = []
        lines.append(self.street_1)
        if self.street_2:
            lines.append(self.street_2)
        lines.append(f'{self.city}, {self.state} {self.zip}')

        return '\n'.join(lines)

class Genre(models.Model):
    id = models.CharField(
        max_length=32,
        primary_key=True
    )

    display_text = models.CharField(
        max_length=64
    )

    def __str__(self):
        return self.display_text
        
class Instrument(models.Model):
    id = models.CharField(
        max_length=32,
        primary_key=True
    )

    display_text = models.CharField(
        max_length=64
    )
    
    def __str__(self):
        return self.display_text

class Provider(models.Model):

    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        NONBINARY = 'nonbinary', _('Nonbinary')
        OTHER = 'other', _('Other')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        MusicspaceUser, 
        related_name='provider_opt',
        on_delete=models.PROTECT
    )

    title = models.CharField(
        max_length=256,
        blank=True,
        default=''
    )

    text = models.TextField(
        blank=True,
        default=''
    )

    gender = models.CharField(
        max_length=16,
        choices=Gender.choices
    )

    location = models.OneToOneField(
        Address, 
        related_name='provider',
        on_delete=models.PROTECT
    )

    image_url = models.CharField(
        max_length=256,
        blank=True,
        default=''
    )

    genres = models.ManyToManyField(Genre)

    instruments = models.ManyToManyField(Instrument)

    in_person = models.BooleanField()
    online = models.BooleanField()

    @property
    def full_name(self) -> str:
        return self.user.get_full_name()

    @property
    def truncated_text(self) -> str:
        if len(self.text) > 100:
            return self.text[:100] + '...' 
        else:
            return self.text

    ## returns Optional[TakeOneUser]
    @property
    def takeone_user(self):
        try:
            return self.takeone_user_opt
        except ObjectDoesNotExist:
            return None

class TakeOneUser(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    provider = models.OneToOneField(
        Provider, 
        related_name='takeone_user_opt',
        on_delete=models.PROTECT
    )

    takeone_id = models.CharField(
        max_length=64,
        editable=False
    )

    active = models.BooleanField(default=True)

    created_date_time = models.DateTimeField(auto_now_add=True)
    modified_date_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date_time']

class TakeOneProject(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=64,
        editable=False
    )

    takeone_user = models.ForeignKey(
        TakeOneUser, 
        related_name='projects',
        on_delete=models.PROTECT
    )

    status = models.CharField(
        max_length=64
    )

    published = models.BooleanField(default=False)
    show_video = models.BooleanField(default=False)

    created_date_time = models.DateTimeField(auto_now_add=True)
    modified_date_time = models.DateTimeField(auto_now=True)

    @property
    def should_render_video(self) -> bool:
        return self.status == 'completed' and \
            self.published and self.show_video

    class Meta:
        ordering = ['created_date_time']