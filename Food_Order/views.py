
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,serializers
from Food_Order import permissions
from Food_Order.models import HotelDb,HotelBookingDb
from Food_Order.serializers import UserSerializer,HotelSerializer,HotelBookingSerializer



class SignUpView(APIView):
    def post(self, request):
        serializer_instance = UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(
                {"Message": "User Created Successfully..."},
                status=201
            )
        return Response(serializer_instance.errors, status=400)


class UserCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer_instance = UserSerializer(users, many=True)
        return Response(serializer_instance.data)


class HotelCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.OwnerOnly]

    def get(self, request):
        qs = HotelDb.objects.filter(created_by=request.user)
        serializer_instance = HotelSerializer(qs, many=True)
        return Response(serializer_instance.data)

    def post(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by != request.user:
            return Response(
                {"Message": "Permission Denied!"},
                status=403
            )
        serializer_instance = HotelBookingSerializer(
            data=request.data,
            context={'hotel': hotel}
        )
        if serializer_instance.is_valid():
            serializer_instance.save(hotel=hotel)

            return Response({
                "Message": "Booking Created Successfully...",
                "Booking Details": serializer_instance.data
            }, status=201)

        return Response(serializer_instance.errors, status=400)

class HotelRetriveUpdateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.OwnerOnly]

    def get(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by != request.user:
            return Response({"Message": "Permission Denied!"}, status=403)
        serializer_instance = HotelSerializer(hotel)
        return Response(serializer_instance.data)

    def put(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by != request.user:
            raise serializers.ValidationError("Access Denied!")
        serializer_instance = HotelSerializer(
            instance=hotel, data=request.data
        )
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Hotel Updated Successfully...",
                "Updated Details": serializer_instance.data
            })
        return Response(serializer_instance.errors, status=400)

    def delete(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by == request.user:
            hotel.delete()
            return Response({"Message": "Hotel Deleted Successfully..."})
        return Response({"Message": "Permission Denied!"}, status=403)


class HotelBookingView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.OwnerOnly]

    def get(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by != request.user:
            return Response({"Message": "Permission Denied!"}, status=403)
        bookings = HotelBookingDb.objects.filter(hotel=hotel)
        serializer_instance = HotelBookingSerializer(
            bookings, many=True, context={'hotel': hotel}
        )
        return Response(serializer_instance.data)

    def post(self, request, pk):
        hotel = get_object_or_404(HotelDb, id=pk)
        if hotel.created_by != request.user:
            return Response({"Message": "Permission Denied!"}, status=403)
        serializer_instance = HotelBookingSerializer(
            data=request.data, context={'hotel': hotel}
        )
        if serializer_instance.is_valid():
            serializer_instance.save(hotel=hotel)
            return Response({
                "Message": "Booking Created Successfully...",
                "Booking Details": serializer_instance.data
            }, status=201)
        return Response(serializer_instance.errors, status=400)


class HotelBookingDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.OwnerOnly]

    def delete(self, request, pk):
        booking = get_object_or_404(HotelBookingDb, id=pk)
        if booking.hotel.created_by != request.user:
            return Response({"Message": "Permission Denied!"}, status=403)
        booking.delete()
        return Response({"Message": "Booking Deleted Successfully..."})

