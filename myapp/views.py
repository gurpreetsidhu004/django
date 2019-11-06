import sys
# appending the path of another folder
# sys.path.insert(0,'/var/www/html/django_app.com/blog/myapp/nlp')
sys.path.insert(0,'/home/paradise/Desktop/worklog/2019/october/oct_11/blog_with_new_theme/myapp/')

from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string

from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from myapp.keras_ai_model import load_path, irrelevant_signs
from keras.models import load_model
from keras import backend as K

import urllib.parse as urlparse
import json, csv, os, urllib, re, time, requests
import numpy as np
import pandas as pd
import nltk, pickle
from keras.preprocessing.sequence import pad_sequences
from utils import postprocessing

import textract as textract
import PyPDF2
# nltk.download('stopwords')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer  # nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer

from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Data_record, Category, present_ghost_tags, Tag_details, \
 All_post_sync, Unregister_tags

import warnings, sys
from configparser import ConfigParser
# import this module to work with unslpash api
from unsplash_search import UnsplashSearch
# import cloudinary for storing cloud pdf files on cloud storage  
import cloudinary, time
import cloudinary.uploader
import cloudinary.api

import jwt
from datetime import datetime as date
from slugify import slugify
import slug

from .forms import BookForm
from myapp import forms

import pandas as pd
import schedule

######## here i created new login redirect  ############
settings.LOGIN_URL = "/"
global sheduling_list
sheduling_list = []

warnings.simplefilter(action='ignore', category=FutureWarning)
sys.setrecursionlimit(100000)
# Naming the variable
tfidf_vect = TfidfVectorizer()
UPLOAD_FOLDER = settings.MEDIA_ROOT
static_folder = settings.STATIC_DIR
current_path = os.getcwd()
# print("current_path is >>>>>", current_path)
config_file = os.path.join(current_path, 'config.ini')
# print("config file _path is >>>>>", config_file)
default_category_img_url = "https://images.unsplash.com/photo-1544847558-3ccacb31ee7f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"

config = ConfigParser()
try:
    config.read(config_file)
    print("=============  config file has been readed successfuly !!! ==============")
except:
    print(" Unable to read config.ini file ")

# Configure cloudinary credentials
cloudinary.config(
    cloud_name=config.get("CLOUDINARY", 'cloud_name'),
    api_key=config.get("CLOUDINARY", 'api_key'),
    api_secret=config.get("CLOUDINARY", 'api_secret'),
)

# create object which search with my api key
unsplash = UnsplashSearch(config.get("UNSPLASH", "api_key"))

# Ghost api key 

Ghost_key = config.get("GHOST", "api_key")
#print("this is ghost api key :",Ghost_key)


def SignUP(request):
    form = forms.RegisterForm()
    if request.method == 'POST':
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/signin')
        else:
            print(form.errors)
    return render(request,'registeration.html',{'form':form})

def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def Sign_in(request):
    if request.method == "POST":
        name = request.POST['un']
        pswd = request.POST['pwd']
        user = authenticate(username=name, password=pswd)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/blog/posts/')
        else:
            wrngpass=("Sorry!! You are not authenticated!!! please check your User Name And Password")
            return render(request,'login.html',{'wrngpass':wrngpass})
    return render(request,'login.html')


