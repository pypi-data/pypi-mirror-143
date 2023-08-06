# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import csv
from io import BytesIO

import charset_normalizer
from flask import current_app
from flask import json
from flask import send_file
from PIL import Image

from .files import open_file
from kadi.lib.archives import get_archive_contents
from kadi.lib.utils import flatten_list
from kadi.lib.web import url_for
from kadi.plugins import run_hook


def preview_file(file):
    """Send a file to a client for previewing in a browser.

    Note that this can potentially pose a security risk, so this should only be used for
    files that are safe for displaying. Uses the content-based MIME type of the file to
    set the content type of the response (see :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to send to the client.
    :return: The response object or ``None`` if the given file could not be found or has
        an incompatible storage type.
    """
    storage = file.storage
    filepath = storage.create_filepath(str(file.id))

    if filepath is None or not storage.exists(filepath):
        return None

    # See ".files.download_file" for why we use a file path here.
    return send_file(
        filepath,
        mimetype=file.magic_mimetype,
        download_name=file.name,
        etag=False,
        conditional=current_app.env == "development",
    )


def _get_encoding(file):
    encoding = None

    with open_file(file, mode="rb") as f:
        if f is None:
            return None

        # Limit the amount of bytes to use for the encoding detection.
        result = charset_normalizer.detect(f.read(16384))

        if result["encoding"] is not None:
            # Fall back to UTF-8 if the confidence is not high enough.
            encoding = result["encoding"] if result["confidence"] > 0.5 else "utf-8"

    if encoding is not None:
        try:
            # If an encoding was found, we try to actually read something from the file
            # using that encoding.
            with open_file(file, mode="r", encoding=encoding) as f:
                f.read(1)
        except:
            return None

    return encoding


def _get_csv_preview(file, encoding):
    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            if f is None:
                return None

            data = f.read(16384)

        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(data)
        has_header = sniffer.has_header(data)

        rows = []
        for row in csv.reader(data.splitlines(), dialect=dialect):
            # Ignore completely empty rows.
            if len(row) > 0:
                rows.append(row)

            if len(rows) >= 50:
                break

        return {"rows": rows, "encoding": encoding, "has_header": has_header}

    except:
        pass

    return None


def _get_image_thumbnail(file):
    image_data = BytesIO()

    with open_file(file) as f:
        if f is None:
            return None

        try:
            with Image.open(f) as image:
                # Special handling to support 16 bit TIFF images.
                if image.format == "TIFF" and image.mode == "I;16":
                    image = image.point(lambda i: i * (1 / 256)).convert("L")

                image.thumbnail((1024, 1024))
                image.save(image_data, format="PNG")

            image_data = base64.b64encode(image_data.getvalue()).decode()
        except:
            return None

    return f"data:image/png;base64,{image_data}"


def _get_text_preview(file, encoding):
    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            if f is None:
                return None

            data = f.read(16384)
            return {"lines": data.splitlines(), "encoding": encoding}
    except:
        pass

    return None


def get_builtin_preview_data(file):
    """Get the preview data of a file based on all built-in preview types.

    :param file: The :class:`.File` to get the preview data of.
    :return: The preview type and preview data as tuple or `None`` if none of the
        built-in preview types are suitable.
    """
    if file.magic_mimetype in [
        "application/gzip",
        "application/x-bzip2",
        "application/x-tar",
        "application/zip",
    ]:
        filepath = file.storage.create_filepath(str(file.id))

        if filepath is not None:
            return "archive", get_archive_contents(filepath, file.magic_mimetype)

    if file.magic_mimetype in [
        "audio/flac",
        "audio/mpeg",
        "audio/ogg",
        "audio/wav",
        "audio/x-wav",
    ]:
        return "audio", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    # Allow all text-based mimetypes as base.
    if file.magic_mimetype.startswith("text/") and file.mimetype == "text/csv":
        encoding = _get_encoding(file)

        if encoding is not None:
            preview_data = _get_csv_preview(file, encoding)

            if preview_data is not None:
                return "csv", preview_data

    # Images that can be previewed directly.
    if file.magic_mimetype in current_app.config["IMAGE_MIMETYPES"]:
        return "image", url_for(
            "api.preview_file", record_id=file.record_id, file_id=file.id
        )

    # Images that need to be converted before previewing them.
    if file.magic_mimetype in [
        "image/bmp",
        "image/gif",
        "image/tiff",
        "image/x-bmp",
        "image/x-ms-bmp",
    ]:
        thumbnail = _get_image_thumbnail(file)

        if thumbnail is not None:
            return "image", thumbnail

    # Allow all text-based MIME types as base.
    if file.magic_mimetype.startswith("text/") and file.mimetype == "text/markdown":
        encoding = _get_encoding(file)

        if encoding is not None:
            preview_data = _get_text_preview(file, encoding)

            if preview_data is not None:
                return "markdown", preview_data

    if file.magic_mimetype == "application/pdf":
        return "pdf", url_for(
            "api.preview_file", record_id=file.record_id, file_id=file.id
        )

    if file.magic_mimetype in [
        "text/plain",
        "application/octet-stream",
    ] and file.mimetype in [
        "application/sla",
        "model/stl",
        "model/x.stl-ascii",
        "model/x.stl-binary",
    ]:
        return "stl", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    if file.magic_mimetype == "video/mp4":
        return "video", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    if file.magic_mimetype == "application/x-flow+json":
        return "workflow", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    return None


def get_preview_data(file, use_fallback=True):
    """Get the preview data of a file.

    Uses the ``"kadi_get_preview_data"`` plugin hook for custom preview data.

    :param file: The :class:`.File` to get the preview data of.
    :param use_fallback: (optional) Flag indicating whether the file should be checked
        for textual data as fallback by trying to detect its encoding.
    :return: The preview type and preview data as tuple, which are always guaranteed to
        be JSON serializable. If either the preview type or data could not be
        determined, ``None`` is returned.
    """
    try:
        preview_data = run_hook("kadi_get_preview_data", file=file)
    except Exception as e:
        current_app.logger.exception(e)
        return None

    if preview_data is not None:
        if (
            not isinstance(preview_data, tuple)
            or not len(preview_data) == 2
            or None in preview_data
        ):
            current_app.logger.error(f"Invalid preview data format for {file!r}.")
            return None

        try:
            json.dumps(preview_data)
        except Exception as e:
            current_app.logger.exception(e)
            return None

    if preview_data is None and use_fallback:
        encoding = _get_encoding(file)

        if encoding is not None:
            preview_data = _get_text_preview(file, encoding)

            if preview_data is not None:
                return "text", preview_data

    return preview_data


def get_preview_scripts():
    """Get all custom scripts for rendering preview data of a file.

    Uses the ``"kadi_get_preview_scripts"`` plugin hook to collect the scripts.

    :return: A flattened list of all preview scripts or an empty list if something went
        wrong while collecting the scripts.
    """
    try:
        preview_scripts = run_hook("kadi_get_preview_scripts")
    except Exception as e:
        current_app.logger.exception(e)
        return []

    return flatten_list(preview_scripts)
