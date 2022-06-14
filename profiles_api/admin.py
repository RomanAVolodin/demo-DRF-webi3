from django.contrib import admin

from profiles_api.models import UserProfile, ProfileFeedItem


admin.site.register(UserProfile)
admin.site.register(ProfileFeedItem)
