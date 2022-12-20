from rest_framework.pagination import PageNumberPagination

from foodgram import settings


class StandardResultsSetPagination(PageNumberPagination):
    page_size = settings.POSTS_PER_PAGE
    page_size_query_param = 'limit'
    max_page_size = 10
