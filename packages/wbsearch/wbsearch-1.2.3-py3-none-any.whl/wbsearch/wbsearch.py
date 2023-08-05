import webbrowser
import click
import KvK
from pathlib import Path

@click.command()
@click.argument('argument', required=True)
@click.option('--set', '-s', help='Set keywords to access your links', required=False)
def search(argument, set):
    path = Path(__file__).parent
    dataBase = KvK.KvK(f'{path}/dataBase.kvk')
    if set != None:
        try:
            var = dataBase.get(set)
        except:
            dataBase.addClass(set)
            dataBase.addAttr(className=set, attrName='link', attrContent=argument)
        else:
            if var != None:
                dataBase.editAttr(className=set, oldAttrName='link', newAttrName='link', attrContent=argument)
            else:
                dataBase.addClass(set)
                dataBase.addAttr(className=set, attrName='link', attrContent=argument)
    else:
        try:
            var = dataBase.get(argument)
        except:
            pass
        else:
            if var != None:
                argument = dataBase.get('link', className=argument)
        try:
            argument.index('http://')
        except:
            try:
                argument.index('https://')
            except:
                argument = argument.replace(' ', '+')
                webbrowser.open(f'https://www.google.com/search?q={argument}')
            else:
                webbrowser.open(argument)
        else:
            webbrowser.open(argument)