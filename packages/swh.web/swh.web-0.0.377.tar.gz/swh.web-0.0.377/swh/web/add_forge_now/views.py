# Copyright (C) 2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Any, Dict, List

from django.conf.urls import url
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from swh.web.add_forge_now.models import Request as AddForgeRequest
from swh.web.api.views.add_forge_now import (
    AddForgeNowRequestPublicSerializer,
    AddForgeNowRequestSerializer,
)
from swh.web.auth.utils import ADD_FORGE_MODERATOR_PERMISSION


def add_forge_request_list_datatables(request: HttpRequest) -> HttpResponse:
    """Dedicated endpoint used by datatables to display the add-forge
    requests in the Web UI.
    """

    draw = int(request.GET.get("draw", 0))

    add_forge_requests = AddForgeRequest.objects.all()

    table_data: Dict[str, Any] = {
        "recordsTotal": add_forge_requests.count(),
        "draw": draw,
    }

    search_value = request.GET.get("search[value]")

    column_order = request.GET.get("order[0][column]")
    field_order = request.GET.get(f"columns[{column_order}][name]", "id")
    order_dir = request.GET.get("order[0][dir]", "desc")

    if field_order:
        if order_dir == "desc":
            field_order = "-" + field_order
        add_forge_requests = add_forge_requests.order_by(field_order)

    per_page = int(request.GET.get("length", 10))
    page_num = int(request.GET.get("start", 0)) // per_page + 1

    if search_value:
        add_forge_requests = add_forge_requests.filter(
            Q(forge_type__icontains=search_value)
            | Q(forge_url__icontains=search_value)
            | Q(status__icontains=search_value)
        )

    if (
        int(request.GET.get("user_requests_only", "0"))
        and request.user.is_authenticated
    ):
        add_forge_requests = add_forge_requests.filter(
            submitter_name=request.user.username
        )

    paginator = Paginator(add_forge_requests, per_page)
    page = paginator.page(page_num)

    if request.user.has_perm(ADD_FORGE_MODERATOR_PERMISSION):
        requests = AddForgeNowRequestSerializer(page.object_list, many=True).data
    else:
        requests = AddForgeNowRequestPublicSerializer(page.object_list, many=True).data

    results = [dict(request) for request in requests]

    table_data["recordsFiltered"] = add_forge_requests.count()
    table_data["data"] = results
    return JsonResponse(table_data)


FORGE_TYPES: List[str] = [
    "bitbucket",
    "cgit",
    "gitlab",
    "gitea",
    "heptapod",
]


def create_request(request):
    """View to create a new 'add_forge_now' request.

    """

    return render(
        request, "add_forge_now/create-request.html", {"forge_types": FORGE_TYPES},
    )


urlpatterns = [
    url(
        r"^add-forge/request/list/datatables/$",
        add_forge_request_list_datatables,
        name="add-forge-request-list-datatables",
    ),
    url(r"^add-forge/request/create/$", create_request, name="forge-add"),
]
