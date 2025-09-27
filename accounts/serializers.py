from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Membership, Organization

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "owner", "created_at"]
        read_only_fields = ["owner"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.pop("owner", None)
        org = Organization.objects.create(owner=user, **validated_data)
        Membership.objects.create(user=user, organization=org, role="ADMIN")
        return org


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "is_active"]


"""
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "is_active"]

class MembershipSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ["id", "user", "organization", "role", "joined_at"]
        read_only_fields = ["organization", "joined_at"]

class MembershipCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=[("ADMIN","Admin"),("MANAGER","Manager"),("MEMBER","Member")], default="MEMBER")

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def create(self, validated_data):
        org = self.context["organization"]
        user = User.objects.get(id=validated_data["user_id"])
        membership, created = Membership.objects.get_or_create(
            user=user, organization=org, defaults={"role": validated_data["role"]}
        )
        if not created:
            membership.role = validated_data["role"]
            membership.save()
        return membership

"""
