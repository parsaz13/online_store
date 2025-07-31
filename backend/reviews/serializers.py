from rest_framework import serializers
from .models import Comment
from products.models import Product
from users.models import CustomUser

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True, source='product.id')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'product_id', 'comment', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'is_published', 'created_at', 'updated_at']

    def validate(self, data):
        product_id = data.get('product').get('id')
        try:
            Product.objects.get(id=product_id, is_deleted=False)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return data

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product']['id'])
        return Comment.objects.create(
            user=self.context['request'].user,
            product=product,
            comment=validated_data['comment'],
            is_published=False
        )