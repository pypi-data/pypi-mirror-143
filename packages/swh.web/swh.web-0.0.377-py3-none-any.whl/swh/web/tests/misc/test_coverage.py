# Copyright (C) 2021-2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from datetime import datetime, timezone
from itertools import chain
import os
from random import randint
import uuid

from django.conf import settings
from django.utils.html import escape

from swh.scheduler.model import LastVisitStatus, ListedOrigin, OriginVisitStats
from swh.web.common.utils import reverse
from swh.web.config import SWH_WEB_SERVER_NAME
from swh.web.misc.coverage import deposited_origins, legacy_origins, listed_origins
from swh.web.tests.django_asserts import assert_contains
from swh.web.tests.utils import check_html_get_response, check_http_get_response


def test_coverage_view_no_metrics(client, swh_scheduler):
    """
    Check coverage view can be rendered when scheduler metrics and deposits
    data are not available.
    """
    url = reverse("swh-coverage")
    check_html_get_response(
        client, url, status_code=200, template_used="misc/coverage.html"
    )


def test_coverage_view_with_metrics(client, swh_scheduler, mocker):
    """
    Generate some sample scheduler metrics and some sample deposits
    that will be consumed by the archive coverage view, then check
    the HTML page gets rendered without errors.
    """

    # mock calls to get nixguix origin counts
    mock_archive = mocker.patch("swh.web.misc.coverage.archive")
    mock_archive.lookup_latest_origin_snapshot.return_value = {"id": "some-snapshot"}
    mock_archive.lookup_snapshot_sizes.return_value = {"release": 30095}

    listers = []
    visit_types = ["git", "hg", "svn", "bzr", "svn"]
    for origins in listed_origins["origins"]:
        # create some instances for each lister
        for instance in range(randint(1, 5)):
            lister = swh_scheduler.get_or_create_lister(
                origins["type"], f"instance-{instance}"
            )
            listers.append(lister)
            # record some sample listed origins
            _origins = []
            origin_visit_stats = []
            for i, visit_type in enumerate(visit_types):
                url = str(uuid.uuid4())
                _origins.append(
                    ListedOrigin(
                        lister_id=lister.id,
                        url=url,
                        visit_type=visit_type,
                        extra_loader_arguments={},
                    )
                )
                # set origin visit stats to some origins
                if i % 2 == 0:
                    now = datetime.now(tz=timezone.utc)
                    origin_visit_stats.append(
                        OriginVisitStats(
                            url=url,
                            visit_type=visit_type,
                            last_successful=now,
                            last_visit=now,
                            last_visit_status=LastVisitStatus.successful,
                            last_snapshot=os.urandom(20),
                        )
                    )
            # send origins data to scheduler
            swh_scheduler.record_listed_origins(_origins)
            swh_scheduler.origin_visit_stats_upsert(origin_visit_stats)

    # compute scheduler metrics
    swh_scheduler.update_metrics()

    # add some sample deposits
    deposits = []
    for origins in deposited_origins["origins"]:
        for _ in range(randint(2, 10)):
            deposits.append(
                {
                    "origin_url": f"https://{origins['search_pattern']}/{uuid.uuid4()}",
                    "status": "done",
                }
            )
    get_deposits_list = mocker.patch("swh.web.misc.coverage.get_deposits_list")
    get_deposits_list.return_value = deposits

    # check view gets rendered without errors
    url = reverse("swh-coverage")
    resp = check_html_get_response(
        client, url, status_code=200, template_used="misc/coverage.html"
    )

    # check logos and origins search links are present in the rendered page
    for origins in chain(
        listed_origins["origins"],
        legacy_origins["origins"],
        deposited_origins["origins"],
    ):
        logo_url = f'{settings.STATIC_URL}img/logos/{origins["type"].lower()}.png'
        assert_contains(resp, f'src="{logo_url}"')

        if "instances" in origins:
            for visit_types_ in origins["instances"].values():
                for data in visit_types_.values():
                    if data["count"]:
                        assert_contains(resp, f'<a href="{escape(data["search_url"])}"')
        else:
            for search_url in origins["search_urls"].values():
                assert_contains(resp, f'<a href="{escape(search_url)}"')

    for visit_type in visit_types:
        assert_contains(resp, f"<td>{visit_type}</td>")

    # check request as in production with cache enabled
    check_http_get_response(
        client, url, status_code=200, server_name=SWH_WEB_SERVER_NAME
    )
