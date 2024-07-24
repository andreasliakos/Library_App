from django.urls import path, include
from .views import (
    BookList,
    BookDetail,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("books/", BookList.as_view(), name="book_list"),
    path("books/<int:pk>/", BookDetail.as_view(), name="book_detail"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
