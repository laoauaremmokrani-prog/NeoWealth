import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import re

# Enhanced keywords for better economic news filtering
keywords = [
    # Economic indicators
    "interest rate", "inflation", "deflation", "GDP", "unemployment", "employment", "wages", "consumer price index",
    "producer price index", "retail sales", "housing market", "real estate", "mortgage rates",
    
    # Central banks & monetary policy
    "Federal Reserve", "FED", "ECB", "Bank of England", "Bank of Japan", "monetary policy", "quantitative easing",
    "tapering", "rate hike", "rate cut", "monetary tightening", "monetary easing",
    
    # Markets & finance
    "stock market", "bond market", "forex", "currency", "dollar", "euro", "yen", "yuan", "crypto", "bitcoin",
    "oil prices", "commodities", "gold", "silver", "energy prices", "gas prices",
    
    # Trade & geopolitics
    "trade war", "tariffs", "sanctions", "supply chain", "global trade", "imports", "exports", "trade deficit",
    "trade surplus", "BRICS", "G7", "G20", "WTO", "trade agreement",
    
    # Economic events
    "recession", "economic slowdown", "economic growth", "economic recovery", "economic crisis", "financial crisis",
    "banking crisis", "debt crisis", "sovereign debt", "default", "bankruptcy",
    
    # Regional economies
    "US economy", "Chinese economy", "European economy", "UK economy", "Japanese economy", "emerging markets",
    "developing countries", "global economy", "world economy",
    
    # Business & corporate
    "earnings", "revenue", "profit", "loss", "layoffs", "hiring", "merger", "acquisition", "IPO", "bankruptcy",
    "corporate earnings", "business confidence", "consumer confidence"
]

async def scrape_aljazeera():
    """Enhanced Al Jazeera news scraper with better data extraction"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set user agent to avoid blocking
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Set shorter timeout
        page.set_default_timeout(15000)
        
        # Scrape multiple news sections for comprehensive coverage
        news_data = []
        
        # Main news page
        try:
            await page.goto("https://www.aljazeera.com/news/", wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)
            
            # Extract articles from main news
            articles = await page.query_selector_all("article")
            print(f"Found {len(articles)} articles on main page")
            
            for article in articles[:20]:  # Get more articles
                try:
                    # Try multiple selectors for better coverage
                    headline_elem = await article.query_selector("h1, h2, h3, h4")
                    description_elem = await article.query_selector("p")
                    
                    if headline_elem and description_elem:
                        headline = (await headline_elem.inner_text()).strip()
                        description = (await description_elem.inner_text()).strip()
                        
                        # Check if article contains economic keywords
                        if any(keyword.lower() in headline.lower() or keyword.lower() in description.lower() 
                               for keyword in keywords):
                            
                            # Extract additional metadata
                            link_elem = await article.query_selector("a")
                            link = await link_elem.get_attribute("href") if link_elem else ""
                            if link and not link.startswith("http"):
                                link = f"https://www.aljazeera.com{link}"
                            
                            # Extract timestamp if available
                            time_elem = await article.query_selector("time, .date, .timestamp")
                            timestamp = await time_elem.get_attribute("datetime") if time_elem else ""
                            
                            # Extract category/tag if available
                            category_elem = await article.query_selector(".category, .tag, .section")
                            category = (await category_elem.inner_text()).strip() if category_elem else ""
                            
                            # Calculate relevance score based on keyword matches
                            relevance_score = sum(1 for keyword in keywords 
                                               if keyword.lower() in headline.lower() or keyword.lower() in description.lower())
                            
                            news_data.append({
                                "date": datetime.today().strftime("%Y-%m-%d"),
                                "timestamp": timestamp,
                                "headline": headline,
                                "description": description,
                                "category": category,
                                "link": link,
                                "relevance_score": relevance_score
                            })
                except Exception as e:
                    continue
        except Exception as e:
            print(f"Warning: Could not access main news page: {e}")
        
        # Also check business/economy section
        try:
            await page.goto("https://www.aljazeera.com/economy/", wait_until="domcontentloaded")
            await page.wait_for_timeout(1000)
            
            economy_articles = await page.query_selector_all("article")
            print(f"Found {len(economy_articles)} articles in economy section")
            
            for article in economy_articles[:15]:
                try:
                    headline_elem = await article.query_selector("h1, h2, h3, h4")
                    description_elem = await article.query_selector("p")
                    
                    if headline_elem and description_elem:
                        headline = (await headline_elem.inner_text()).strip()
                        description = (await description_elem.inner_text()).strip()
                        
                        # Extract metadata
                        link_elem = await article.query_selector("a")
                        link = await link_elem.get_attribute("href") if link_elem else ""
                        if link and not link.startswith("http"):
                            link = f"https://www.aljazeera.com{link}"
                        
                        time_elem = await article.query_selector("time, .date, .timestamp")
                        timestamp = await time_elem.get_attribute("datetime") if time_elem else ""
                        
                        category_elem = await article.query_selector(".category, .tag, .section")
                        category = (await category_elem.inner_text()).strip() if category_elem else ""
                        
                        relevance_score = sum(1 for keyword in keywords 
                                           if keyword.lower() in headline.lower() or keyword.lower() in description.lower())
                        
                        news_data.append({
                            "date": datetime.today().strftime("%Y-%m-%d"),
                            "timestamp": timestamp,
                            "headline": headline,
                            "description": description,
                            "category": category,
                            "link": link,
                            "relevance_score": relevance_score
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Warning: Could not access economy section: {e}")
        
        await browser.close()
        
        # Remove duplicates and sort by relevance
        if news_data:
            # Remove duplicates based on headline
            seen_headlines = set()
            unique_news = []
            for news in news_data:
                if news["headline"] not in seen_headlines:
                    seen_headlines.add(news["headline"])
                    unique_news.append(news)
            
            # Sort by relevance score (highest first)
            unique_news.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return unique_news
        return []

async def main():
    """Main function to run the enhanced scraper"""
    print("Starting Enhanced Al Jazeera Economic News Scraper...")
    print("Looking for economic indicators, market news, and policy updates...")
    
    news_data = await scrape_aljazeera()
    
    if not news_data:
        print("No relevant economic news found.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(news_data)
    
    # Save to CSV with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"aljazeera_economic_news_{timestamp}.csv"
    df.to_csv(filename, index=False)
    
    print(f"Enhanced news data saved to {filename}")
    print(f"Found {len(news_data)} relevant economic articles")
    
    # Display top articles by relevance
    print(f"\n{'='*80}")
    print("TOP ECONOMIC NEWS BY RELEVANCE")
    print(f"{'='*80}")
    
    for i, news in enumerate(news_data[:10], 1):  # Show top 10
        print(f"\n{i}. {news['headline']}")
        print(f"   {news['description'][:150]}{'...' if len(news['description']) > 150 else ''}")
        print(f"   Category: {news['category'] or 'General'}")
        print(f"   Relevance Score: {news['relevance_score']}")
        if news['link']:
            print(f"   Link: {news['link']}")
        print("   " + ("-" * 80))
    
    # Summary statistics
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS")
    print(f"{'='*80}")
    
    if 'category' in df.columns:
        category_counts = df['category'].value_counts()
        print("\nNews by Category:")
        for category, count in category_counts.head(5).items():
            print(f"   - {category or 'General'}: {count} articles")
    
    print(f"\nAverage Relevance Score: {df['relevance_score'].mean():.1f}")
    print(f"Highest Relevance Score: {df['relevance_score'].max()}")
    print(f"Total Articles Found: {len(news_data)}")
    
    print(f"\nEnhanced scraping complete! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
