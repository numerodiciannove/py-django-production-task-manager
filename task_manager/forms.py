from django import forms
from django.forms import PasswordInput

from task_manager.models import Task, Project, Team, Worker, Position


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "is_complete",
            'name',
            'description',
            'start_time',
            'deadline',
            'priority',
            'task_type',
            "project"
        ]
        widgets = {
            'project': forms.HiddenInput(),
            "start_time": forms.DateInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
            "task_type": forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['project'].initial = kwargs['instance'].project

    def save(self, commit=True):
        task = super().save(commit=False)
        task.save()
        task.task_type.set(self.cleaned_data['task_type'])

        if commit:
            task.save()
        return task


class ProjectForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"

    def save(self, commit=True):
        project = super().save(commit=False)
        project.save()
        project.teams.set(self.cleaned_data['teams'])

        if commit:
            project.save()

        return project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'is_complete',
            'name',
            'priority',
            'description',
            'start_time',
            'deadline',
            "project",
            'task_type',
        ]
        widgets = {
            "start_time": forms.DateInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
            "task_type": forms.CheckboxSelectMultiple()
        }


class WorkerForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    confirm_password = forms.CharField(widget=PasswordInput)

    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
            "confirm_password",
            "position",
            "country",
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class TeamForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"


class WorkerSearchForm(forms.Form):
    search_first_last_name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder":
                    "Search: For example, Terry Richardson. "
                    "Another enter just the First Name or Last Name."
            })
    )


class TeamSearchForm(forms.Form):
    search_by_team_name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder":
                    "Search: by team name"
            }
        )
    )


class PositionSearchForm(forms.Form):
    search_by_position = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder":
                    "Search: by position name"
            }
        )
    )
