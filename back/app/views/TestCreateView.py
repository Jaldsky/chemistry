
from typing import NoReturn

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from os import getenv
import random

from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

# from app.base.views_base import ViewBase
# from app.core.prompt import Prompt
# from app.core.yandex_gpt_client import YandexGPTClient
# from app.forms import UserRegistrationForm, LoginForm, CreateTaskForm
# from app.models import Roles


class ViewBase(View):
    METHOD_NOT_ALLOWED_ERROR: str = 'Method Not Allowed'
    PROHIBITED_METHODS: tuple = ()

    def __getattr__(self, method_name: str) -> JsonResponse | NoReturn:
        if method_name in self.PROHIBITED_METHODS:
            return lambda request: JsonResponse({'error': self.METHOD_NOT_ALLOWED_ERROR}, status=405)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{method_name}'")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TestCreateView(ViewBase):
    PROHIBITED_METHODS: tuple = ('put', 'patch', 'delete')
    template_name = 'tests/test_create.html'

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('')

        # if request.user.role not in (Roles.ADMIN, Roles.TEACHER):
        #     return HttpResponseForbidden()

        return render(request, self.template_name)

    # @staticmethod
    # def post(request):
    #     pass
        # if not request.user.is_authenticated:
        #     return redirect('/login/')

        # if request.user.role not in (Roles.ADMIN, Roles.TEACHER):
        #     return HttpResponseForbidden()
        #
        # form = CreateTaskForm(request.POST)
        # if not form.is_valid():
        #     raise Exception

        # context = {
        #     'form': form.create_task_with_prompt(),
        # }
        # return render(request, 'tests/test_create.html', context)
        # return render(request, 'tests/test_create.html', context)