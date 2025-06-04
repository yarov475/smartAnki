from smartanki.utils.web_scraper import scrape_webpage

def test_scrape_webpage_success():
    url = "https://en.wikipedia.org/wiki/Entropy"
    text = scrape_webpage(url)

    # Basic checks
    assert isinstance(text, str), "❌ scrape_webpage did not return a string"
    assert len(text) > 100, "❌ Scraped text is too short"
    assert "entropy" in text.lower(), "❌ Scraped text does not contain 'entropy'"
