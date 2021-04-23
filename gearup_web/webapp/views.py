import os
import sys
import requests
from django.views import View
from django.core.cache import cache

from django.conf import settings
from django.shortcuts import render
# from django.views.generic.detail import SingleObjectMixin

CACHE_TIME = 0


class BaseView(View):
    """
    common modules
    """

    context = {'api_url': settings.API_URL}

    def generate_jwt(self, request):
        url = settings.API_URL + 'api/token/'
        r = requests.post(url=url, data={'username': settings.SILENT_LOGIN_USERNAME,
                                         'password': settings.SILENT_LOGIN_PASSWORD})
        if r.status_code == 200 and 'access' in r.json():
            request.session['token'] = r.json()['access']

    def dispatch(self, request, *args, **kwargs):
        # cache_key = 'menu_list'
        # result = cache.get(cache_key)
        # if not result:
        try:
            result = ''
            url = settings.API_URL + 'api/menus/'
            headers = {"Authorization": "Bearer %s" % self.request.session['token']}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
            else:
                self.generate_jwt(request)
                headers = {"Authorization": "Bearer %s" % self.request.session['token']}
                result = requests.get(url, headers=headers).json()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))

        # cache.set(cache_key, result, CACHE_TIME)

        self.context['menu'] = result
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class HomePageView(BaseView):

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        cache_key = 'home_page'
        response = cache.get(cache_key)
        if not response:
            url = settings.API_URL + 'api/home_page/'
            headers = {"Authorization": "Bearer %s" % request.session['token']}
            response = requests.get(url, headers=headers).json()
        cache.set(cache_key, response, CACHE_TIME)
        self.context.update(response)
        return render(request, self.template_name, self.context)


class DisabilityAccessView(BaseView):

    template_name = "disability-access.html"

    def get(self, request, *args, **kwargs):
        self.context['api_token'] = self.request.session['token']
        return render(request, self.template_name, self.context)


class CustomPageView(BaseView):

    template_name = "custom_page.html"

    def get(self, request, page_uid, *args, **kwargs):
        cache_key = 'custom_page_%s' % page_uid
        response = cache.get(cache_key)
        if not response:
            url = settings.API_URL + 'api/pages/%s?web_view=true' % page_uid
            headers = {"Authorization": "Bearer %s" % request.session['token']}
            response = requests.get(url, headers=headers).json()
        cache.set(cache_key, response, CACHE_TIME)
        self.context.update(response)
        return render(request, self.template_name, self.context)


class NCCollegesView(BaseView):

    template_name = "nc-colleges.html"

    def get(self, request, *args, **kwargs):
        self.context['api_token'] = self.request.session['token']
        url = settings.API_URL + 'api/majors/'
        headers = {"Authorization": "Bearer %s" % request.session['token']}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self.context['majors'] = response.json()
        else:
            self.context['majors'] = []
        return render(request, self.template_name, self.context)


class CareersView(BaseView):

    template_name = "careers.html"

    def get(self, request, *args, **kwargs):
        self.context['api_token'] = self.request.session['token']
        return render(request, self.template_name, self.context)


class CollegeDetailView(BaseView):
    """docstring for  CollegeDetailView"""

    template_name = "college_detail.html"

    def get(self, request, college_uid, *args, **kwargs):
        cache_key = 'college_detail_%s' % college_uid
        response = cache.get(cache_key)
        if not response:
            url = settings.API_URL + 'api/colleges/%s?web_view=true' % college_uid
            headers = {"Authorization": "Bearer %s" % request.session['token']}
            response = requests.get(url, headers=headers).json()
        cache.set(cache_key, response, CACHE_TIME)
        self.context.update(response)
        return render(request, self.template_name, self.context)


class CareerDetailView(BaseView):
    """docstring for  CareerDetailView"""

    template_name = "career_detail.html"

    def get(self, request, career_uid, *args, **kwargs):
        cache_key = 'career_detail_%s' % career_uid
        response = cache.get(cache_key)
        if not response:
            url = settings.API_URL + 'api/careers/%s?web_view=true' % career_uid
            headers = {"Authorization": "Bearer %s" % request.session['token']}
            response = requests.get(url, headers=headers).json()
        cache.set(cache_key, response, CACHE_TIME)
        self.context.update(response)
        return render(request, self.template_name, self.context)
