from DSR.utils import BaseModel, ULIDField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(BaseModel):

    internal_id = ULIDField(_('project ulid'), editable=False)
    name = models.CharField(_('project name'), max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class TaskType(BaseModel):

    internal_id = ULIDField(_('task type ulid'), editable=False)
    name = models.CharField(_('type'), max_length=150)
    slug = models.SlugField(_('type slug'), max_length=150)


class DailyStatusReport(models.Model):

    internal_id = ULIDField(_('dsr ulid'), editable=False)
    date = models.DateField(_('date'))
    task_details = models.TextField(_('task details'))
    status_summary = models.TextField(_('status summary'))
    hours_worked = models.DecimalField(_('hours worked'), max_digits=5, decimal_places=2, editable=False)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('user.UserAccount', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} - {self.task.name} - {self.date}"