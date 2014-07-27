import wikipedia
from flask import Flask, request, redirect
from creoleparser import text2html
from yahoo.search.news import NewsSearch
from url_shortener import UrlShortener
from threading import Lock
import sys
import duckduckgo
from duckduckgo import Result
from duckduckgo import query as Q
reload(sys)
lock = Lock()
THREADS = 20
sys.setdefaultencoding("utf-8")
app = Flask(__name__)
@app.route('/<query>')
def wsearch(query, methods=['POST', 'GET']):
    try:
        print query
        head = str(query)
        style = '''<head>
        <link rel="stylesheet" type="text/css" href="wiki.css">
        </head>'''
        title = "<title>{0}</title>".format(str(head))
        result = Q(query)
        uri = result.abstract.url
        page = wikipedia.page(title=query)
        content = text2html(page.content)
        for elem in page.links:
            refrence = "<a href=http://localhost:5000/{0}><center><br>{0}</center></body></a>".format(elem)
            summary = "<body><center>{0}</center></body>".format(content)
            us = UrlShortener()
            url = UrlShortener.shorten(us, page.url)
            home = str("/")
            re = "<br><center><a href={0}>Home</a></center>".format(home)
            body = "<br><center><a href={0}>Random</a></center>".format(str('{success:'))
            link = "<br><center><a href={0}>WikiPage</a></center>".format(uri)
            wiki = str(style + title + "\n" + "<br>"+ summary + "\n" + body + "\n" + link + re + refrence + "<center>" + "</center>")
    except wikipedia.DisambiguationError:
        print "\n"
        try:
            head = wikipedia.random(pages=1)
            style = '''<head>
            <link rel="stylesheet" type="text/css" href="wiki.css">
            </head>'''
            title = "<title>{0}</title>".format(str(head))
            page = wikipedia.page(title=head)
            content = text2html(page.content)
            result = duckduckgo.query(head)
            uri = result.abstract.url
            summ = wikipedia.summary(str(head))
            summary = "<body><center><div class='page'>{0}</div><center><body>".format(content)
            for elem in page.links:
                refrence = "<a href=http://localhost:5000/{0}><center><br>{0}</center></body></a>".format(elem)
                us = UrlShortener()
                url = UrlShortener.shorten(us, page.url)
                home = str("/")
                re = "<br><a href={0}>Home</a>".format(home)
                body = "<br><a href={0}>Random</a>".format(str('{success:'))
                link = "<br><a href={0}>WikiPage</a>".format(uri)
                wiki = str(style + title + "\n" + summary + "\n" + body + "\n" + link + re + refrence)
                return wiki
        except wikipedia.DisambiguationError, UnicodeEncodeError:
            head = wikipedia.random(pages=1)
            style = '''<head>
            <link rel="stylesheet" type="text/css" href="wiki.css">
            </head>'''
            title = "<title>{0}</title>".format(str(head))
            page = wikipedia.page(title=head)
            content = text2html(page.content)
            result = duckduckgo.query(head)
            uri = result.abstract.url
            summ = wikipedia.summary(str(head))
            summary = "<body><center><div class='page'>{0}</div><center><body>".format(content)
            for elem in page.links:
                refrence = "<a href=http://localhost:5000/" + elem + "><center><br>{0}</center></body></a>".format(elem)
                us = UrlShortener()
                url = UrlShortener.shorten(us, page.url)
                home = str("/")
                re = "<br><a href={0}>Home</a>".format(home)
                body = "<br><a href={0}>Random</a>".format(str('{success:'))
                link = "<br><a href={0}>WikiPage</a>".format(uri)
                wiki = str(style + title + "\n" + summary + "\n" + body + "\n" + link + refrence)
    return wiki
@app.route('/', methods=['GET', 'POST'])
def index():
    return '''
    <title>Wiki Rest API</title>
    <link rel="stylesheet" type="text/css" href="wiki.css">
    <body>

    <b><center>Welcome to WikiRest Api</center></b>
    <b><center>About <a href="/wiki">Wiki</a></center></b>
    <b><center>Random Page <a href="/'{success':'">Random</a>
    <script>
    function makeid()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
    document.cookie=makeid();
    </script>
    </body>
    '''

if __name__ == "__main__":
    try:
        app.run()
    except UnicodeEncodeError:
       print "\n"