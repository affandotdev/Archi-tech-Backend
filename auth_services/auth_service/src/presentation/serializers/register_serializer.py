from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(
        choices=[
            ("architect", "Architect"),
            ("engineer", "Engineer"),
            ("client", "Client"),
            ("admin", "Admin"),
        ],
        default="client",
        required=False,
    )
