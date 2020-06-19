from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class register(forms.Form):
    username = forms.CharField(
        error_messages={
            "required": "不能为空"
        },
        widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"})
    )
    cname = forms.CharField(
        error_messages={
            "required": "不能为空"
        },
        widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入中文名"})
    )
    email = forms.EmailField(
        widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "输入邮箱"})
    )
    soft = forms.MultipleChoiceField(
        choices=(
            (1, "confluence"),
            (2, "jira"),
            (3, "gitlab"),
        ),
        initial=[1, 3],
        widget=forms.CheckboxSelectMultiple(
        ),
    )