import rest_framework.pagination as pagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'items': data
        })
