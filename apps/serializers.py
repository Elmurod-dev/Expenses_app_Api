from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User, Expense, Category


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'type']

class ExpensesCategorySerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Expense
        fields = ['pk', 'amount', 'category', 'description','type']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category = instance.category
        representation['category'] = CategorySerializer(category).data  # Category obyektini serialize qilish
        return representation


class BalanceSerializer(Serializer):
    total = IntegerField()
    income_sum =IntegerField()
    expenses_sum = IntegerField()



