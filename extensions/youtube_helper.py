def on_page_load(browser):
    url = browser.url().toString()
    if "youtube.com" not in url: return
    js = """
    setInterval(()=>{
        let skip = document.querySelector('.ytp-skip-ad-button');
        if(skip) skip.click();
        let video = document.querySelector('video');
        if(video) video.autoplay=false;
    },1000);
    """
    browser.page().runJavaScript(js)
