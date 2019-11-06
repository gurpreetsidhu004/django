from django.contrib import admin

# Register your models here.
from myapp.models import Data_record, Category, present_ghost_tags,\
  Tag_details, All_post_sync,Unregister_tags #Keywords_record,

class PostAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class Present_ghost_tags(admin.ModelAdmin):
    pass

class All_post_Admin(admin.ModelAdmin):
    pass

class Tag_detailsAdmin(admin.ModelAdmin):
    pass

class UnregisterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Data_record, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(present_ghost_tags, Present_ghost_tags)
admin.site.register(All_post_sync, All_post_Admin)
admin.site.register(Tag_details, Tag_detailsAdmin)
admin.site.register(Unregister_tags, UnregisterAdmin)