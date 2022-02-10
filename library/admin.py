from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from . models import *
admin.site.register(Signup)
admin.site.register(Userhistory)
admin.site.register(Book)

class IssuebookAdmin(SimpleHistoryAdmin):
    list_display=['id','bookname','studentname','issuedate','expirydate']
    history_list_display = ['bookname','studentname','issuedate','expirydate']
admin.site.register(Issuebook, IssuebookAdmin)

class RequestbookAdmin(SimpleHistoryAdmin):
    list_display = ['id','bookname','user_name','setlimit','requestdate']
    history_list_display = ['id','bookname','user_name','setlimit','requestdate']
admin.site.register(Requestbook, RequestbookAdmin)
