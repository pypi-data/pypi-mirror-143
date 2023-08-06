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
from flask import current_app
from flask_babel import gettext as _
from flask_login import current_user

from kadi.ext.db import db
from kadi.lib.api.core import json_error_response
from kadi.lib.format import filesize
from kadi.modules.records.models import File
from kadi.modules.records.models import Upload
from kadi.modules.records.schemas import FileSchema


def check_max_upload_size(size):
    """Check the maximum configured size of a single upload.

    Uses the value ``MAX_UPLOAD_SIZE`` in the application's configuration.

    :param size: The size of an upload to check.
    :return: An error response or ``None`` if the size is not exceeded.
    """
    max_size = current_app.config["MAX_UPLOAD_SIZE"]

    if max_size is not None and size > max_size:
        return json_error_response(
            413,
            description=_(
                "Maximum upload size exceeded (%(filesize)s).",
                filesize=filesize(max_size),
            ),
        )

    return None


def check_upload_user_quota(user=None, additional_size=0):
    """Check the maximum configured size of a user's upload quota.

    Uses the value ``MAX_UPLOAD_USER_QUOTA`` in the application's configuration.

    :param user: (optional) The user to check the quota of. Defaults to the current
        user.
    :param additional_size: (optional) Additional size to add to or subtract from the
        user's total.
    :return: An error response or ``None`` if the size is not exceeded.
    """
    user = user if user is not None else current_user

    max_quota = current_app.config["MAX_UPLOAD_USER_QUOTA"]

    if max_quota is not None:
        total_file_size = (
            user.files.filter(File.state == "active", File.storage_type == "local")
            .with_entities(db.func.sum(File.size))
            .scalar()
        )

        # Processing uploads are taken into account as well, even if there is the
        # possibility that they might not actually finish.
        total_upload_size = (
            user.uploads.filter(Upload.state == "processing")
            .with_entities(db.func.sum(Upload.size))
            .scalar()
        )

        total_size = (total_file_size or 0) + (total_upload_size or 0)

        if (total_size + additional_size) > max_quota:
            return json_error_response(
                413,
                description=_(
                    "Maximum upload quota exceeded (%(filesize)s).",
                    filesize=filesize(max_quota),
                ),
            )

    return None


def check_file_exists(record, name):
    """Check if a file with the given name already exists in the given record.

    :param record: The record in which to search for the file name.
    :param name: The name of the file to check.
    :return: An error response or ``None`` if the name does not exists.
    """
    file = record.active_files.filter(File.name == name).first()

    if file is not None:
        return json_error_response(
            409,
            description=_("A file with that name already exists."),
            file=FileSchema().dump(file),
        )

    return None


def check_storage_compatibility(current_storage, new_storage):
    """Check if two storages are compatible.

    :param current_storage: The current storage a file is stored in.
    :param new_storage: The new storage a file should be stored in.
    :return: An error response or ``None`` if the two storages are compatible.
    """
    if not current_storage.storage_type == new_storage.storage_type:
        return json_error_response(
            400,
            description=(
                _(
                    "Replacing a file stored in a different storage is currently not"
                    " supported, please delete the file first."
                )
            ),
        )

    return None
