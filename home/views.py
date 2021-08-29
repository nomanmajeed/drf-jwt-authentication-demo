from django.contrib.auth.models import User
from rest_framework import serializers, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Student, Book, Category
from .serializers import (
    StudentSerializer,
    BookSerializer,
    CategorySerializer,
    UserSerializer,
)

# Create your views here.


@api_view(["GET"])
def home(request):

    student_objs = Student.objects.all()
    serializer = StudentSerializer(
        student_objs, many=True
    )  # many=True for bulk data (more than one record) else many=False

    # Serialized Data can be accessed using serializer.data

    return Response({"status": 200, "payload": serializer.data})


"""
Simple POST Request
"""

# @api_view(["POST"])
# def post_student(request):

#     data = request.data
#     print(data)

#     return Response(
#         {"status": 200, "payload": "Message Recieved at POST_Student Successfully"}
#     )


"""
POST Request with Data Insertion
"""


@api_view(["POST"])
def post_student(request):

    serializer = StudentSerializer(data=request.data)  # Serialized Data to be inserted

    if not serializer.is_valid():

        return Response(
            {
                "status": 403,
                "errors": serializer.errors,
                "message": "Something went Wrong",
            }
        )

    serializer.save()

    return Response(
        {"status": 200, "payload": request.data, "message": "Your data is inserted"}
    )


@api_view(["PUT"])
def update_student_put(request, id):
    print("id: ", id)

    try:
        print("Indide Try")
        student_objs = Student.objects.get(id=id)
        print("student_objs: ", student_objs)

        serializer = StudentSerializer(student_objs, request.data)
        print("serializer: ", serializer)
        if not serializer.is_valid():
            return Response(
                {
                    "status": 403,
                    "errors": serializer.errors,
                    "message": "Something went Wrong",
                }
            )

        serializer.save()

        return Response(
            {"status": 200, "payload": request.data, "message": "Your data is updated"}
        )

    except Exception as e:
        print("Indide Except")
        return Response(
            {
                "status": 403,
                "errors": "Invalid Id Passed",
                "message": "Something went Wrong",
            }
        )


@api_view(["PATCH"])
def update_student_patch(request, id):
    print("id: ", id)

    try:
        print("Indide Try")
        student_objs = Student.objects.get(id=id)
        print("student_objs: ", student_objs)

        serializer = StudentSerializer(student_objs, request.data, partial=True)
        print("serializer: ", serializer)
        if not serializer.is_valid():
            return Response(
                {
                    "status": 403,
                    "errors": serializer.errors,
                    "message": "Something went Wrong",
                }
            )

        serializer.save()

        return Response(
            {"status": 200, "payload": request.data, "message": "Your data is updated"}
        )

    except Exception as e:
        print("Indide Except")
        return Response(
            {
                "status": 403,
                "errors": "Invalid Id Passed",
                "message": "Something went Wrong",
            }
        )


@api_view(["DELETE"])
def delete_student(request, id):
    print("id: ", id)

    try:
        print("Indide Try")
        student_objs = Student.objects.get(id=id)
        print("student_objs: ", student_objs)

        student_objs.delete()

        return Response(
            {"status": 200, "payload": request.data, "message": "Your data is deleted"}
        )

    except Exception as e:
        print("Indide Except")
        return Response(
            {
                "status": 403,
                "errors": "Invalid Id Passed",
                "message": "Something went Wrong",
            }
        )


@api_view(["GET"])
def get_book(request):

    book_objs = Book.objects.all()
    serializer = BookSerializer(book_objs, many=True)

    return Response(
        {
            "status": 200,
            "payload": serializer.data,
            "message": "Request Successful",
        }
    )


"""
USE OF APIVIEW using Class based Views

"""


class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "status": 403,
                    "errors": serializer.errors,
                    "message": "Something went Wrong",
                }
            )

        serializer.save()

        user = User.objects.get(username=serializer.data["username"])
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": 200,
                "payload": serializer.data,
                "refresh-token": str(refresh),
                "access-token": str(refresh.access_token),
                "message": "User Registered and Token Created",
            }
        )


class StudentAPI(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(
            student_objs, many=True
        )  # many=True for bulk data (more than one record) else many=False

        # Serialized Data can be accessed using serializer.data

        return Response({"status": 200, "payload": serializer.data})

    def post(self, request):
        serializer = StudentSerializer(
            data=request.data
        )  # Serialized Data to be inserted

        if not serializer.is_valid():

            return Response(
                {
                    "status": 403,
                    "errors": serializer.errors,
                    "message": "Something went Wrong",
                }
            )

        serializer.save()

        return Response(
            {"status": 200, "payload": request.data, "message": "Your data is inserted"}
        )

    def put(self, request):
        try:
            print("Indide Try")
            student_objs = Student.objects.get(id=request.data["id"])
            print("student_objs: ", student_objs)

            serializer = StudentSerializer(student_objs, request.data)
            print("serializer: ", serializer)
            if not serializer.is_valid():
                return Response(
                    {
                        "status": 403,
                        "errors": serializer.errors,
                        "message": "Something went Wrong",
                    }
                )

            serializer.save()

            return Response(
                {
                    "status": 200,
                    "payload": request.data,
                    "message": "Your data is updated",
                }
            )

        except Exception as e:
            print("Indide Except")
            return Response(
                {
                    "status": 403,
                    "errors": "Invalid Id Passed",
                    "message": "Something went Wrong",
                }
            )

    def delete(self, request):
        try:
            print("Indide Try")
            id = request.GET.get("id")
            student_objs = Student.objects.get(id=id)
            print("student_objs: ", student_objs)

            student_objs.delete()

            return Response(
                {
                    "status": 200,
                    "payload": request.data,
                    "message": "Your data is deleted",
                }
            )

        except Exception as e:
            print("Indide Except")
            return Response(
                {
                    "status": 403,
                    "errors": "Invalid Id Passed",
                    "message": "Something went Wrong",
                }
            )


class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):
    """
    ListAPIView => GET request
    CreateAPIView = > POST Request
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGenericByID(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    UpdateAPIView => PUT/PATCH request
    DestroyAPIView = > DELETE Request
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"  # to get id from url i-e generic_student/1/
