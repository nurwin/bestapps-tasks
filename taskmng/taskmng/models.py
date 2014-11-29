from django.db import models
from django.contrib.auth.models import User


class TaskCategory(models.Model):
	TASK_TYPE = (
		('S', 'Schedule'),
		('I', 'Incidental'),
	)

	task_category_name = models.CharField(max_length=50)
	task_category_type = models.CharField(max_length=1, choices=TASK_TYPE)
	task_category_start_time = models.DateTimeField()
	task_category_end_time = models.DateTimeField()

	def __unicode__(self):
		return self.task_category_name

class Task(models.Model):
	task_category = models.ForeignKey(TaskCategory, blank=True, null=True)
	task_name = models.CharField(max_length=128)
	task_description = models.TextField()
	task_manual = models.TextField(blank=True, null=True)
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
        ('R', 'Rejected'),
        ('A', 'Accepted'),
    )
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	usertask_status = models.CharField(blank=True, null=True, max_length=1, choices=TASK_STATUS)
	usertask_note = models.TextField(blank=True, null=True)