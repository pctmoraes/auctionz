import io
import mimetypes
import os
import re
import uuid

import falcon
import msgpack

DIR_PATH = '/fareka/images/'


class Collection:

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp):
        image_files = [f for f in os.listdir(
            self._image_store._storage_path
        ) if f.endswith('.png')]

        images = [{'href': self._image_store._storage_path + f'/{image}'} for image in image_files]

        doc = {'images': images}


        resp.data = msgpack.packb(doc, use_bin_type=True)
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        name = self._image_store.save(req.stream, req.content_type)
        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name


class Item:

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, name):
        resp.content_type = mimetypes.guess_type(name)[0]

        print('\nname', name)
        print('\nself._image_store', self._image_store)

        try:
            resp.stream, resp.content_length = self._image_store.open(name)
        except IOError:
            raise falcon.HTTPNotFound()


class ImageStore:

    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(r'.+\.[a-z]{2,4}$')

    def __init__(
        self,
        storage_path,
        uuidgen=uuid.uuid4,
        fopen=io.open
    ):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, image_stream, image_content_type):
        ext = mimetypes.guess_extension(image_content_type)
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        image_path = os.path.join(self._storage_path, name)

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name

    def open(self, name):
        if not self._IMAGE_NAME_PATTERN.match(name):
            raise IOError('File not found')

        image_path = os.path.join(self._storage_path, name)
        stream = self._fopen(image_path, 'rb')
        content_length = os.path.getsize(image_path)

        return stream, content_length