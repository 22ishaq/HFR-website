from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Application, Profile, Team

# Suggested for the major autocomplete; free text is still allowed.
COMMON_DEGREES = [
    'Aeronautical Engineering', 'Aerospace Systems', 'Mechanical Engineering',
    'Mechatronics', 'Electronics & Electrical Engineering',
    'Electronics & Software Engineering', 'Computer Science', 'Software Engineering',
    'Civil Engineering', 'Biomedical Engineering', 'Product Design Engineering',
    'Physics', 'Mathematics', 'Chemistry', 'Economics', 'Business & Management',
    'Accountancy & Finance', 'Marketing', 'Law', 'Politics', 'Psychology',
]


# You have to be at the university to apply, so the GUID address is the proof.
# Postgrads and staff often use the second domain rather than the first.
GLASGOW_EMAIL_DOMAINS = ('student.gla.ac.uk', 'glasgow.ac.uk')


class SignUpForm(forms.ModelForm):
    """Account creation. Four fields, exactly as the wireframe draws them."""

    name = forms.CharField(
        max_length=100, label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        label='GUID Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'GUID Email Address', 'autocomplete': 'email',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password', 'autocomplete': 'new-password',
        }),
    )
    password_confirm = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password', 'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password_confirm')

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())
        if len(name) < 2:
            raise forms.ValidationError('Enter your full name.')
        return name

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if email.rpartition('@')[2] not in GLASGOW_EMAIL_DOMAINS:
            allowed = ' or '.join('@' + d for d in GLASGOW_EMAIL_DOMAINS)
            raise forms.ValidationError(
                f'That is not a University of Glasgow address. Use your GUID email, '
                f'ending in {allowed}.'
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account already exists for that email. Try logging in instead.'
            )
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        password, confirm = cleaned.get('password'), cleaned.get('password_confirm')
        if password and confirm and password != confirm:
            self.add_error('password_confirm', 'The two passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # The GUID is unique, so its local part becomes the username
        user.username = self.cleaned_data['email'].split('@')[0]
        user.email = self.cleaned_data['email']
        first, _, last = self.cleaned_data['name'].partition(' ')
        user.first_name, user.last_name = first, last
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'year_of_study', 'major',
            'first_pick', 'alternative', 'wildcard',
            'cv', 'why_society', 'why_division', 'what_makes_you', 'what_to_learn',
        )
        widgets = {
            'major': forms.TextInput(attrs={
                'list': 'degree-suggestions',
                'placeholder': 'Start typing, e.g. Aerospace, Computer Science…',
                'autocomplete': 'off',
            }),
            'why_society': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'You could build a Formula 1 car, a rocket, a satellite or prosthetics. Why HFR?',
            }),
            'why_division': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'What draws you to your first pick?',
            }),
            'what_makes_you': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Not your grades. What are you actually like to work with?',
            }),
            'what_to_learn': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Skills, tools, experiences. What do you want out of this?',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recruiting = Team.objects.filter(is_recruiting=True)
        for name in ('first_pick', 'alternative', 'wildcard'):
            self.fields[name].queryset = recruiting

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv and cv.size > 5 * 1024 * 1024:
            raise forms.ValidationError('CV must be under 5MB.')
        return cv

    def clean(self):
        cleaned = super().clean()
        picks = [cleaned.get('first_pick'), cleaned.get('alternative'), cleaned.get('wildcard')]
        picks = [p for p in picks if p]
        if len(picks) == 3 and len({p.pk for p in picks}) != 3:
            raise forms.ValidationError(
                'Your first pick, alternative and wildcard must be three different teams.'
            )
        return cleaned


class RedeemCodeForm(forms.Form):
    code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 8F3A21BC', 'autocomplete': 'off'}),
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()


class OnboardingForm(forms.ModelForm):
    """Wireframe 24. Every step is mandatory."""

    class Meta:
        model = Profile
        fields = (
            'display_name', 'avatar', 'avatar_preset',
            'contact_method', 'contact_time', 'phone',
        )
        widgets = {
            'display_name': forms.TextInput(attrs={
                'placeholder': 'Pick a display name', 'autocomplete': 'off',
            }),
            'avatar_preset': forms.RadioSelect,
            'contact_method': forms.RadioSelect,
            'contact_time': forms.RadioSelect,
            'phone': forms.TextInput(attrs={'placeholder': '+44 7…'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'].required = True
        self.fields['contact_method'].required = True
        self.fields['contact_time'].required = True
        # Strip the empty "---------" choice from the radio groups
        for name in ('avatar_preset', 'contact_method', 'contact_time'):
            self.fields[name].choices = [
                c for c in self.fields[name].choices if c[0]
            ]

    def clean_display_name(self):
        name = self.cleaned_data['display_name'].strip()
        clash = Profile.objects.filter(display_name__iexact=name)
        if self.instance.pk:
            clash = clash.exclude(pk=self.instance.pk)
        if clash.exists():
            raise forms.ValidationError('That display name is taken. Try another.')
        return name

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('avatar') and not cleaned.get('avatar_preset'):
            self.add_error('avatar_preset', 'Upload a photo or pick a premade one.')
        if cleaned.get('contact_method') == 'whatsapp' and not cleaned.get('phone', '').strip():
            self.add_error('phone', 'Add your number so we can reach you on WhatsApp.')
        return cleaned
