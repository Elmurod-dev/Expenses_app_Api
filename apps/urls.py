from django.urls import path

from apps.views import ExpensesCreateApiview, ExpensesDeleteApiview, ExpensesUpdateApiview, \
    ExpensesDetailApiView, ExpensesListApiView, BalanceApiview, CategoryTypeListApiView, CategoryListApiView, \
    CategoryUpdateApiview, CategoryDeleteApiview
from apps.views import ForgotPasswordAPIView, ForgotPasswordCheckAPIView, PasswordResetView, RegisterAPIView, \
    RegisterCheckAPIView

urlpatterns=[
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

urlpatterns+=[
    path('forgot-password', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('verify-otp', ForgotPasswordCheckAPIView.as_view(), name='forgot_password_check'),
    path('auth/reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('register/check', RegisterCheckAPIView.as_view(), name='register-check'),
]