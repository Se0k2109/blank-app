from playwright.sync_api import sync_playwright
import json

URL = 'https://z-one.kr/university/naesin/practical'
TARGETS = ['가천대학교', '상명대학교']


def find_img_by_text(page, name):
    # Try to find an element that contains the university name and return the first image src within
    return page.evaluate(
        """(name) => {
            function safeSrc(img){ if(!img) return null; return img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || null }
            // find elements whose visible text contains the name
            const nodes = Array.from(document.querySelectorAll('body *'))
                .filter(n => n.childElementCount > 0 || (n.innerText && n.innerText.trim().length>0));
            let found = nodes.find(e => (e.innerText || '').includes(name));
            if(!found) return null;
            // try to find img inside
            let img = found.querySelector('img');
            if(img) return safeSrc(img);
            // walk up and look for img siblings/parents
            let parent = found.parentElement;
            while(parent){
                img = parent.querySelector('img');
                if(img) return safeSrc(img);
                parent = parent.parentElement;
            }
            return null;
        }""",
        name,
    )


def collect_all_images(page):
    return page.evaluate("() => Array.from(document.querySelectorAll('img')).map(i => i.src || i.getAttribute('data-src') || i.getAttribute('data-lazy-src') || '').filter(Boolean)")


def main():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(URL, wait_until='networkidle', timeout=60000)

        for t in TARGETS:
            results[t] = find_img_by_text(page, t)

        results['_all_imgs'] = collect_all_images(page)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        browser.close()


if __name__ == '__main__':
    main()
