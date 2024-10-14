## InsScrapy: Instagram and TikTok Recipe Scraper
### Overview
InsScrapy is a web scraping project designed to extract recipe information from Instagram and TikTok posts. Utilizing httpx for scraping and spacy for natural language processing, this tool efficiently retrieves recipe names and ingredients.
### Features
- Scrape recipe information  from Instagram and TikTok posts
- Built with httpx for efficient web scraping
- Employs spacy's NLP capabilities for text analysis to extract recipe names and ingredients

Installation
To get started, follow these steps:
1. Install Required Python Modules
```bash
pip install -r requirements.txt
```

1. Download Spacy Language Model
```bash
python -m spacy download en_core_web_sm
```
Usage
Run the spider using:
```bash
python run.py
```
### Important Notes
Due to stricter TikTok's robust anti-bot mechanisms compared to Instagram, scraping may occasionally fail.
For commercial use with high traffic, consider integrating Scrapfly services to bypass anti-bot restrictions.