@login_required
def api_nlp_view(request):
    """
    This fucntuion read file extarct data using pypdf and pass to the nlp function.
    """
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        try:
            my_category = request.POST['category']
        except:
            my_category = None

        my_title = request.POST['doc_title']

        try:
            created_data_obj = cloudinary.uploader.upload(myfile,
                                      folder="my_folder/nlp_pdf/",
                                      public_id=f"{myfile.name.split('.')[0]}{(str(round(time.time())))[:3]}",
                                      overwrite=True,
                                      resource_type="raw"
                                                          )
            unsecure_url = created_data_obj.get('url')
            secure_url = created_data_obj.get('secure_url')
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> url is generated >>>>>>>>>>>>>>>>>>>>>>>.")
        
        except:

            return HttpResponse("<h3> Sorry we can't process this document due to file size max_value exceed </h3>")

        fs = FileSystemStorage(location=UPLOAD_FOLDER)  # defaults to   MEDIA_ROOT
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        # print("======= file_url is :==========", file_url)
        exact_url = UPLOAD_FOLDER + '/' + myfile.name
        pdf_file_read = open(exact_url, "rb")
        fileObject = pdf_file_read
        try:
            pdfFileReader = PyPDF2.PdfFileReader(fileObject, strict=False)
        except:
            pdfFileReader = PyPDF2.PdfFileReader(fileObject, strict=True)

        if pdfFileReader.isEncrypted:
            pdfFileReader.decrypt('')
        totalPageNumber = pdfFileReader.numPages
        currentPageNumber = 0
        text = ''
        while (currentPageNumber < totalPageNumber):
            pdfPage = pdfFileReader.getPage(currentPageNumber)
            text = text + pdfPage.extractText()
            currentPageNumber += 1
        #print(text)
        if (text == ''):
            text = textract.process(exact_url, method='tesseract', encoding='utf-8')
        try:
            final_text_file_name = open(UPLOAD_FOLDER + '/' + filename.split('.')[0] + ".txt", "wb+")
            # print("show the file please......", dir(final_text_file_name))
            final_text_file_name.write(text)
        except:
            final_text_file_name = open(UPLOAD_FOLDER + '/' + filename.split('.')[0] + ".txt", "w+")
            # print("show the file please......", dir(final_text_file_name))
            final_text_file_name.write(text)
        final_text_file_name.close()
        # print(">>>>>>>>>>DATA IS WRITTEN :>>>>>>>>>>>>",UPLOAD_FOLDER + '/'+filename.split('.')[0] + ".txt")
        all_keywords = text_file_processing(UPLOAD_FOLDER + '/' + filename.split('.')[0] + ".txt")

        total_keywords = [key for key in all_keywords.keys() if len(key) > 3]
        #print(len(total_keywords))
        #print(total_keywords)
        keywords_with_image_links = dict()
        img_count = 0
        for key_w in total_keywords:
            #print(key_w)
            if img_count == 5:
                break
            try:
                img = unsplash.search_photo(f"{my_category} {key_w}")
                keywords_with_image_links[key_w] = img.get('img')
                #print(img)
            # print(f"Keyword is {key_w} and its link is {img.get('img')}")
            except:
                pass
            img_count += 1 

        normalise_keywords = " ".join([key for key in all_keywords.keys() if len(key) > 3])
        print('>>>>>>>>>>>>>>>>>.uploaded keywords ',normalise_keywords)
        ######################################################################################
        all_obj = Category.objects.filter(name=my_category)
        if len(all_obj) == 0:
            enter_category_to_db = Category.objects.create(
                name=my_category)
            enter_category_to_db.save()

        else:
            print(f"============{my_category} :> category already present in the db ========")

        
        try:
            post_title = my_title
            post_title_img = unsplash.search_photo(post_title)
            post_title_img = post_title_img.get('img')
            #print(post_title_img)
        except:
            post_title_img = default_category_img_url

        entry_to_database = Data_record()
        entry_to_database.keywords_with_links = keywords_with_image_links
        entry_to_database.title = my_title
        entry_to_database.file_path = secure_url
        final_obj_id = Category.objects.get(name=my_category)
        entry_to_database.categories = final_obj_id
        entry_to_database.keywords = normalise_keywords
        entry_to_database.save()

        return redirect("posts")

        #     return HttpResponse("<h3> Sorry we can't process this document due to file size max_value exceed </h3>")
    else:
        return render(request, "upload.html")


@login_required
def all_post(request):
    """
    This post will show all existing post on front end using django built in 
    paginator function where user can limit number of posts
    """
    posts = Data_record.objects.all().order_by('-created_on')
    
    paginator = Paginator(posts, 9)
    #print("total posts are :",len(posts))

    try:
        page = request.GET.get('page', 1)
        page_post = paginator.page(page)

    except PageNotAnInteger:
        page_post = paginator.page(1)
    
    except EmptyPage:
        page_post = paginator.page(paginator.num_pages)
    
    context = {
        "posts": page_post,
    }

    return render(request, "blog_index.html", context)


@login_required
def blog_category(request, category):
    """
	This post will show filtered existing post on front end 
	"""
    try:
        posts = Data_record.objects.filter(
            categories__name__contains=category
        ).order_by(
            '-created_on'
        )
        print('lenght of category is :',len(posts))
        context = {
            "category": category,
            "posts": posts
        }
        if len(posts)==0:
            raise Exception
    except:
        raise Http404
    return render(request, "blog_category.html", context)


