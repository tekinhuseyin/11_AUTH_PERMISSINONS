from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class MyNumberPagination(PageNumberPagination):
    page_size=5 # her sayhfa için  max obje sayısı
    page_query_param="sayfa"  # query deki key page yerine
    page_size_query_param="adet"  # donen veriyi sınarla
    max_page_size=3 
    ordering="id"


class MyLimitPaginatian(LimitOffsetPagination):
    default_limit=8
    limit_query_param="kac_tane"
    offset_query_param="kacinci"
    # offset_query_description=10

class MyCursorPaginatian(CursorPagination):
    page_size=10
    
    ordering="-first_name"
