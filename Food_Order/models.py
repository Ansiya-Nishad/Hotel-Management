from django.db import models
from django.contrib.auth.models import User


class HotelDb(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.IntegerField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Created_Hotels"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class HotelBookingDb(models.Model):
    hotel = models.ForeignKey(
        HotelDb, on_delete=models.CASCADE, related_name="hotel_bookings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hotel_bookings"
    )
    check_in = models.DateField()
    check_out = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hotel', 'user', 'check_in'],
                name='unique_hotel_booking'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.hotel.title}"
