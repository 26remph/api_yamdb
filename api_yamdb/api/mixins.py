from rest_framework import mixins, viewsets
from .permissions import AdminOrReadOnly


class PostDeleteByAdminOrReadOnlyMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Mixin: GET(list only), POST и DELETE.
    GET - для всех.
    POST и DELETE - только для админа.
    """


class PostDeletePatchByAdminOrReadOnlyMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Mixin: GET(list and detail), POST, PATCH, DELETE.
    GET - для всех.
    POST, PATCH и DELETE - только для админ.
    """
    permission_classes = (AdminOrReadOnly, )
