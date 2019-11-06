from django.db import models
from django_mysql.models import JSONField

# Create your models here.

default_img_link = "https://images.unsplash.com/photo-1544847558-3ccacb31ee7f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
    	return self.name

# class Keywords_record(models.Model):
# 	keyword_name = models.CharField(max_length=250, unique=True)
# 	keyword_image_url = models.URLField(max_length=250)

# 	def __str__(self):
# 		return self.keyword_name

class Tag_details(models.Model):
	unique_id = models.CharField(max_length=250, unique=True)
	url = models.URLField(max_length=250, default="https://knowzone.ghostzones.ml/404/")
	name = models.CharField(max_length=250, unique=True)
	slug = models.CharField(max_length=250, unique=True)
	created_at = models.DateTimeField()
	meta_title = models.CharField(max_length=1000, null=True)
	updated_at = models.DateTimeField()
	visibility = models.CharField(max_length=250, default="public")
	description = models.TextField(max_length=1000, null=True)
	feature_image = models.URLField(max_length=250, null=True)
	meta_description = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.name

class Unregister_tags(models.Model):
	url = models.URLField(max_length=250, default="https://knowzone.ghostzones.ml/404/")
	name = models.CharField(max_length=250, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	visibility = models.CharField(max_length=250, default="public")
	feature_image = models.URLField(max_length=250, null=True)


class Data_record(models.Model):
	title = models.CharField(max_length=250, unique=True)
	feature_image = models.URLField(max_length=250, default=default_img_link)
	file_path = models.URLField(max_length=250, null=True)
	iframe = models.BooleanField(default=False)
	mobiledoc = models.TextField(max_length=2000, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	keywords = models.TextField(max_length=1000, null=True)
	complete_tags = models.ManyToManyField(Tag_details)
	Not_registered_tags = models.ManyToManyField(Unregister_tags)
	categories = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
	keywords_with_links = JSONField(null=True)
	excel_uploaded = models.BooleanField(default=False)
	ghost_post_id = models.CharField(max_length=500, blank=True, default="Not reviewed yet")
	ghost_post_uuid = models.CharField(max_length=500, blank=True, default="Not reviewed yet")

	def __str__(self):
		return self.title
 
class All_post_sync(models.Model):
	record = models.ForeignKey('Data_record', on_delete=models.CASCADE, null=True)
	publish_status = models.BooleanField(default=False)
	
	def __str__(self):
		return self.record.title

class present_ghost_tags(models.Model):
	all_tags = JSONField()
	hit_details = JSONField()
