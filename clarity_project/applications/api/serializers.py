from rest_framework import serializers

from clarity_project.applications.models import SchoolApplication


class SchoolApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolApplication
        fields = "__all__"
