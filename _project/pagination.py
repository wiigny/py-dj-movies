from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 6
    page_query_param = "page"
    page_size_query_param = "all_results"
