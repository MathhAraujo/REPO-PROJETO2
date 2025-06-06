from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm 
from django.core.exceptions import ValidationError
from .models import DesempenhoMateria, Materia
from django.forms import modelformset_factory

User = get_user_model()

class EditarDadosPessoaisForm(forms.Form):
    email = forms.EmailField(
        label="Novo Email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control-input', 'autocomplete': 'email'})
    )
    senha_atual = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'current-password'}),
        required=False, 
        strip=False
    )
    nova_senha1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'new-password'}),
        required=False,
        strip=False,
        min_length=8,
        help_text="Deixe em branco se não quiser alterar a senha. Mínimo de 8 caracteres."
    )
    nova_senha2 = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'new-password'}),
        required=False,
        strip=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        novo_email = self.cleaned_data.get('email').lower()
        if self.user and novo_email == self.user.email.lower(): 
            return novo_email 

       
        if User.objects.filter(email__iexact=novo_email).exists():
            raise forms.ValidationError("Este email já está em uso por outro usuário.")
        
        if User.objects.filter(username__iexact=novo_email).exists():
            raise forms.ValidationError("Este email (como nome de usuário) já está em uso por outro usuário.")
        return novo_email

    def clean_nova_senha2(self):
        nova_senha1 = self.cleaned_data.get('nova_senha1')
        nova_senha2 = self.cleaned_data.get('nova_senha2')

        if nova_senha1 and not nova_senha2:
            raise forms.ValidationError("Por favor, confirme sua nova senha.")
        if nova_senha1 and nova_senha2 and nova_senha1 != nova_senha2:
            raise forms.ValidationError("As novas senhas não coincidem.")
        return nova_senha2

    def clean(self):
        cleaned_data = super().clean()
        novo_email = cleaned_data.get('email')
        nova_senha1 = cleaned_data.get('nova_senha1')
        senha_atual_fornecida = cleaned_data.get('senha_atual')

        email_foi_alterado = self.user and novo_email and novo_email.lower() != self.user.email.lower()
        senha_foi_alterada = bool(nova_senha1)
        if email_foi_alterado or senha_foi_alterada:
            if not senha_atual_fornecida:
                self.add_error('senha_atual', "Sua senha atual é obrigatória para salvar alterações no email ou na senha.")
            elif self.user and not self.user.check_password(senha_atual_fornecida):
                self.add_error('senha_atual', "Senha atual incorreta.")
        
        return cleaned_data

class DesempenhoMateriaForm(forms.ModelForm):
    class Meta:
        model = DesempenhoMateria
        fields = ['nota_qualitativa', 'faltas', 'observacoes']
        widgets = {
            'nota_qualitativa': forms.Select(attrs={'class': 'form-control-select'}),
            'faltas': forms.NumberInput(attrs={'class': 'form-control-input', 'min': '0'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control-textarea', 'rows': 3}),
        }
    
DesempenhoMateriaFormSet = modelformset_factory(
    DesempenhoMateria, 
    form=DesempenhoMateriaForm, 
    extra=0, 
    can_delete=False 
)