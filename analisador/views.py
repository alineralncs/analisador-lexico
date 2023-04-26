from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from .forms import ArquivoForm
from .models import Arquivo
import os
# Create your views here.
class FormView(FormView):
    template_name = 'index.html'
    form_class = ArquivoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        arquivos = Arquivo.objects.all()
        return render(request, self.template_name, {'form': form, 'arquivos': arquivos})

    # def form_valid(self, form):
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponseBadRequest("Dados inválidos.")
        
        arquivo = form.cleaned_data['arquivo']
        nome_arquivo, extensao = os.path.splitext(arquivo.name)

        if extensao.lower() != '.c':
            form.add_error('arquivo', 'Por favor, selecione um arquivo em C.')
            return render(request, self.template_name, {'form': form})
        arquivo = form.save(commit=False)
        arquivo.save()



        my_file = request.FILES['arquivo']
    
        file_content = ''
        for chunk in my_file.chunks():
            file_content += chunk.decode('utf-8')
    
        if len(file_content) == 0:
            print('Arquivo vazio')
        else:
            print('Conteúdo:', file_content)
        analisar_arquivo = Arquivo.analyse(file_content)
       # print('analisar', analisar_arquivo)

        arquivos = Arquivo.objects.filter()
        
        return render(request, self.template_name, {'form': form, 'file_content': file_content, 'analisar_arquivo': analisar_arquivo, 'arquivos': arquivos})

class DeletarArquivoView(View):
    def get(self, request, pk):
        obj = Arquivo.objects.get(pk=pk)
        os.remove(obj.arquivo.path)
        obj.delete()
        return redirect('analisador')