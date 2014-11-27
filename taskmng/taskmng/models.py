from django.db import models
from django.contrib.auth.models import User


class TaskSchedule(models.Model):
	task_schedule_name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.task_schedule_name

class Task(models.Model):
	TASK_CATEGORY = (
		('S', 'Schedule'),
		('I', 'Incidental'),
	)
	task_schedule = models.ForeignKey(TaskSchedule, blank=True, null=True)
	task_name = models.CharField(max_length=128)
	task_category = models.CharField(max_length=1, choices=TASK_CATEGORY)
	task_description = models.TextField()
	task_manual = models.TextField(blank=True, null=True)
	task_start_datetime = models.DateTimeField()
	task_end_datetime = models.DateTimeField()
	task_note = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.task_name

class Attachment(models.Model):
	ATTACHMENT_TYPE = (
		('I', 'Image'),
		('A', 'Audio'),
		('D', 'Document'),
	)
	task = models.ForeignKey(Task)
	Attachment_type = models.CharField(max_length=1, choices=ATTACHMENT_TYPE)
	Attachment_file = models.FileField()

class UserTask(models.Model):
	TASK_STATUS = (
        ('D', 'Done'),
        ('V', 'Verified'),
    )
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	usertask_status = models.CharField(blank=True, null=True, max_length=1, choices=TASK_STATUS)