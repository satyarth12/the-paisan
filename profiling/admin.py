from django.contrib import admin
from profiling.models.profile import Profile
from profiling.models.referral import ReferralSystem
from profiling.models.report import ReportCategory, Report
from profiling.models.block import Block


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age')


@admin.register(ReferralSystem)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'referred_by', 'invites')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reported_by", "reported_on", "category")

    def reported_by(self, obj):
        return obj.user

    def reported_on(self, obj):
        return str(obj.content_object)

    def category(self, obj):
        return obj.category


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("blocked_by", "blocked_user", "created_at")

    def blocked_by(self, obj):
        return obj.user

    def blocked_user(self, obj):
        return obj.user_2

    def created_at(self, obj):
        return obj.created_at.date()


admin.site.register(ReportCategory)
