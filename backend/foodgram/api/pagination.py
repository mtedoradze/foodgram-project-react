from rest_framework.pagination import PageNumberPagination

RECIPES_PER_PAGE = 6

MAX_PAGE_SIZE = 10


class StandardResultsSetPagination(PageNumberPagination):
    page_size = RECIPES_PER_PAGE
    page_query_param = 'page'
    page_size_query_param = 'limit'
    # max_page_size = MAX_PAGE_SIZE
