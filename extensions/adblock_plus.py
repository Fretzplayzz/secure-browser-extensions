def on_page_load(browser):
    js = """
    let blocked = ['doubleclick', 'googlesyndication', 'adsystem', 'tracker'];
    let elements = document.querySelectorAll('img, iframe, div');
    elements.forEach(el => {
        blocked.forEach(b => { if(el.src && el.src.includes(b)) el.style.display='none'; });
    });
    """
    browser.page().runJavaScript(js)

