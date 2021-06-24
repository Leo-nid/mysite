from django.contrib import admin
from .models import Post, Comment
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from .views import upload_file

class PostAdmin(admin.ModelAdmin):
    change_list_template = "admin/monitor_change_list.html"
    list_display = ['view_title']

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        custom_urls = [
            url('^import/$', upload_file, name='process_import'),
            url('^export/$', self.export_as_json, name='process_export'),]
        return custom_urls + urls

    @admin.display(empty_value='???')
    def view_title(self, obj):
        return obj.post_text[:10] # first 10 symbols of text

    def export_as_json(self, request):
        data = Post.objects.all()
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=DownloadedText.json'
        serializers.serialize("json", data, stream=response)
        return response

    def import_from_json(self, request):

        return HttpResponseRedirect("../")


class CommentAdmin(admin.ModelAdmin):
    change_list_template = "admin/monitor_change_list.html"
    list_display = ['view_title']

    def get_urls(self):
        urls = super(CommentAdmin, self).get_urls()
        custom_urls = [
            url('^import/$', upload_file, name='process_import'),
            url('^export/$', self.export_as_json, name='process_export'),]
        return custom_urls + urls

    @admin.display(empty_value='???')
    def view_title(self, obj):
        return obj.comment_text[:10]

    def export_as_json(self, request):
        data = Comment.objects.all()
        response = HttpResponse(content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=DownloadedText.json'
        serializers.serialize("json", data, stream=response)
        return response

    def import_from_json(self, request):
        Post.objects.all().delete()
        it = serializers.deserialize("json", request.body)
        it.save()
        return HttpResponseRedirect("../")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)