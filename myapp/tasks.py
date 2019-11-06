from __future__ import absolute_import, unicode_literals
from celery import task
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from configparser import ConfigParser
import json, csv, os, urllib, re, time, requests, jwt
from datetime import datetime as date
from django.shortcuts import redirect
from slugify import slugify

from .models import Data_record, Category, present_ghost_tags, Tag_details, All_post_sync, Unregister_tags

from .views import populate_tags_details

current_path = os.getcwd()
config_file = os.path.join(current_path, 'config.ini')
config = ConfigParser()

try:
    config.read(config_file)
except:
    print(" Unable to read config.ini file ")

# Ghost api key 
#print(" ====================== inside task.py  ================")
Ghost_key = config.get("GHOST", "api_key")


# print("this is ghost api key :",Ghost_key)


@task()
def mycron_job():
	print(" ====================== inside mycron_job function ================")
	all_syn_post = All_post_sync.objects.all()
	print(" inside the cron job function ")
	#print(len(all_syn_post))
	if len(all_syn_post) > 0:
		id, secret = Ghost_key.split(':')
		#print(id, secret)
		iat = int(date.now().timestamp())

		header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
		payload = {
			'iat': iat,
			'exp': iat + 5 * 60,
			'aud': '/v2/admin/'
		}
		url = 'https://knowzone.ghostzones.ml/ghost/api/v2/admin/posts/'
		#print(" Mannual Cronjob is running ")

		for post in all_syn_post:
			print(post.id)
			target_post = Data_record.objects.get(id=post.record_id)
			print("target post found")
			token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
			headers = {'Authorization': 'Ghost {}'.format(token.decode())}
			mobiledoc_url = target_post.mobiledoc
			mobiledoc = "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[[\"html\",{\"html\":\"<iframe src=\\\"" + mobiledoc_url + "\\\" width=\\\"100%\\\" height=\\\"1000\\\" frameborder=\\\"0\\\" scrolling=\\\"no\\\"></iframe>\"}]],\"markups\":[],\"sections\":[[10,0],[1,\"p\",[]]]}"
			tag_json = list()
			for tag in target_post.complete_tags.all():
				temp_dict = dict()
				temp_dict['id'] = tag.unique_id
				tag_json.append(temp_dict)
			try:
				for tag in target_post.Not_registered_tags.all():
					temp_dict = dict()
					temp_dict['name'] = tag.name
					temp_dict['url'] = tag.url
					tag_json.append(temp_dict)
					print("tag added in tags_json >>>>>",tag.name)
			except:

				print(">>>>>> No registered tag found from db >>>>>")
				pass

			print(tag_json)
			
			body = {
				'posts': [{'title': target_post.title,
						   "mobiledoc": mobiledoc,
						   "tags": tag_json,
						   "feature_image": target_post.feature_image
						   }
						  ]}
			#print(body)
			r = requests.post(url, json=body, headers=headers)
			checking_data = r.json()
			#print(checking_data)
			response_id = checking_data['posts'][0].get('id')
			response_uuid = checking_data['posts'][0].get('uuid')
			new_tags = checking_data['posts'][0]['tags']

			for check_id in new_tags:
				try:
					Tag_details.objects.get(unique_id = check_id['id'])
					pass
				except:
	                #print("link of image ", check_id['feature_image'])
					tag_to_table = Tag_details()
					tag_to_table.unique_id = check_id['id']
					tag_to_table.url = check_id['url']
					tag_to_table.name = check_id['name'].capitalize()
					tag_to_table.slug = slugify(check_id['name'])
					tag_to_table.created_at = check_id['created_at']
					tag_to_table.meta_title = check_id['meta_title']
					tag_to_table.updated_at = check_id['updated_at']
					tag_to_table.visibility = check_id['visibility']
					tag_to_table.description = check_id['description']
					tag_to_table.feature_image = check_id['feature_image']
					tag_to_table.meta_description = check_id['meta_description']
					tag_to_table.save()
					unregistered_obj = Unregister_tags.objects.get(name = check_id['name'].capitalize())
					target_post.Not_registered_tags.remove(unregistered_obj)
					unregistered_obj.delete()
					print("======  tag registration with addition in tag details completed ======== ")

			target_post.ghost_post_id = response_id
			target_post.ghost_post_uuid = response_uuid
			target_post.save()
			print("Total posts are ", len(all_syn_post))
			post.delete()
			print("post removed")
			print("Total remaining posts are ", len(All_post_sync.objects.all()))


@task()
def tag_updation():
	print(">>>>> This task should executed after 1 week")
	requests.get('http://127.0.0.1:8000/populate_tags_details')
