Projeto Econet
=======
[![Build Status](https://travis-ci.org/luanfonceca/econet.png?branch=master)](https://travis-ci.org/luanfonceca/econet)


Como Instalar e Configurar
===============
1. Clone ou Baixe esse repositório;
2. Entre na pasta do projeto, onde se encontra os códigos:
    - `$ cd econet/econet`
3. Certifique-se de já ter o Python, na versão ~2.7, instalado. Instale o [pip](http://www.pip-installer.org/en/latest/) ou [easy_install](http://pythonhosted.org/distribute/easy_install.html);
4. Instale as dependências do projeto;
    - `$ pip install -r requirements.txt`
5. Copie o `.sample`, para o seu:
    - `cp settings_local.py.sample settings_local.py`
6. Configure o `DATABASES`, dentro do arquivo [settings_local](https://github.com/luanfonceca/econet/blob/master/econet/settings_local.py.sample#L14) file.
7. Sincronize o seu banco, com os Models e as Aplicações externas:
    - ```python manage.py syncdb```
8. Migre as tabelas do seu banco, com os Models e as Aplicações externas:
    - ```python manage.py migrate```
9. Rode o seu projeto:
    - ```python manage.py runserver```
10. Veja ele rodando na `localhost`; 
    - ```127.0.0.1:8000```

- você pode mudar a  *porta* na qual o django rodará seu projeto: 
    - ```python manage.py runserver 8080``` --> ```127.0.0.1:8080```