@login_required
def tag_filter(request, tag):
    """
    This function is used to filter posts according to tags
    """

    tag_filter_query = Tag_details.objects.get(name=tag)
    tag_posts = Data_record.objects.filter(complete_tags=tag_filter_query)
    context = {
            "category": tag,
            "posts": tag_posts
        }
    return render(request, "blog_category.html", context)


@login_required
def blog_detail(request, pk):
    """
    this function will diplay content of each blog using it's primary key

    """
    #print("================ inside blog_detail ============ ")
    post = Data_record.objects.filter(pk=pk)
    #print("total posts are :", len(post))
    #print(post[0])
    data_key = post[0].keywords_with_links.keys()
    data_url = post[0].keywords_with_links.values()
    context = {
        "post": post[0],
    }

    return render(request, "blog_detail.html", context)


def text_file_processing(file_path):
    """
    Keyword extraction using nlp code dony by Sanpreet singh
    """

    # print("file_path is.....", file_path)
    myfile = open(file_path, "r")
    data_file = myfile.read()
    # myfile.close()
    # print("my file....", data_file)
    lem = WordNetLemmatizer()
    stem = PorterStemmer()
    word = "inversely"

    stop_words = set(stopwords.words("english"))  ##Creating a list of custom stopwords
    new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown"]
    stop_words = stop_words.union(new_words)

    corpus = []
    # Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', str(data_file))

    # Convert to lowercase
    text = text.lower()

    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    ##Convert to list from string
    text = text.split()

    ##Stemming
    ps = PorterStemmer()  # Lemmatisation

    lem = WordNetLemmatizer()

    text = [lem.lemmatize(word) for word in text if not word in
                                                        stop_words]
    text = " ".join(text)

    corpus.append(text)
    # print(corpus)
    cv = CountVectorizer()
    X = cv.fit_transform(corpus)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)  # get feature names
    feature_names = cv.get_feature_names()

    # fetch document for which keywords needs to be extracted
    doc = " ".join(corpus)
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""

        # use only topn items from vector
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        # results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results  # sort the tf-idf vectors by descending order of scores

    sorted_items = sort_coo(tf_idf_vector.tocoo())  # extract only the top n; n here is 10

    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
    final_data = doc, keywords
    # print("here are keywords >>>>>>>>>>>>>", keywords)
    return keywords

