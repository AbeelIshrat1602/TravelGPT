from langchain_community.tools import DuckDuckGoSearchResults
from crewai.tools import tool

@tool
def search_web_tool(query: str):
    """
    Searches the web for the provided query and returns relevant results.
    Args:
        query: The search query string
    Returns:
        Search results as a string
    """
    search_tool = DuckDuckGoSearchResults(num_results=10, verbose=True) 
    return search_tool.run(query)

# Adding web_search_tool as an alias to search_web_tool for compatibility
@tool
def web_search_tool(query: str):
    """
    An alias for search_web_tool. Searches the web for the provided query.
    Args:
        query: The search query string
    Returns:
        Search results as a string
    """
    return search_web_tool(query)

# If you need the ScrapeWebsiteTool functionality, here's a simpler implementation
@tool
def scrape_website_tool(url: str):
    """
    Extracts the main content from a website URL.
    Args:
        url: The website URL to scrape
    Returns:
        The extracted content as text
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract main content (paragraphs)
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text().strip() for p in paragraphs])
        
        # Truncate if too long
        if len(content) > 8000:
            content = content[:8000] + "... (content truncated)"
        
        return content
    except Exception as e:
        return f"Error scraping website: {str(e)}"