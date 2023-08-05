# Copyright (C) 2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from __future__ import annotations

import enum
from typing import List

from django.db import models


class RequestStatus(enum.Enum):
    """Request statuses.

    Values are used in the ui.

    """

    PENDING = "Pending"
    WAITING_FOR_FEEDBACK = "Waiting for feedback"
    FEEDBACK_TO_HANDLE = "Feedback to handle"
    ACCEPTED = "Accepted"
    SCHEDULED = "Scheduled"
    FIRST_LISTING_DONE = "First listing done"
    FIRST_ORIGIN_LOADED = "First origin loaded"
    REJECTED = "Rejected"
    SUSPENDED = "Suspended"
    DENIED = "Denied"

    @classmethod
    def choices(cls):
        return tuple((variant.name, variant.value) for variant in cls)

    def allowed_next_statuses(self) -> List[RequestStatus]:
        next_statuses = {
            self.PENDING: [self.WAITING_FOR_FEEDBACK, self.REJECTED, self.SUSPENDED],
            self.WAITING_FOR_FEEDBACK: [self.FEEDBACK_TO_HANDLE],
            self.FEEDBACK_TO_HANDLE: [
                self.WAITING_FOR_FEEDBACK,
                self.ACCEPTED,
                self.REJECTED,
                self.SUSPENDED,
            ],
            self.ACCEPTED: [self.SCHEDULED],
            self.SCHEDULED: [
                self.FIRST_LISTING_DONE,
                # in case of race condition between lister and loader:
                self.FIRST_ORIGIN_LOADED,
            ],
            self.FIRST_LISTING_DONE: [self.FIRST_ORIGIN_LOADED],
            self.FIRST_ORIGIN_LOADED: [],
            self.REJECTED: [],
            self.SUSPENDED: [self.PENDING],
            self.DENIED: [],
        }
        return next_statuses[self]  # type: ignore


class RequestActorRole(enum.Enum):
    MODERATOR = "moderator"
    SUBMITTER = "submitter"
    FORGE_ADMIN = "forge admin"

    @classmethod
    def choices(cls):
        return tuple((variant.name, variant.value) for variant in cls)


class RequestHistory(models.Model):
    """Comment or status change. This is commented or changed by either submitter or
    moderator.

    """

    request = models.ForeignKey("Request", models.DO_NOTHING)
    text = models.TextField()
    actor = models.TextField()
    actor_role = models.TextField(choices=RequestActorRole.choices())
    date = models.DateTimeField(auto_now_add=True)
    new_status = models.TextField(choices=RequestStatus.choices(), null=True)


class Request(models.Model):
    status = models.TextField(
        choices=RequestStatus.choices(), default=RequestStatus.PENDING.name,
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    submitter_name = models.TextField()
    submitter_email = models.TextField()
    # FIXME: shall we do create a user model inside the webapp instead?
    forge_type = models.TextField()
    forge_url = models.TextField()
    forge_contact_email = models.EmailField()
    forge_contact_name = models.TextField()
    forge_contact_comment = models.TextField(
        help_text="Where did you find this contact information (url, ...)",
    )
