def on_page_load(browser):
    js = """
    let s = document.createElement('style');
    s.innerHTML = `
      html { filter: invert(1) hue-rotate(180deg); }
      img, video { filter: invert(1) hue-rotate(180deg); }
    `;
    document.head.appendChild(s);
    """
    browser.page().runJavaScript(js)
