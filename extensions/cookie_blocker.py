def on_page_load(browser):
    js = """
    document.cookie.split(';').forEach(c=>{
        document.cookie = c.split('=')[0] + '=;expires=Thu,01 Jan 1970 00:00:00 UTC;path=/;';
    });
    """
    browser.page().runJavaScript(js)
