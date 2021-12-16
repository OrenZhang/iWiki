from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class NumPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 100
    invalid_page_message = "页码有误，请切换为第一页"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("page", self.page.number),
                    ("results", data),
                ]
            )
        )


class RepoListNumPagination(NumPagination):
    page_size = 16
