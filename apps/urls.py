from django.urls import path

from apps.views import RegisterApiview, ExpensesCreateApiview, ExpensesDeleteApiview, ExpensesUpdateApiview, \
    ExpensesDetailApiView, ExpensesListApiView, BalanceApiview, CategoryTypeListApiView, CategoryListApiView, \
    CategoryUpdateApiview,CategoryDeleteApiview

urlpatterns = [
    path("auth/register/",RegisterApiview.as_view()),
]


urlpatterns+=[
    path("expenses/", ExpensesCreateApiview.as_view()),
    path("expenses/delete/<int:pk>", ExpensesDeleteApiview.as_view()),
    path("expenses/update/<int:pk>", ExpensesUpdateApiview.as_view()),
    path("expenses/<int:pk>", ExpensesDetailApiView.as_view()),
    path("expenses/list/", ExpensesListApiView.as_view()),
    path("expenses/balance/", BalanceApiview.as_view()),
    path("category/<str:type>", CategoryTypeListApiView.as_view()),
]

urlpatterns+=[
    path("admin/category/", CategoryListApiView.as_view()),
    path("admin/category/update/<int:pk>", CategoryUpdateApiview.as_view()),
    path("admin/category/delete/<int:pk>", CategoryDeleteApiview.as_view()),
]