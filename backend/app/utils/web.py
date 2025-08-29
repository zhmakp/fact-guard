from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import logging
from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)


class WebScraper:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.converter =  DocumentConverter()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def convert_to_markdown(self, url: str) -> Optional[str]:
        """Convert webpage content to Markdown"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            markdown = md(response.content, strip=['a', 'img', 'script', 'style'])
            return str(markdown)
        except Exception as e:
            logger.error(f"Error converting {url} to Markdown: {str(e)}")
            return None

    async def convert_using_docling(self, url: str) -> Optional[str]:
        """Convert webpage content to Markdown using Docling"""
        try:
            doc = self.converter.convert(source=url)
            return str(doc.document.export_to_markdown())
        except Exception as e:
            logger.error(f"Error converting {url} to Markdown using Docling: {str(e)}")
            return None

    async def extract_text_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract text content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract title
            title = ""
            if soup.title:
                title = soup.title.string.strip() if soup.title.string else ""
            # Extract main content
            content = ""

            # Try to find main content areas
            content_selectors = [
                "div",
                "main",
                ".content",
                ".article-body",
                ".entry-content",
                ".post-content",
                ".story-body",
            ]

            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = " ".join(el.get_text(strip=True) for el in elements)
                    break

            # Fallback to body if no specific content area found
            if not content and soup.body:
                content = soup.body.get_text(strip=True)

            # Clean up the content
            content = self._clean_extracted_text(content)

            return {
                "url": url,
                "title": title,
                "content": content,
                "length": len(content),
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing content from {url}: {str(e)}")
            return None

    def _clean_extracted_text(self, text: str) -> str:
        """Clean extracted text content"""
        if not text:
            return ""

        # Remove excessive whitespace
        import re

        text = re.sub(r"\s+", " ", text)

        # Remove common navigation elements
        navigation_phrases = [
            "skip to main content",
            "menu",
            "search",
            "home",
            "about",
            "contact",
            "privacy policy",
            "terms of service",
            "cookie policy",
        ]

        text_lower = text.lower()
        for phrase in navigation_phrases:
            text_lower = text_lower.replace(phrase, "")

        return text.strip()

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return all([parsed.scheme, parsed.netloc])
        except:
            return False

    def extract_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return None


# Global web scraper instance
web_scraper = WebScraper()
