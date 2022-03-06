import os.path
import re
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
# from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape, mark_safe


class OppostManager(models.Manager):
    def get_queryset(self):
        return super(OppostManager, self).get_queryset().filter(is_oppost=True)


class Post(models.Model):
    BOARD_SLUG = ''
    allowed_img_extensions = ['jpg', 'jpeg', 'gif', 'png']
    allowed_vid_extensions = ['mp4', 'webm']
    oppost = models.ForeignKey("self", on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250, blank=True, null=True)
    file = models.FileField(upload_to='src',
                            validators=[FileExtensionValidator(
                                allowed_extensions=allowed_img_extensions+allowed_vid_extensions)],
                            blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumb', blank=True, null=True)
    body = models.TextField(max_length=15000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_oppost = models.BooleanField(default=False)

    objects = models.Manager()
    oppost_manager = OppostManager()

    class Meta:
        abstract = True

    def is_file_img(self):

        if self.file:
            return self.file.name.lower().split('.')[-1] in self.allowed_img_extensions
        else:
            return False

    def get_file_name(self):
        return self.file.name.split('/')[-1]

    def get_file_size(self):
        return str(self.file.size // 1024) + 'Kb'

    def get_absolute_url(self):
        return reverse('board:thread_detail', kwargs={'board_slug': self.BOARD_SLUG, 'id': self.id})

    def format_post_body(self):

        self.body = escape(self.body)

        match = re.findall(r"\B`.+`\B", self.body, flags=re.DOTALL)

        if match:
            for i in match:
                self.body = self.body.replace(i, '<pre>{}</pre>'.format(i[1:-1:]))

        match = re.findall(r"(?<!&gt;)&gt;(?!&gt;).+", self.body)

        if match:
            for i in match:
                self.body = self.body.replace(i, '<div class="quote_text">{}</div>'.format(i))

        match = re.findall(r"&gt;&gt;\d+", self.body)

        if match:
            for i in match:

                post_id = i[8:]
                try:
                    linked_post = self.__class__.objects.get(id=post_id)
                except ObjectDoesNotExist:
                    continue

                if linked_post.is_oppost:
                    self.body = self.body.replace(i, f'<a href="/{self.BOARD_SLUG}/{post_id}">{i}</a>')
                else:
                    self.body = self.body.replace(i,
                                                  f'<a href="/{self.BOARD_SLUG}/{linked_post.oppost.id}#'
                                                  f'{post_id}" onclick="highlight({post_id})">{i}</a>')

        match = re.findall(r"\B\*\*[^\*{2}]+\*\*\B|\b__[^_{2}]+__\b", self.body)

        if match:
            for i in match:
                self.body = self.body.replace(i, '<b>{}</b>'.format(i[2:-2:]))

        match = re.findall(r"\B\*[^\*]+\*\B|\b_[^_]+_\b", self.body)

        if match:
            for i in match:
                self.body = self.body.replace(i, '<i>{}</i>'.format(i[1:-1:]))

        match = re.findall(r"(\bhttps?://|\bftp://|\bmailto:)[^\s]+", self.body)

        if match:
            for i in match:
                self.body = self.body.replace(i, '<a href="{}">{}</a>'.format(i, i))

    def create_vid_thumbnail(self):

        def resize_image(image, size=(150, 150)):

            h, w = image.shape[:2]
            c = image.shape[2] if len(image.shape) > 2 else 1

            if h == w:
                return cv2.resize(image, size, cv2.INTER_AREA)

            dif = h if h > w else w

            interpolation = cv2.INTER_AREA if dif > (size[0] + size[1]) // 2 else cv2.INTER_CUBIC

            x_pos = (dif - w) // 2
            y_pos = (dif - h) // 2

            if len(image.shape) == 2:
               mask = np.zeros((dif, dif), dtype=image.dtype)
               mask[y_pos:y_pos + h, x_pos:x_pos + w] = image[:h, :w]
            else:
               mask = np.zeros((dif, dif, c), dtype=image.dtype)
               mask[y_pos:y_pos + h, x_pos:x_pos + w, :] = image[:h, :w, :]

            return cv2.resize(mask, size, interpolation)

        vidcap = cv2.VideoCapture(self.file.path)
        file_name, _ = os.path.splitext(self.get_file_name())
        vidcap.set(1, 1.0)
        success, image = vidcap.read()
        image = resize_image(image)
        is_success, buffer = cv2.imencode(".jpg", image)
        io_buf = BytesIO(buffer)
        self.thumbnail.save(file_name + '.jpg', ContentFile(io_buf.read()), save=True)
        io_buf.close()
        return True

    def create_img_thumbnail(self):

        if not self.file:
            return

        THUMBNAIL_SIZE = (150, 150)

        image = Image.open(self.file)

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.file.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def save(self, *args, **kwargs):

        if not self.id:
            self.format_post_body()
            if self.is_file_img():
                self.create_img_thumbnail()


        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostA(Post):
    BOARD_SLUG = 'a'


class PostB(Post):
    BOARD_SLUG = 'b'
