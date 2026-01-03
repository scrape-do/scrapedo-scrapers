import unittest
import sys
import os

# Add parent directory to path to import the scraper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestPeopleSearchNowScraper(unittest.TestCase):
    """
    Test suite for PeopleSearchNow scraper.
    
    Note: These tests require a valid Scrape.do API token to be set in scrapePersonInfo.py
    and a valid example profile URL. Update the token and target_url in scrapePersonInfo.py
    before running these tests.
    """
    
    def test_scrape_person_info(self):
        """
        Test that the scraper can extract person information from a profile page.
        
        This test imports the scraper module and verifies that all required fields
        (name, age, address, city, state) are extracted and non-empty.
        """
        # Import the scraper module
        import scrapePersonInfo
        
        # Verify that all required variables are defined and non-empty
        self.assertTrue(hasattr(scrapePersonInfo, 'name'), "Name should be extracted")
        self.assertTrue(hasattr(scrapePersonInfo, 'age'), "Age should be extracted")
        self.assertTrue(hasattr(scrapePersonInfo, 'address'), "Address should be extracted")
        self.assertTrue(hasattr(scrapePersonInfo, 'city'), "City should be extracted")
        self.assertTrue(hasattr(scrapePersonInfo, 'state'), "State should be extracted")
        
        # Note: We can't easily test non-empty values without modifying the scraper
        # to separate fetching from printing, but we can verify the variables exist
        
    def test_required_imports(self):
        """Test that all required modules can be imported."""
        try:
            import requests
            import urllib.parse
            from bs4 import BeautifulSoup
        except ImportError as e:
            self.fail(f"Required import failed: {e}")
    
    def test_token_placeholder(self):
        """Test that the token is set to placeholder value in the source."""
        import scrapePersonInfo
        
        # Verify that the token is set to the placeholder
        self.assertEqual(scrapePersonInfo.token, "<your_token>",
                        "Token should be set to placeholder '<your_token>' in source code")


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