@login_required
def send_to_ghost(request, pk):
    """
    This fuction is create post in Ghost cms from our django data using api
    """
    print("============ send to ghost is executed ============")
    id, secret = Ghost_key.split(':')

    # Prepare header and payload
    iat = int(date.now().timestamp())

    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/v2/admin/'
    }
    
    all_tags_database_current_obj = present_ghost_tags.objects.get()
    all_tags_database = all_tags_database_current_obj.all_tags
    token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
    current_obj = Data_record.objects.get(pk=pk)
    if current_obj.ghost_post_id != "Not reviewed yet":
        return HttpResponse("<h1> This post already posted on Ghost blog</h1>")
    #print("post found")
    tags_data = current_obj.keywords_with_links
    tags_data_from_db = all_tags_database
    present_tags_with_id = dict()
    for num in tags_data_from_db:
        present_tags_with_id[num['name'].lower()] = num['id']

    tag_json = list()
    for tag,values in tags_data.items():
        mydict = dict()
        mydict['name'] = tag.capitalize()
        mydict['slug'] = slugify(tag)
        mydict['visibility'] = "public"
        mydict['feature_image'] = values
        mydict['url'] = "https://knowzone.ghostzones.ml/tag/{}".format(tag)
        tag_json.append(mydict)

    backup_dict_data = tag_json
    for index,tag_d in enumerate(tag_json):
        tag_name = tag_d['name'].lower()
        if tag_name in present_tags_with_id:
            tag_json[index].clear()
            tag_json[index] = dict()
            tag_json[index]['id'] = present_tags_with_id[tag_name]
            tag_json[index]['name'] = tag_name
    
    try:
        post_title = current_obj.title
        post_title_img = unsplash.search_photo(post_title)
        post_title_img = post_title_img.get('img')
    except:
        post_title = current_obj.categories
        post_title_img = unsplash.search_photo(post_title).get('img')

    post_pdf_link = current_obj.file_path
    url = 'https://knowzone.ghostzones.ml/ghost/api/v2/admin/posts/'
    headers = {'Authorization': 'Ghost {}'.format(token.decode())}
    mobiledoc_url = post_pdf_link
    mobiledoc = "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[[\"html\",{\"html\":\"<iframe src=\\\""+ mobiledoc_url+ "\\\" width=\\\"100%\\\" height=\\\"1000\\\" frameborder=\\\"0\\\" scrolling=\\\"no\\\"></iframe>\"}]],\"markups\":[],\"sections\":[[10,0],[1,\"p\",[]]]}"
    body = {
        'posts': [{'title': post_title,
                   "mobiledoc": mobiledoc,
                  "tags": tag_json,
                  "feature_image": post_title_img
                  }
            ]}

    r = requests.post(url, json=body, headers=headers)
    checking_data = r.json()
    print(checking_data)
    response_id = checking_data['posts'][0].get('id')
    response_uuid = checking_data['posts'][0].get('uuid')
    new_tags = checking_data['posts'][0]['tags']

    all_tags_id  = [check_tag['id'] for check_tag in all_tags_database]
    for check_id in new_tags:

        #print("obtained tags results ",check_id)

        if check_id['id'] in all_tags_id:
            pass
        else:
            try:
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
            except:
                pass
            all_tags_database.append(check_id)
            
    current_tag_obj = present_ghost_tags.objects.get()
    current_tag_obj.all_tags = all_tags_database
    current_tag_obj.save()

    for tag_name in new_tags:
        #print(tag_name['id'], tag_name['name'])
        # print("tag name >>>>>>>>>>>>>>>>>>>>>>>>>>>>", tag_name)
        # print(tag_name['id'])
        Get_tag_object = Tag_details.objects.get(unique_id=tag_name['id'])
        current_obj.complete_tags.add(Get_tag_object)
        #print(tag_name['name'], "is added in db")

    current_obj.feature_image = post_title_img
    current_obj.iframe = True
    current_obj.ghost_post_id = response_id
    current_obj.ghost_post_uuid = response_uuid

    current_obj.save()

    return HttpResponse("<h1> Data has been posted on Ghost blog</h1>")


def refresh_image(request):
    """
    Here I use ajax to refresh image form an unsplash api
    """
    my_key = request.GET.get('key', None)
    my_post_id = request.GET.get('post_key', None)
    my_default_url = request.GET.get('default_url', None)
    try:
        change_img = unsplash.search_photo(my_key)
        refreshed_url= change_img.get('img')
    except:
        refreshed_url = my_default_url

    current_obj = Data_record.objects.get(pk=my_post_id)
    tag_details = current_obj.keywords_with_links
    changed_tag_with_url = {my_key: refreshed_url}
    tag_details.update(changed_tag_with_url)
    current_obj.keywords_with_links.update(tag_details)
    current_obj.save()
    data =dict()
    data['response_message'] = ' new image has been found ',
    data['img_url'] = refreshed_url,
    data['img_key'] = "img-{}".format(my_key)
    return  JsonResponse(data)

# <<<<<<<<<<<<<<<<<<<<< table post edit using ajax with modal >>>>>>>>>>>>>>>>>>>

@login_required
def book_list(request):
    """
    This function use to display all post data in datatable 
    """
    books = Data_record.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def save_book_form(request, form, template_name):
    """
    This function is used to proccess book_create and book_update and reflect changes in db
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Data_record.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def book_create(request):
    """
    This function used on edit table page where user can crete post details using ajax
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'books/includes/partial_book_create.html')


