from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SignupForm(UserCreationForm):
    """
        Registration form for new users.

        Extends Django's built-in UserCreationForm to work with the
        custom User model. It collects the user's email, first name,
        and password, while handling password confirmation and hashing
        automatically.
    """

    email = forms.EmailField(
        label="ایمیل",
        error_messages={
            "required": "وارد کردن ایمیل الزامی است.",
            "invalid": "آدرس ایمیل معتبر نیست.",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ایمیل خود را وارد کنید",
                "autocomplete": "email",
            }
        ),
    )

    first_name = forms.CharField(
        label="نام",
        error_messages={
            "required": "وارد کردن نام الزامی است.",
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "نام خود را وارد کنید",
                "autocomplete": "given-name",
            }
        ),
    )

    password1 = forms.CharField(
        label="رمز عبور",
        error_messages={
            "required": "وارد کردن رمز عبور الزامی است.",
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور را وارد کنید",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        error_messages={
            "required": "تکرار رمز عبور الزامی است.",
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور را دوباره وارد کنید",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")

        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیستند.")

        errors = []

        try:
            validate_password(password2, self.instance)

        except ValidationError as e:

            for error in e.messages:

                if "too short" in error:
                    errors.append("رمز عبور باید حداقل ۸ کاراکتر باشد.")

                elif "too common" in error:
                    errors.append("رمز عبور انتخاب شده بسیار رایج است.")

                elif "entirely numeric" in error:
                    errors.append("رمز عبور نباید فقط شامل اعداد باشد.")

                elif "too similar" in error:
                    errors.append("رمز عبور نباید شبیه اطلاعات شخصی شما باشد.")

                else:
                    errors.append(error)

        if errors:
            raise ValidationError(errors)

        return password2


class LoginForm(AuthenticationForm):

    """
        Authentication form for existing users.

        This form customizes Django's built-in AuthenticationForm by
        providing Persian labels, placeholders, and CSS classes for
        rendering a styled login interface while preserving Django's
        default authentication behavior.
    """

    error_messages = {
        "invalid_login": "ایمیل یا رمز عبور وارد شده صحیح نیست.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }

    username = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل خود را وارد کنید',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'autocomplete': 'current-password',
        })
    )
