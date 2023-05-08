from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template


def getFotoPerfil(usuario):
  html = BeautifulSoup(
    urlopen('https://github.com/' + usuario).read(), "html5lib")
  lista = []
  for item in html.find_all('img'):
    lista.append(item['src'])

  imagem = list(
    filter(lambda k: 'https://avatars.githubusercontent.com/u' in k, lista))[0]
  return imagem


def getNomePerfil(usuario):
  html = BeautifulSoup(
    urlopen('https://github.com/' + usuario).read(), "html5lib")
  return html.find(itemprop='name').text.replace(' ', '').strip("\n")


def getNomeRepositorio(usuario):
  html = BeautifulSoup(
    urlopen('https://github.com/' + usuario + '?tab=repositories').read(),
    "html5lib")
  lista = []
  for link in html.find_all('a', {'itemprop': 'name codeRepository'}):
    repositorio = link.get_text().replace(' ', '').strip("\n")
    lista.append(repositorio)
  return lista


def getRepositorios(usuario):
  html = BeautifulSoup(
    urlopen('https://github.com/' + usuario + '?tab=repositories').read(),
    "html5lib")
  lista = []
  for link in html.find_all('a', {'itemprop': 'name codeRepository'}):
    repositorio = link.get_text().replace(' ', '').strip("\n")
    lista.append('https://github.com/' + usuario + '/' + repositorio)
  return lista


def geraHTML(foto, nome, repositorios, repoNome):
  html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    	<title>Meu currículo</title>
    	<meta charset="UTF-8">
    	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    	<style>
    		body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
  }}
  
  header {{
    background-color: #003366;
    color: #fff;
    padding: 20px;
    text-align: center;
  }}
  
  h1 {{
    margin: 0;
    font-size: 3rem;
    font-weight: bold;
  }}
  
  img {{
    border-radius: 50%;
    display: block;
    margin: 0 auto;
    max-width: 200px;
  }}
  
  section {{
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-top: 30px;
  }}
  
  h2 {{
    font-size: 2rem;
    margin-top: 1em;
  }}
  
  ul {{
    list-style-type: none;
    padding: 0;
    margin: 0;
  }}
  
  li {{
    margin-bottom: 0.5em;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  
  a {{
    color: #003366;
    text-decoration: none;
  }}
  
  a:hover {{
    text-decoration: underline;
  }}
  
  @media (max-width: 800px) {{
    h1 {{
      font-size: 2rem;
    }}
    img {{
      max-width: 150px;
    }}
    section {{
      max-width: 600px;
    }}
    h2 {{
      font-size: 1.5rem;
    }}
  }}
    	</style>
    </head>
    <body>
    	<header>
    		<img src="{foto}" alt="Foto de perfil">
    		<h1>{nome}</h1>
    	</header>
    	<section>
    		<h2>Repositórios do GitHub</h2>
    		<ul>
    """

  for i, repo in enumerate(repositorios):
    html += f"""\t\t\t<li><a href=\"{repo}\">{repoNome[i]}</a></li>\n"""

  html += """
        		</ul>
        	</section>
        </body>
        </html>
        """

  return html


app = Flask(__name__)


@app.route("/", defaults={'usuario': 'MatheusAvelar'})
@app.route("/<usuario>")
def home(usuario):
  foto = getFotoPerfil(usuario)
  nome = getNomePerfil(usuario)
  repositorios = getRepositorios(usuario)
  repoNome = getNomeRepositorio(usuario)
  html = geraHTML(foto, nome, repositorios, repoNome)
  return render_template("index.html", resume_html=html)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
