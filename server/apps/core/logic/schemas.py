from drf_yasg import openapi

SUCCESS = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

BAD_REQUEST = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "field_name": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
        ),
    },
)

UNAUTHORIZED = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

NO_CONTENT = openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
