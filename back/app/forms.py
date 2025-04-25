from os import getenv

from annotated_types.test_cases import cases
from django import forms

from .core.core.prompt import Prompt
from .core.core.yandex_gpt_client import YandexGPTClient
from .models import News, TestQuestion


class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        category = cleaned_data.get('category')
        
        # Если это статья, проверяем, что категория соответствует
        if content_type == 'article' and category != 'article':
            # Автоматически устанавливаем категорию 'article' для статей
            cleaned_data['category'] = 'article'
        
        return cleaned_data


class CreateTaskForm(forms.Form):
    selected_task = forms.CharField(widget=forms.Textarea)

    def exec(self):
        prompt = Prompt()
        selected_task = self.cleaned_data.get('selected_task')
        method = f"get_{selected_task.replace('-', '_')}_prompt"

        task_text = YandexGPTClient(
            token=getenv('OAUTH_TOKEN'),
            folder_id=getenv('FOLDER_ID')
        ).get_prompt_response_msg(
            text=getattr(prompt, method)
        )
        return {
            'task_text': task_text,
            'selected_task': selected_task
        }


class AddTaskToBaseForm(forms.Form):
    SUCCESS_MSG: str = "Задание успешно добавлено в базу данных!"
    ERROR_MSG: str = "Произошла ошибка: {error}!"

    task_text = forms.CharField(widget=forms.Textarea)
    task_answer = forms.CharField(widget=forms.Textarea)
    selected_task_answer = forms.CharField(widget=forms.Textarea)

    def mapping_tests(self, value: str) -> int:
        if value == 'task-one':
            return 1
        if value == 'task-two':
            return 2
        if value == 'task-three':
            return 3
        if value == 'task-four':
            return 4
        if value == 'task-five':
            return 5
        if value == 'task-six':
            return 6
        if value == 'task-seven':
            return 7
        if value == 'task-eighth':
            return 8
        if value == 'task-nine':
            return 9
        if value == 'task-ten':
            return 10
        if value == 'task-eleven':
            return 11
        if value == 'task-twelve':
            return 12

    def exec(self):
        task_text = self.cleaned_data.get('task_text')
        task_answer = self.cleaned_data.get('task_answer')
        selected_task_answer = self.cleaned_data.get('selected_task_answer')
        try:
            TestQuestion.objects.create(
                test_id=self.mapping_tests(selected_task_answer),
                answer=task_answer,
                question_text=task_text
            )
        except Exception as e:
            msg = self.ERROR_MSG.format(error=str(e))
        else:
            msg = self.SUCCESS_MSG
        return {'info_msg': msg}
