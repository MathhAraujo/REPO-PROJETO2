from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm 
from django.core.exceptions import ValidationError

User = get_user_model()

class EditarDadosPessoaisForm(forms.Form):
    email = forms.EmailField(
        label="Novo Email",
        required=True, # O email em si é obrigatório, mas a alteração pode ser opcional na view
        widget=forms.EmailInput(attrs={'class': 'form-control-input', 'autocomplete': 'email'})
    )
    senha_atual = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'current-password'}),
        required=False, # Torna-se obrigatório na view se houver tentativa de mudar email ou senha
        strip=False
    )
    nova_senha1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'new-password'}),
        required=False, # Apenas se o usuário quiser mudar a senha
        strip=False,
        min_length=8, # Exemplo de validação
        help_text="Deixe em branco se não quiser alterar a senha. Mínimo de 8 caracteres."
    )
    nova_senha2 = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control-input', 'autocomplete': 'new-password'}),
        required=False, # Apenas se nova_senha1 for preenchida
        strip=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Passa o usuário para o formulário
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email # Preenche o email atual

    def clean_email(self):
        novo_email = self.cleaned_data.get('email').lower()
        if self.user and novo_email == self.user.email.lower(): # Se o email não mudou
            return novo_email # Nenhuma validação de unicidade necessária

        # Verifica se o novo email já está em uso por OUTRO usuário
        if User.objects.filter(email__iexact=novo_email).exists():
            raise forms.ValidationError("Este email já está em uso por outro usuário.")
        # Se o seu USERNAME_FIELD for 'email', a checagem acima já cobre.
        # Se for diferente, e o username também deve ser único e igual ao email:
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

    def clean(self): # Validação geral do formulário
        cleaned_data = super().clean()
        novo_email = cleaned_data.get('email')
        nova_senha1 = cleaned_data.get('nova_senha1')
        senha_atual_fornecida = cleaned_data.get('senha_atual')

        email_foi_alterado = self.user and novo_email and novo_email.lower() != self.user.email.lower()
        senha_foi_alterada = bool(nova_senha1) # Se o campo nova_senha1 foi preenchido

        if email_foi_alterado or senha_foi_alterada:
            if not senha_atual_fornecida:
                self.add_error('senha_atual', "Sua senha atual é obrigatória para salvar alterações no email ou na senha.")
            elif self.user and not self.user.check_password(senha_atual_fornecida):
                self.add_error('senha_atual', "Senha atual incorreta.")
        
        return cleaned_data