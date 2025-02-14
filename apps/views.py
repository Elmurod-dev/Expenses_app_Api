from drf_spectacular.utils import extend_schema
from rest_framework import request
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from apps.models import Expense, Category
from apps.serializers import RegisterSerializer, ExpensesCategorySerializer, BalanceSerializer, CategorySerializer


@extend_schema(tags=["Auth"],request=RegisterSerializer,responses=RegisterSerializer)
class RegisterApiview(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)



########################## Expenses

@extend_schema(tags=["Expenses"],request=ExpensesCategorySerializer)
class ExpensesCreateApiview(CreateAPIView):
    serializer_class = ExpensesCategorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user)
        return Response(self.get_serializer(instance).data, status=HTTP_201_CREATED)


@extend_schema(tags=["Expenses"],responses=ExpensesCategorySerializer)
class ExpensesDeleteApiview(DestroyAPIView):
    serializer_class = ExpensesCategorySerializer
    lookup_field = 'pk'
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.user != user:
            return Response({"detail": "You do not have permission to delete this expense."},
                            status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(tags=["Expenses"],responses=ExpensesCategorySerializer)
class ExpensesUpdateApiview(UpdateAPIView):
    serializer_class = ExpensesCategorySerializer
    lookup_field = 'pk'
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.request.user
        instance = self.get_object()
        if instance.user != user:
            return Response({"detail": "You do not have permission to delete this expense."},
                            status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.get_serializer(instance).data, status=HTTP_200_OK)


@extend_schema(tags=["Expenses"])
class ExpensesDetailApiView(RetrieveAPIView):
    serializer_class = ExpensesCategorySerializer
    queryset = Expense.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        if instance.user != user:
            return Response({"detail": "You do not have permission to view this expense."},
                            status=HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@extend_schema(tags=["Expenses"],responses=ExpensesCategorySerializer)
class ExpensesListApiView(ListAPIView):
    serializer_class = ExpensesCategorySerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



@extend_schema(tags=["Expenses"])
class BalanceApiview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        amounts = Expense.objects.filter(user=self.request.user)
        total = sum(amounts.values_list('amount', flat=True))
        income_sum = sum(amounts.filter(type='income').values_list('amount', flat=True))
        expenses_sum = sum(amounts.filter(type='expense').values_list('amount', flat=True))

        response = {
            'total': total,
            'income': income_sum,
            'expenses': expenses_sum,
        }
        return Response(response, status=HTTP_200_OK)


############################### Category
@extend_schema(tags=["Category"],responses=CategorySerializer)
class CategoryTypeListApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'type'

    def get_queryset(self):
        type = self.kwargs['type']
        return Category.objects.filter(type=type)



################ ADMIN

@extend_schema(tags=["Admin"],responses=CategorySerializer)
class CategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Admin"],responses=CategorySerializer)
class CategoryUpdateApiview(UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=["Admin"],responses=CategorySerializer)
class CategoryDeleteApiview(DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    lookup_field = 'pk'