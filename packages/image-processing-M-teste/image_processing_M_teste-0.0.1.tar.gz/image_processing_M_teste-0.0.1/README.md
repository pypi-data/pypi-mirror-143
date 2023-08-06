# Pacote de Processamento de Imagens
Autora: Karina Kato


Aula: Descomplicando a Criação de Pacotes de Processamento de Imagens em Python

Description. 

O pacote "image_processing" é usado para:

Módulo "Processing":

-> Correspondência de histograma;

-> Similaridade estrutural;

-> Redimensionar imagem;

Módulo "Utils":

-> Ler imagem;

-> Salvar imagem;

-> Plotar imagem;

-> Resultado do gráfico;

-> Plotar histograma;

## Installation

Passo a passo da configuração para hospedar um pacote em Python no ambiente de testes Test Pypi

 Instalação das últimas versões de "setuptools" e "wheel"

    py -m pip install --user --upgrade setuptools wheel
 Tenha certeza que o diretório no terminal seja o mesmo do arquivo "setup.py"

    C:\Users\Marcelo\PycharmProjects\pacote-de-processamento-de-imagens> py setup.py sdist bdist_wheel

 Após completar a instalação, verifique se as pastas abaixo foram adicionadas ao projeto:

 build;

 dist;

 image_processing_test.egg-info.

Basta subir os arquivos, usando o Twine, para o Test Pypi:

    py -m twine upload --repository testpypi dist/*

## Usage

```python
from image_processing_M_teste.processing import combination

combination.my_function()
```

## Author (quem hospedou o projeto no Test Pypi)
Marcelo Mandler

## License
[MIT](https://choosealicense.com/licenses/mit/)