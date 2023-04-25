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
        my_file = request.FILES['arquivo']
        if form.is_valid():

            arquivo = form.cleaned_data['arquivo']
            nome_arquivo, extensao = os.path.splitext(arquivo.name)
            if extensao.lower() != '.c':
                print('aaaaaaaaaaaaaq')
                form.add_error('arquivo', 'Por favor, selecione um arquivo em C.')
            else:
                arquivo = form.save(commit=False)
                arquivo.save()
                print('salvou')
        else:
            print('not valid')
        arquivos = Arquivo.objects.filter()
       
        print('my', my_file)
        file_content = my_file.read().decode('utf-8')
        print('form', file_content)
        analisar_arquivo = Arquivo.analisar(my_file, file_content)
        print('n', analisar_arquivo)
        

            # self.form_invalid(form)  
            # if form.is_valid():
            #     arquivo = form.save(commit=False)
            #     arquivo.save()
            #     arquivo = form.cleaned_data['arquivo']
                
            #     arquivos = Arquivo.objects.filter()
            #     my_file = request.FILES['arquivo']
            #     print('form', my_file)

            #file_content = my_file.read().decode('utf-8')
            #     analisar_arquivo = Arquivo.analisar(my_file, file_content)
            #     print('n', analisar_arquivo)
            # # return redirect('analisador')

  



        # if form.is_valid():
        #     arquivo = form.save(commit=False)
        #     arquivo.save()

        #     return redirect('analisador')
        
        
        return render(request, self.template_name, {'form': form, 'file_content': my_file, 'analisar_arquivo': analisar_arquivo, 'arquivos': arquivos})

class DeletarArquivoView(View):
    def get(self, request, pk):
        obj = Arquivo.objects.get(pk=pk)
        os.remove(obj.arquivo.path)
        obj.delete()
        return redirect('analisador')