
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import CitizenProfile

User = get_user_model()


class CitizenRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Phone Number",
        help_text="Enter 0712345678 or +254712345678.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "phone_number")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose another."
            )

        return username

    def clean_phone_number(self):
        phone = re.sub(
            r"[\s()-]", "", self.cleaned_data["phone_number"]
        )

        # Convert Kenyan numbers to international format.
        if phone.startswith("0") and len(phone) == 10:
            phone = "+254" + phone[1:]
        elif phone.startswith("254") and len(phone) == 12:
            phone = "+" + phone

        # Validate Kenyan mobile numbers.
        if not re.fullmatch(r"\+254[17]\d{8}", phone):
            raise forms.ValidationError(
                "Invalid phone number. Enter a valid Kenyan mobile "
                "number, e.g. 0712345678 or +254712345678."
            )

        # Prevent the same phone number being registered twice.
        if CitizenProfile.objects.filter(
            phone_number=phone
        ).exists():
            raise forms.ValidationError(
                "This phone number is already registered. "
                "Please use another number."
            )

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            CitizenProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"],
            )

        return user
