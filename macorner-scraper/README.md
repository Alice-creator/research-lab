# Macorner Review Scraper

A Python tool for scraping customer reviews from Macorner products via the Judge.me API. This scraper extracts detailed review data including ratings, review text, customer photos, and reviewer information, then saves it to CSV format for analysis.

## Features

- 🔍 **Product Review Extraction**: Scrapes reviews for any Macorner product URL
- 📊 **Structured Data Output**: Exports reviews to CSV with standardized fields
- 🖼️ **Image URL Collection**: Captures customer-uploaded review photos
- ✅ **Data Validation**: Uses Pydantic models for robust data handling
- 🔄 **Batch Processing**: Interactive mode for processing multiple products
- 🛡️ **Error Handling**: Graceful handling of network errors and invalid URLs

## Project Structure

```
macorner_scraper/
├── main.py           # Main application entry point
├── review.py         # Pydantic model for review data
├── constants.py      # Configuration and environment variables
├── requirements.txt  # Python dependencies
├── reviews.csv       # Output file (auto-generated)
├── .env             # Environment configuration (not tracked)
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:Alice-creator/Macorner-scraper.git
   cd macorner_scraper
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

## Usage

1. **Run the scraper**:
   ```bash
   python main.py
   ```

2. **Input product URLs**:
   - Enter a Macorner product URL when prompted
   - Example: `https://macorner.co/products/personalized-acrylic-ornament`
   - Enter `q` or press Enter without input to quit

3. **Output**:
   - Reviews are automatically saved to `reviews.csv`
   - Each run appends new reviews to the existing file

## Data Fields

The scraper extracts the following information for each review:

| Field | Description |
|-------|-------------|
| `title` | Review title/headline |
| `rating` | Star rating (1-5) |
| `body` | Full review text |
| `review_date` | Date in DD/MM/YYYY format |
| `reviewer_name` | Customer name |
| `product_url` | Original product URL |
| `picture_urls` | Customer-uploaded images (pipe-separated) |
| `product_id` | Shopify product ID |

## Dependencies

- **requests**: HTTP client for API calls
- **pydantic**: Data validation and modeling
- **python-dotenv**: Environment variable management
- **typing-extensions**: Enhanced type hints

## Configuration

The scraper uses environment variables for configuration:

- `REVIEW_PRODUCT_URL_TEMPLATE`: Judge.me API endpoint template
- `CSV_PATH`: Output file path for reviews

## Error Handling

The application handles various error scenarios:

- **Network errors**: Connection timeouts, HTTP errors
- **Invalid URLs**: Non-product URLs or malformed links
- **Missing data**: Products without reviews
- **API changes**: Graceful handling of JSON structure changes

## Example Output

Sample CSV data structure:
```csv
title,rating,body,review_date,reviewer_name,product_url,picture_urls,product_id
"Perfect Gift",5,"Love this ornament!",15/09/2025,"Shannon","https://macorner.co/products/...",https://image1.jpg | https://image2.jpg,8303014772892
```

## Development

### Code Structure

- **`main.py`**: Application entry point with interactive CLI
- **`review.py`**: Pydantic model defining review data structure
- **`constants.py`**: Configuration management and environment loading

### Key Functions

- `Review.from_judgeme()`: Maps Judge.me API response to Review model
- `write_reviews_csv()`: Handles CSV output with proper formatting
- Error handling for network requests and data validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Legal Notice

This tool is for educational and research purposes. Ensure you comply with:
- Macorner's Terms of Service
- Judge.me's API usage policies
- Rate limiting and respectful scraping practices

## License

[Add your license information here]

## Support

For issues or questions:
- Create an issue in the repository
- Check existing issues for similar problems
- Provide detailed error messages and steps to reproduce