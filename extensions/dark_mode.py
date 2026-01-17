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

    // Observe DOM changes (catch dynamic content like SPAs)
    const observer = new MutationObserver(() => applyDarkMode());
    observer.observe(document.body, { childList: true, subtree: true });

    // Also re-apply every 2 seconds as a fallback
    setInterval(applyDarkMode, 2000);
    """
    browser.page().runJavaScript(js)
