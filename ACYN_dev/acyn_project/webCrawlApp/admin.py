from django.contrib import admin

from .models import TestData, NaverWebtoon, NaverWebnovel, DaumWebtoon, Netflix

# Register your models here.
admin.site.register(TestData)

admin.site.register(NaverWebtoon)
admin.site.register(NaverWebnovel)
admin.site.register(DaumWebtoon)
admin.site.register(Netflix)