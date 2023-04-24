from django.urls import path
from analisador.views import FormView
from .views import FormView, DeletarArquivoView

urlpatterns = [
        path('arquivos', FormView.as_view(), name='analisador'),
        path('arquivos/<int:pk>/deletar/', DeletarArquivoView.as_view(), name='deletar_arquivo')
]