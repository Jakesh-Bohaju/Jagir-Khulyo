from rest_framework import serializers

from blog.models import Comment
from custom_auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class CommentChildSerializer(serializers.ModelSerializer):
    comment_user = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'answer',
            'comment_user'
        )


class CommentSerializer(serializers.ModelSerializer):
    # creating new field
    child_comments = serializers.SerializerMethodField()

    def get_child_comments(self, obj):
        return CommentChildSerializer(obj.sub_comments.all(), many=True).data

    class Meta:
        model = Comment
        fields = (
            'id',
            'answer',
            'child_comments',
            'comment_date',
            'comment_user'
        )
