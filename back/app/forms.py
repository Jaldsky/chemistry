from os import getenv

from django import forms

from .core.core.prompt import Prompt
from .core.core.yandex_gpt_client import YandexGPTClient
from .models import News

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

    task_text = forms.CharField(widget=forms.Textarea)

    def exec(self):
        msg = self.SUCCESS_MSG

        return {'info_msg': msg}