@login_required
def book_update(request, pk):
    """
    This function used on edit table page where user can update post details using ajax
    """
    book = get_object_or_404(Data_record, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_update.html')


@login_required
def book_delete(request, pk):
    """
    This function used on edit table page where user can delete post using ajax
    """
    book = get_object_or_404(Data_record, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Data_record.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<< END of Edit functions >>>>>>>>>>>>>>>>>>>>>>>>>
def populate_tags_details(request):
    """
    This function use to fetch all tags form ghost cms and store them with all essential details
    in our Django database
    """
    print("this function is working inside the Populate tags ")
    try:
        tag_obj = present_ghost_tags.objects.get()
        tag_obj.delete()
        print('previous tags are deleted')
        raise Exception
    except:
        print('inside the exception')
        id, secret = Ghost_key.split(':')
        iat = int(date.now().timestamp())

        header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
        payload = {
            'iat': iat,
            'exp': iat + 5 * 60,
            'aud': '/v2/admin/'
        }

        token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
        url = 'https://knowzone.ghostzones.ml/ghost/api/v2/admin/tags/?limit=all'
        headers = {'Authorization': 'Ghost {}'.format(token.decode())}

        tags_hit_data = requests.get(url, headers=headers)
        tags_hit_data = tags_hit_data.json()
        tags_data = tags_hit_data['tags']
        tags_meta_details = tags_hit_data['meta']

        all_tags_obj = present_ghost_tags.objects.create(
                                                        all_tags=tags_data,
                                                        hit_details= tags_meta_details
                                                        )
        # data saved
        all_tags_obj.save()
        # now fetch data from db and populate  Tag_details table
        tag_obj = present_ghost_tags.objects.get()
        for current_tag in tag_obj.all_tags:
            #print(current_tag)
            try:
                # tag details saved here
                my_tag_details = Tag_details()
                my_tag_details.unique_id = current_tag.get('id')
                my_tag_details.url = current_tag.get('url')
                my_tag_details.name = current_tag.get('name').capitalize()
                my_tag_details.slug = current_tag.get('slug')
                my_tag_details.created_at = current_tag.get('created_at')
                my_tag_details.meta_title = current_tag.get('meta_title')
                my_tag_details.updated_at = current_tag.get('updated_at')
                my_tag_details.visibility = current_tag.get('visibility')
                my_tag_details.description = current_tag.get('description')
                my_tag_details.feature_image = current_tag.get('feature_image')
                my_tag_details.meta_description = current_tag.get('meta_description')
                my_tag_details.save()
                print("new_tags are saved")
            except:
                pass
        print("tags are updated")
        return redirect("posts")
    return redirect("posts")

@login_required
def excel_2_db(request):
    """
    This function take input as excel sheet and populate database
    """
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            my_df = pd.read_excel(myfile)
            for num in range(len(my_df)):
                try:
                    my_dict = Data_record()
                    if pd.isnull(my_df.loc[num]['title']):
                        raise Exception
                    #print("===== AFTER ========")
                    print("before work  ")
                    my_dict.title = my_df.loc[num]['title']
                    # print("title found")
                    #mobiledoc_url = my_df.loc[num]['mobiledoc']
                    #my_dict.mobiledoc = "{\"version\":\"0.3.1\",\"atoms\":[],\"cards\":[[\"html\",{\"html\":\"<iframe src=\\\""+ mobiledoc_url+ "\\\" width=\\\"100%\\\" height=\\\"1000\\\" frameborder=\\\"0\\\" scrolling=\\\"no\\\"></iframe>\"}]],\"markups\":[],\"sections\":[[10,0],[1,\"p\",[]]]}"
                    my_dict.file_path = my_df.loc[num]['mobiledoc']
                    my_dict.mobiledoc = my_df.loc[num]['mobiledoc']
                    my_dict.feature_image = my_df.loc[num]['feature_image']
                    my_dict.excel_uploaded = True
                    # if pd.isnull(my_df.loc[num]['Tags']):
                    #     raise Exception
                    my_dict.iframe = True if my_df.loc[num]['iframe'] ==1.0 else False
                    my_dict.save()
                    #print("done 1")
                    try:
                        all_tags_excel = my_df.loc[num]['Tags'].split(',')
                        #print(all_tags_excel)
                        for tag in all_tags_excel:
                            tag = tag.lower().strip()
                            try:
                                present_tag_details = Tag_details.objects.get(name=tag)
                                print(f"============{tag}============tag found in db")
                                my_dict.complete_tags.add(present_tag_details)
                                my_dict.save()
                                #print("done 2")
                            except:
                                print(">>>>>>>>>>>>>>>>>>>>>inside the except")
                                print(">>>>>>>>>>>>>>>>>>>>>", tag.capitalize())
                                # Here i save not saved tag details
                                current_tag_details = Unregister_tags() 
                                current_tag_details.name = tag.capitalize()
                                print(slugify(tag))
                                current_tag_details.url = "knowzone.ghostzones.ml/tag/{}/".format(slugify(tag))
                                print('after url ')
                                current_tag_details.save()
                                print('after saving')
                                ###################### adding relationship ##################
                                print(">>>>>>>>>>>>>>>>...",tag.capitalize())
                                temp_unregiter_tags = Unregister_tags.objects.get(name = tag.capitalize()) 
                                print(">>>>>>>>>>>>>>>Tag found from unregistered_records")
                                my_dict.Not_registered_tags.add(temp_unregiter_tags)    
                                print("=== Non registered tags are added in seprate table ==== ")
                                my_dict.save()
                                print("============= all done ===============")

                    except:
                        pass
                    #print(num)     
                    my_dict.save()
                    #print("done 3")
                
                except:
                    pass
            return redirect("posts")

    except NameError:
        return HttpResponse("<h2>please upload a valid xlsx file</h2>")

    except KeyError:
        return HttpResponse("<h2>please upload a valid xlsx file</h2>")

    except TypeError:
        return HttpResponse("<h2>please upload a valid xlsx file</h2>")

    return render(request,'excel_upload.html')

@login_required
def ai_model(request):
    """
    In this function Our Ai model take some text as input and predict tags 
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_path = os.getcwd()
    myapp_path = (os.path.join(BASE_DIR,'myapp'))

    if request.method == "POST":
        real_document = request.POST['my_text']
        load_model_path = load_path()
        keras_model = load_model(load_model_path)
        preprocessed_text = irrelevant_signs(real_document)
        # print(preprocessed_text)
        # step 2.1: tokenize the string using nltk.word_tokenize(string)
        real_document_tokenize = nltk.word_tokenize(preprocessed_text.lower())
        
        dictionary = os.path.join(myapp_path, 'dictionary')
        open_dictionary = open(dictionary, 'rb')
        # exit()
        string_to_object_deserialize = pickle.load(open_dictionary)
        # print(dir(string_to_object_deserialize))
        list_dict=dict()
        list_dict['topic']= real_document_tokenize
        real_document_tokenize_values = list_dict.values()
      
        # step 2.4: preparing the actual data
        test_data = string_to_object_deserialize.texts_to_sequences(real_document_tokenize_values)

        # step 2.5: converting list into numpy array
        max_document_length= 7000
        test_x = np.asarray(pad_sequences(test_data, maxlen=max_document_length, padding='post', truncating='post'))
        # exit()
        # step 3: predicting using trained keras model
        # K.clear_session()
        output_prediction = keras_model.predict(x=test_x, verbose=1)
        K.clear_session()

        # step 4: converting 3-d array into 2-d array using mp.argmax
        obtained_tokens = postprocessing.undo_sequential(output_prediction)

        # step 5: use obtained tokens and tokenize string to get the top words

        obtained_words_top = postprocessing.get_words(list_dict, obtained_tokens) 
        # print(obtained_words_top)
        clean_words = postprocessing.get_valid_patterns(obtained_words_top)

        # Getting more rectified words from each list
        values=list()
        for id_, each_value in clean_words.items():
            for each_inner_value in each_value:
                if len(each_inner_value)> 1:
                    each_inner_value_1=[value for value in each_inner_value if len(value)>3]
                    values.append(each_inner_value_1)
                else:
                    values.append(each_inner_value)                     
        # print("value is.....", values)
        values= values[:9]
        my_tags = {key:value for key, value in enumerate(values)}

        context_data = {
            "all_tags":my_tags.values()
        }

        return render(request, "index.html", context_data)
    return render(request, "index.html")

@login_required
def send_all_post_2_ghost(request):
    """
    This function will filter all the excel uploaded posts that are not uploaded and save in another table
    using ORM table name is "All_post_sync"
    """
    print("=========================  all post data is running  ======================")
    unregistered_records = Data_record.objects.filter(excel_uploaded=True).filter(ghost_post_id="Not reviewed yet")
    for post in unregistered_records:
        save_in_db = All_post_sync()
        save_in_db.record =  Data_record.objects.get(id=post.id)
        save_in_db.save()  

    return redirect("posts")

    # ====================== Ghost api start from here ========================#

    #return HttpResponse('WORking')