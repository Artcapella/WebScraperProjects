import requests
from bs4 import BeautifulSoup

def get_average_scores(search_query):
    url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.com/"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.HTTPError as e:
        print(f"Failed to fetch search results: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    scores = []
    for result in results[:3]:  # Extracting scores from top 3 results
        score_element = result.find('span', class_='a-icon-alt')
        if score_element:
            score = float(score_element.text.split()[0])
            scores.append(score)

    if not scores:
        print("No scores found in the top 3 results.")
        return None

    average_score = sum(scores) / len(scores)
    return average_score

def get_top_rated_product(search_query):
    url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    headers = {
        # Mimicks a chrome browser to avoid being blocked by Amazon
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        # Add Accept-Language header to specify language preference
        "Accept-Language": "en-US,en;q=0.5",
        # Add Accept-Encoding header to handle compressed responses
        "Accept-Encoding": "gzip, deflate, br",
        # Add Referer header to simulate a request from the Amazon website, bypassing Amazon blocking
        "Referer": "https://www.amazon.com/"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.HTTPError as e:
        print(f"Failed to fetch search results: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    top_product = None
    top_score = 0
    for result in results:  # Extracting scores from top 3 results
        score_element = result.find('span', class_='a-icon-alt')
        if score_element:
            score = float(score_element.text.split()[0])
            if score > top_score:
                top_score = score
                top_product = result

    if not top_product:
        print("No top-rated product found.")
        return None

    product_name = top_product.find('span', class_='a-text-normal').text
    product_price = top_product.find('span', class_='a-price').text
    return product_name, product_price

if __name__ == "__main__":
    search_query = input("Enter your Amazon search query: ")
    average_score = get_average_scores(search_query)
    top_product = get_top_rated_product(search_query)
    if average_score:
        print(f"Average score of the top 3 results for '{search_query}': {average_score}")
        print(f"Top-rated product for '{search_query}': {top_product[0]} - Price: {top_product[1]}")
        