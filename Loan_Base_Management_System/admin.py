from django.contrib import admin
from .models import userInfo, committeeInfo1, Friend, committeeStore, RequestDetail, WinnerDetail, Transaction, Chat

# Register your models here.
admin.site.register(userInfo)
admin.site.register(committeeInfo1)
admin.site.register(Friend)
admin.site.register(committeeStore)
admin.site.register(RequestDetail)
admin.site.register(WinnerDetail)
admin.site.register(Transaction)
admin.site.register(Chat)
