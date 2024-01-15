from django import forms
from task_manager.models import Task


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
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
        super(ProjectTaskForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['project'].initial = kwargs['instance'].project

    def save(self, commit=True):
        task = super().save(commit=False)
        task.save()
        task.task_type.set(self.cleaned_data['task_type'])

        if commit:
            task.save()
        return task

