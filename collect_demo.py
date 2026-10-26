"""Exemplo Playwright restrito ao quadro fictício servido em localhost."""
import argparse
from pathlib import Path
from urllib.parse import urlparse

def collect(url:str,output:Path):
    parsed=urlparse(url)
    if parsed.scheme!='http' or parsed.hostname not in {'localhost','127.0.0.1','::1'}:
        raise ValueError('O exemplo aceita somente HTTP local; nunca um quadro profissional.')
    from playwright.sync_api import sync_playwright
    output.parent.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as runner:
        browser=runner.chromium.launch()
        try:
            page=browser.new_page();page.goto(url)
            page.get_by_role('heading',name='Quadro fictício de materiais',exact=True).wait_for()
            with page.expect_download() as waiting:
                page.get_by_role('link',name='Exportar quadro fictício para Excel',exact=True).click()
            waiting.value.save_as(str(output))
        finally:browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/board.html')
    parser.add_argument('--saida',type=Path,default=Path('demo_output/exportacao_coletada.xlsx'))
    args=parser.parse_args();collect(args.url,args.saida)
