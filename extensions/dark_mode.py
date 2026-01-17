def on_page_load(browser):
    js = """
    function applyDarkMode() {
        if (document.getElementById('dark-mode-style')) return;
        let s = document.createElement('style');
        s.id = 'dark-mode-style';
        s.innerHTML = `
            html { filter: invert(1) hue-rotate(180deg) !important; }
            img, video { filter: invert(1) hue-rotate(180deg) !important; }
        `;
        document.head.appendChild(s);
    }
    applyDarkMode();
    // Re-apply every second to catch dynamic content
    setInterval(applyDarkMode, 1000);
    """
    browser.page().runJavaScript(js)
