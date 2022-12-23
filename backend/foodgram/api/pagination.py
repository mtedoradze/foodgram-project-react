from rest_framework.pagination import PageNumberPagination

POSTS_PER_PAGE = 6

MAX_PAGE_SIZE = 10


class StandardResultsSetPagination(PageNumberPagination):
    page_size = POSTS_PER_PAGE
    page_size_query_param = 'limit'
    max_page_size = MAX_PAGE_SIZE
