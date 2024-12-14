# Airbnb Listings Scraper

This repository contains a Python script designed to scrape detailed information from Airbnb listings. The script leverages Selenium with `undetected_chromedriver` to bypass bot detection mechanisms and includes functionality to extract various listing details, including reviews, amenities, and images.

---

## Features

1. **Dynamic Interaction**:
   - Handles dynamic elements such as "Show more" buttons, scrolling, and pagination.

2. **Modular Design**:
   - Each scraping task (e.g., amenities, reviews) is encapsulated in a dedicated method for better organization and reusability.

3. **Robust Error Handling**:
   - Includes exception handling to ensure the script continues running even if errors occur on specific pages or elements.

4. **Extensive Data Extraction**:
   - Scrapes the following details:
     - Listing Title
     - Address
     - Number of Reviews
     - Amenities
     - Images
     - Description
     - Features

5. **Scalability**:
   - Built with features like dynamic timeouts and configurable scrolling limits to handle diverse page structures.

---

## Prerequisites

### Python Libraries:
- Python 3.8+
- Selenium
- undetected-chromedriver
- pandas

Install the dependencies using:
```bash
pip install selenium undetected-chromedriver pandas
```

### Browser Driver:
- Ensure you have Chrome installed.
- Download the appropriate version of the ChromeDriver from [ChromeDriver](https://sites.google.com/chromium.org/driver/).

---

## Setup and Usage

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo-name/airbnb-scraper.git
cd AirBnbListingsData
```

### 2. Run the Script
Edit the script to include your desired Airbnb URL(s) and execute:
```bash
python AirBnbListingsData.py
```

### 3. Output
The extracted data is stored in a Python dictionary (`main_data`). You can save it to a CSV or JSON file using built-in or third-party libraries like `pandas`.

Example:
```python
import pandas as pd
pd.DataFrame([main_data]).to_csv("airbnb_data.csv", index=False)
```

---

## Script Overview

### 1. **Initialization**
- The script initializes the Selenium WebDriver using `undetected_chromedriver` to avoid detection.
- Configures timeouts and browser options for efficient scraping.

### 2. **Scraping Details**
- **Title and Address:** Extracted using XPath selectors tailored to the Airbnb page structure.
- **Reviews:** Handles pagination and dynamic loading to collect all reviews.
- **Amenities:** Expands hidden sections to fetch all available amenities.
- **Images:** Retrieves all image URLs for the listing.

### 3. **Dynamic Page Handling**
- Scrolls through pages and sections to ensure all content is loaded before extraction.
- Uses `WebDriverWait` for dynamic wait conditions.

### 4. **Error Handling**
- Implements try-except blocks to handle transient issues like missing elements or timeout errors.

---

## Configuration Options

### Customizable Parameters:
- **Scroll Count:** Adjust the number of scrolls for image or review sections.
- **Timeouts:** Modify implicit and explicit wait times for element loading.
- **Headless Mode:** Enable headless mode for faster scraping by uncommenting:
  ```python
  chrome_options.add_argument("--headless")
  ```

---

## Known Limitations

1. **Layout Changes:**
   - The script relies on specific XPath selectors that may break if Airbnb updates its website layout.

2. **Rate Limits:**
   - Extensive scraping may trigger bot detection. To mitigate this:
     - Use a rotating proxy service.
     - Reduce scraping speed with delays between requests.

3. **Incomplete Data:**
   - Listings with incomplete or hidden data may result in partially filled output.

---

## Future Enhancements

1. **Proxy Integration:**
   - Add support for rotating proxies to bypass rate limits and geographic restrictions.

2. **Concurrency:**
   - Implement multithreading or multiprocessing for faster scraping of multiple listings.

3. **Data Export:**
   - Enhance output functionality to support saving directly to databases or cloud storage.

4. **Config File:**
   - Externalize XPaths and configurations for better maintainability.

---

## Author

**Anwaar Mirza**
- Data Mining and Web Scraping Expert
- [LinkedIn](https://www.linkedin.com/in/anwaar-mirza-895825288/)
- [GitHub](https://github.com/anwaar-mirza)

For inquiries or custom scraping projects, please reach out!

