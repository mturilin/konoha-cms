from .models import Page
from coffin.shortcuts import render
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import redirect
import yaml
from konoha import KonohaError



def page(request, path):
    preview = request.GET.get('preview', 'false').lower()

    try:
        page = Page.objects.get(path=path)
    except Page.DoesNotExist:
        raise Http404(path)

    if not page.published:
        if (request.user.is_staff and preview != 'true') or not request.user.is_staff:
            raise Http404(path)

    if page.login_required and not request.user.is_authenticated():
        return redirect_to_login(page.full_path)

    try:
        version = int(request.GET['version'])
        data = page.version_data(version)
        if not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
    except KeyError:
        data = page.published_data

    data_dict = yaml.load(data)

    if not page.template:
        raise KonohaError("Page doesn't have template")

    return render(request,
                  page.template,
                  dictionary=data_dict,
                  content_type=page.content_type_with_charset)



