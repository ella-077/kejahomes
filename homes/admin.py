from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from .models import Apartment, ApartmentImage, ApartmentApplication, ApplicationDocument


# 🔥 Inline for multiple apartment images
class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 3


# 🔥 Apartment Admin
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'contact', 'preview_images']
    inlines = [ApartmentImageInline]

    def preview_images(self, obj):
        images = obj.images.all()[:3]
        if not images:
            return "No Images"

        # Only call format_html if we have at least one image
        html = "".join(
            '<img src="{}" style="width:60px;height:50px;object-fit:cover;margin-right:5px;border-radius:5px;" />'.format(img.image.url)
            for img in images
        )
        return format_html("{}", html)


# 🔥 Inline for application documents
class ApplicationDocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0


# 🔥 Apartment Application Admin
@admin.register(ApartmentApplication)
class ApartmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'apartment', 'status', 'submitted_at', 'approved_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'apartment', 'email')
    inlines = [ApplicationDocumentInline]
    actions = ['approve_applications']

    def approve_applications(self, request, queryset):
        for app in queryset:
            app.status = 'approved'
            app.approved_at = timezone.now()
            app.price = 20000  # you can customize later
            app.payment_info = "Mpesa Paybill: 123456, Account: yourname"
            app.save()

        self.message_user(request, f"{queryset.count()} application(s) approved!")

    approve_applications.short_description = "Approve selected applications"