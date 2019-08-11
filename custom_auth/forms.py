from django import forms
from custom_auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'role'
        )

    # for hashing the password field
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
