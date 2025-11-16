from django import forms
from .models import ServiceRequest
from users.models import UserSkill


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ["offered_skill", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Descreva o que você precisa..."}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        qs = UserSkill.objects.select_related("user").all()
        if request and request.user.is_authenticated:
            qs = qs.exclude(user=request.user)
        self.fields["offered_skill"].queryset = qs
        self.fields["offered_skill"].label = "Serviço/Skill"
        self.fields["offered_skill"].help_text = "Escolha um serviço oferecido por um provedor"
