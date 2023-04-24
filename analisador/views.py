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

    def form_valid(self, form):
        arquivo = form.cleaned_data['arquivo']
        nome_arquivo, extensao = os.path.splitext(arquivo.name)
        if extensao.lower() != '.c':
            form.add_error('arquivo', 'Por favor, selecione um arquivo em C.')
            return self.form_invalid(form)  
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.save()
            return redirect('analisador')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        arquivos = Arquivo.objects.all()
        my_file = request.FILES['arquivo']
        print('form', my_file)

        file_content = my_file.read().decode('utf-8')
        analisar_arquivo = Arquivo.analisar(my_file, file_content)

        # if form.is_valid():
        #     arquivo = form.save(commit=False)
        #     arquivo.save()

        #     return redirect('analisador')
        
        print('arquivos', arquivos)
        return render(request, self.template_name, {'form': form, 
        'file_content': my_file, 'analisar_arquivo': analisar_arquivo, 'arquivos': arquivos})

class DeletarArquivoView(View):
    def get(self, request, pk):
        obj = Arquivo.objects.get(pk=pk)
        os.remove(obj.arquivo.path)
        obj.delete()
        return redirect('analisador')