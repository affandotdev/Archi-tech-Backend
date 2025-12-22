# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import get_user_model
# from django.db.models import Q
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from src.infrastructure.message_broker import publish_user_role_updated_event
# from src.presentation.serializers.admin_serializer import AdminUserSerializer
# from src.infrastructure.message_broker import publish_user_updated_event

# User = get_user_model()

# class IsAdminUser(permissions.BasePermission):
#     """
#     Allows access only to admin users.
#     """
#     def has_permission(self, request, view):
#         print(f"DEBUG [AuthService]: Checking permission for user {request.user}")
#         if not request.user or not request.user.is_authenticated:
#             print("DEBUG [AuthService]: User not authenticated")
#             return False
        
#         is_admin = getattr(request.user, 'role', None) == 'admin'
#         print(f"DEBUG [AuthService]: User Role: {getattr(request.user, 'role', 'None')} -> Is Admin? {is_admin}")
#         return is_admin


# class AdminUserListController(APIView):
#     permission_classes = [IsAdminUser]

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('search', openapi.IN_QUERY, description="Search by email, first_name, last_name", type=openapi.TYPE_STRING),
#         ],
#         responses={200: AdminUserSerializer(many=True)}
#     )
#     def get(self, request):
#         print("DEBUG [AuthService]: AdminUserListController GET called")
#         search_query = request.query_params.get("search", "")
#         try:
#             users = User.objects.all().order_by("-date_joined")
#             print(f"DEBUG [AuthService]: Total users found: {users.count()}")

#             if search_query:
#                 users = users.filter(
#                     Q(email__icontains=search_query) |
#                     Q(first_name__icontains=search_query) |
#                     Q(last_name__icontains=search_query)
#                 )

#             serializer = AdminUserSerializer(users, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#             print(f"DEBUG [AuthService]: Error fetching users: {e}")
#             return Response({"error": str(e)}, status=500)


# class AdminUserDetailController(APIView):
#     permission_classes = [IsAdminUser]

#     @swagger_auto_schema(responses={200: AdminUserSerializer})
#     def get(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = AdminUserSerializer(user)
#         return Response(serializer.data)

#     def delete(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             user.delete() 
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# class AdminUserStatusController(APIView):
#     permission_classes = [IsAdminUser]

#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={'status': openapi.Schema(type=openapi.TYPE_BOOLEAN)}
#     ))
#     def patch(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             is_active = request.data.get("status")
#             if is_active is None:
#                 return Response({"error": "Status required"}, status=400)
#             user.is_active = is_active
#             user.save()
            
#             # 🔥 Publish Event
#             publish_user_updated_event(user.id, {"is_active": is_active})

#             return Response({"message": "Status updated"})
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)




# class AdminUserRoleController(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             role = request.data.get("role")
#             if not role:
#                 return Response({"error": "Role required"}, status=400)

#             user.role = role
#             user.save()

#             publish_user_role_updated_event(user.id, role)

#             return Response({"message": "Role updated"})
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)



# class AdminUserVerifyController(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request, user_id):
#         try:
#             user = User.objects.get(id=user_id)
#             user.is_verified = True
#             user.save()
#             return Response({"message": "User verified"})
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)


# class AdminDashboardStatsController(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         total_users = User.objects.count()
#         # Using active users as a proxy for "Active Sessions" for now
#         active_sessions = User.objects.filter(is_active=True).count()
#         # Placeholder for incidents
#         open_incidents = 0 
        
#         return Response({
#             "totalUsers": total_users,
#             "total_users": total_users, # Fallback
#             "activeSessions": active_sessions,
#             "active_sessions": active_sessions, # Fallback
#             "openIncidents": open_incidents,
#             "open_incidents": open_incidents, # Fallback
#         })


# class AdminSystemHealthController(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         # Mock health check for now. In a real system, you'd ping dependencies.
#         return Response({
#             "auth": "Operational",
#             "user": "Operational",
#             "notifications": "Operational",
#             "database": "Connected"
#         })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.presentation.serializers.admin_serializer import AdminUserSerializer
from src.infrastructure.message_broker import publish_user_role_updated_event

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, "role", None) == "admin"


class AdminUserListController(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search by email, first_name, last_name",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: AdminUserSerializer(many=True)},
    )
    def get(self, request):
        search_query = request.query_params.get("search", "")

        users = User.objects.all().order_by("-date_joined")

        if search_query:
            users = users.filter(
                Q(email__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserDetailController(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={200: AdminUserSerializer})
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = AdminUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminUserStatusController(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "status": openapi.Schema(type=openapi.TYPE_BOOLEAN)
            },
        )
    )
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            is_active = request.data.get("status")

            if is_active is None:
                return Response({"error": "Status required"}, status=400)

            user.is_active = is_active
            user.save()

            # ❌ NO EVENTS HERE (Auth-only state)
            return Response({"message": "Status updated"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class AdminUserRoleController(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "role": openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    )
    def post(self, request, user_id):
        role = request.data.get("role")
        if not role:
            return Response({"error": "Role required"}, status=400)

        user = User.objects.get(id=user_id)
        user.role = role
        user.save()

        # 🔥 ONLY event that touches role
        publish_user_role_updated_event(user.id, role, is_verified=True)

        return Response({"message": "Role updated"})
    

    

class AdminUserVerifyController(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()

            # Optional future event: USER_VERIFIED
            return Response({"message": "User verified"})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class AdminDashboardStatsController(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()

        return Response(
            {
                "totalUsers": total_users,
                "activeSessions": active_users,
                "openIncidents": 0,
            }
        )


class AdminSystemHealthController(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(
            {
                "auth": "Operational",
                "user": "Operational",
                "database": "Connected",
            }
        )
