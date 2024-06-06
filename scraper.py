from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import re

def scrape_jumia(query):
    print("----------SCRAPING JUMIA----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.jumia.ma/catalog/?q=" + query)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".prd._fb.col.c-prd"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 8:  # Stop after 8 products because 9th always not found
            break
        try:
            title_element = product.find_element(By.CSS_SELECTOR, "a.core")
            title = title_element.get_attribute("data-ga4-item_name")
            url = title_element.get_attribute("href")

            # Check if the product is out of stock
            try:
                out_of_stock_element = product.find_element(By.CLASS_NAME, "product-card__badge--outOfStock")
                if out_of_stock_element:
                    print(f"Product {index + 1} is out of stock.")
                    continue
            except NoSuchElementException:
                # If the out-of-stock element is not found, continue as usual
                pass

            # Wait for the price element to load
            try:
                price_element = WebDriverWait(product, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".prc"))
                )
                price_text = price_element.text.strip()
                # Split the price text by hyphen and pick the second part
                price_parts = price_text.split('-')
                if len(price_parts) > 1:
                    price_text = price_parts[1].strip()  # Get the second part and trim whitespace
                else:
                    price_text = price_parts[0].strip()  # If there's only one part, use it
                price = float(re.sub(r'[^\d.]', '', price_text))
            except (NoSuchElementException, TimeoutException):
                # If price cannot be found, skip this product
                print(f"Price not found for product {index + 1}.")
                continue

            # Scrape image URL
            image_element = product.find_element(By.CSS_SELECTOR, "img.img")
            image_url = image_element.get_attribute("data-src") if image_element else None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results




def scrape_electroplanet(query):
    print("----------SCRAPING ELECTROPLANET----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.electroplanet.ma/recherche?q=" + query)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.item.product.product-item"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            # Check if the product is out of stock
            try:
                out_of_stock_element = product.find_element(By.CSS_SELECTOR, "span[title='Epuisé']")
                print(f"Product {index + 1} is out of stock.")
                continue
            except NoSuchElementException:
                pass

            title_element = product.find_element(By.CSS_SELECTOR, "a.product-item-link")
            title = title_element.text
            url = title_element.get_attribute("href")

            # Extract the current price (special price if on sale, regular price otherwise)
            try:
                price_element = product.find_element(By.CSS_SELECTOR, ".price-box-special .special-price .price")
                price_text = price_element.text.strip()
            except NoSuchElementException:
                price_element = product.find_element(By.CSS_SELECTOR, ".price-box .price")
                price_text = price_element.text.strip()

            # Remove spaces and convert to float
            price_text = re.sub(r'\s+', '', price_text)
            price = float(price_text.replace('.', '').replace(',', '.'))

            try:
                image_element = product.find_element(By.CSS_SELECTOR, "img.product-image-photo")
                image_url = image_element.get_attribute("src")

                # Check for alternative attributes if the image URL is a placeholder
                if "data:image" in image_url:
                    image_url = image_element.get_attribute("data-src") or image_element.get_attribute("data-lazy")
            except:
                image_url = None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found: {e}")
            continue

    driver.quit()
    return results




def scrape_virgin(query):
    print("----------SCRAPING VIRGIN----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://virginmegastore.ma")

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "autocomplete-0-input"))
        )
        search_box.send_keys(query)
        search_box.submit()

        is_product_page = "boutique" not in driver.current_url
        results = []

        if is_product_page:
            try:
                # Check for out-of-stock text within the "add-to-cart" button (existing code)

                title_element = driver.find_element(By.CSS_SELECTOR, "a.text-base.font-bold")
                title = title_element.text.strip()
                url = driver.current_url

                try:
                    # Target the parent element containing the sale price
                    sale_element = driver.find_element(By.CSS_SELECTOR, ".product-onsale")       #STILL EXTRACTING OLD PRICE
                    # Get the last child element with the price value within the sale section
                    price_element = sale_element.find_element(By.CSS_SELECTOR, ".price__value:last-child")
                    price_text = price_element.find_element(By.CSS_SELECTOR, ".price__number").text.strip()
                except NoSuchElementException:
                    # Fallback to the first price element (consider adding logic for regular price)
                    try:
                        price_element = driver.find_element(By.CSS_SELECTOR, ".price__value .price__number")
                        price_text = price_element.text.strip()
                    except NoSuchElementException:
                        print("Price element not found on product page")
                        price_text = "N/A"

                price = float(re.sub(r'[^\d,]', '', price_text).replace('.', '').replace(',', '.')) if price_text else None

                # Image extraction (existing logic with comment)
                try:
                    image_element = driver.find_element(By.CSS_SELECTOR, "img.w-full.object-contain")
                    image_url = image_element.get_attribute("src")
                except NoSuchElementException:
                    print("Image element not found on product page")
                    image_url = None

                # You could potentially explore using alternative image selectors or searching within the product details
                # if "img.w-full.object-contain" is not reliable.

                results.append({"title": title, "url": url, "price": price, "image_url": image_url})

            except Exception as e:
                print(f"An error occurred while scraping the product page: {e}")

        else:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.product")))
            products = driver.find_elements(By.CSS_SELECTOR, "li.product")
            for index, product in enumerate(products):                              #not tested yet
                if index >= 10:  # Stop after 10 products
                    break
                try:
                    # Out-of-stock check within the loop (optional)
                    # ... (similar logic as above for product page)

                    title_element = product.find_element(By.CSS_SELECTOR, "a.text-base.font-bold")
                    title = title_element.text.strip()
                    url = title_element.get_attribute("href")

                    try:
                        # Target the parent element containing the sale price
                        sale_element = driver.find_element(By.CSS_SELECTOR, ".product-onsale")         #STILL EXTRACTING OLD PRICE
                        # Get the last child element with the price value within the sale section
                        price_element = sale_element.find_element(By.CSS_SELECTOR, ".price__value:last-child")
                        price_text = price_element.find_element(By.CSS_SELECTOR, ".price__number").text.strip()
                    except NoSuchElementException:
                        # Fallback to the first price element (consider adding logic for regular price)
                        try:
                            price_element = driver.find_element(By.CSS_SELECTOR, ".price__value .price__number")
                            price_text = price_element.text.strip()
                        except NoSuchElementException:
                            print("Price element not found on product page")
                            price_text = None

                    price = float(re.sub(r'[^\d,]', '', price_text).replace('.', '').replace(',', '.')) if price_text else "N/A"

                    # Image extraction (existing logic with comment)
                    try:
                        image_element = product.find_element(By.CSS_SELECTOR, "img.w-full.object-contain")
                    except NoSuchElementException:
                        try:
                            image_element = product.find_element(By.CSS_SELECTOR, "img")
                        except NoSuchElementException:
                            image_element = None

                    image_url = image_element.get_attribute("src") if image_element else None

                    price_text = ""
                    try:
                        price_element = product.find_element(By.CSS_SELECTOR, ".price__number")
                        price_text = price_element.text.strip()
                    except NoSuchElementException:
                        print(f"Price element not found for product: {url}")

                    price = float(re.sub(r'[^\d,]', '', price_text).replace('.', '').replace(',', '.')) if price_text else None

                    result = {"title": title, "url": url, "price": price, "image_url": image_url}
                    results.append(result)
                    print(result)


                except NoSuchElementException as e:
                    print(f"An element was not found: {e}")
                    continue

    except TimeoutException:
        print("No products found.")
    finally:
        driver.quit()

    return results




def scrape_marjanemall(query):
    print("----------SCRAPING MARJANEMALL----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.marjanemall.ma/catalogsearch/result/?q=" + query)

    try:
        # Wait for the product listing to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-item"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            # Extract title and URL
            title_element = product.find_element(By.CSS_SELECTOR, "a.product-item-link")
            title = title_element.text.strip() if title_element else "N/A"
            url = title_element.get_attribute("href") if title_element else "N/A"

            # Extract price
            price_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".price-box .price"))
            )
            price_text = price_element.text.strip() if price_element else "0.00"
            price_text = re.sub(r'\s+', '', price_text)  # Remove whitespace
            price_text = re.sub(r'[^\d,]', '', price_text)  # Remove non-numeric except comma
            price_parts = price_text.split(',')
            if len(price_parts) == 2:
                price_integer = price_parts[0]
                price_decimal = price_parts[1]
            else:
                price_integer = price_text
                price_decimal = '00'

            # Merge integer and decimal parts to form the full price string
            price_text = f"{price_integer}.{price_decimal}"
            try:
                price = float(price_text)
            except ValueError:
                print(f"Could not convert price to float: '{price_text}'")
                price = 0.0

            # Extract image URL
            try:
                image_element = product.find_element(By.CSS_SELECTOR, "img.product-image-photo")
                image_url = image_element.get_attribute("data-src") if image_element.get_attribute("data-src") else image_element.get_attribute("src")
            except:
                image_url = None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results




def scrape_aswakassalam(query):
    print("----------SCRAPING ASWAKASSALAM----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.aswakassalam.com/?s=" + query + "&post_type=product&product_cat=0")

    try:
        # Check for either product listing or single product page
        is_product_page = "/produit/" not in driver.current_url

        if is_product_page:
            # Product listing page
            products = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product")))
            results = []
            for index, product in enumerate(products):
                if index >= 10:  # Stop after 10 products
                    break
                try:
                    # Extract details for each product
                    title_element = product.find_element(By.CSS_SELECTOR, "a.product-loop-title")
                    title = title_element.text.strip() if title_element else "N/A"
                    url = title_element.get_attribute("href") if title_element else "N/A"

                    # Extract price
                    price_element = product.find_element(By.CSS_SELECTOR, ".price")
                    price_text = price_element.text.strip()
                    if "del" in price_element.get_attribute("innerHTML"):
                        # Product is on sale, get the current price
                        current_price = price_element.find_element(By.CSS_SELECTOR, "ins").text.strip()
                    else:
                        current_price = price_text

                    # Remove currency symbol and convert to float
                    current_price = re.sub(r'[^\d,]', '', current_price).replace(',', '.')
                    price = float(current_price)

                    image_element = product.find_element(By.CSS_SELECTOR, ".product-image img")
                    image_url = image_element.get_attribute("src") if image_element else None

                    result = {"title": title, "url": url, "price": price, "image_url": image_url}
                    results.append(result)
                    print(result)

                except NoSuchElementException as e:
                    print(f"An element was not found for product {index + 1}: {e}")
                    continue
        else:
            # Single product page
            try:
                # Extract details for single product
                title_element = driver.find_element(By.CSS_SELECTOR, "a.product-loop-title")
                title = title_element.text.strip() if title_element else "N/A"

                url = driver.current_url

                # Extract price
                price_element = driver.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_element.text.strip()
                if "del" in price_element.get_attribute("innerHTML"):
                    # Product is on sale, get the current price
                    current_price = price_element.find_element(By.CSS_SELECTOR, "ins").text.strip()
                else:
                    current_price = price_text

                # Remove currency symbol and convert to float
                current_price = re.sub(r'[^\d,]', '', current_price).replace(',', '.')
                price = float(current_price)

                image_element = driver.find_element(By.CSS_SELECTOR, ".product-image img")
                image_url = image_element.get_attribute("src") if image_element else None

                result = {"title": title, "url": url, "price": price, "image_url": image_url}
                results = [result]
            except NoSuchElementException as e:
                print(f"An element not found on product page: {e}")
                results = []
    except TimeoutException:
        print("No products found.")
        return []
    finally:
        driver.quit()

    return results




def scrape_mediazone(query):
    print("----------SCRAPING MEDIAZONE----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://mediazone.ma/products?search="+ query + "=&page=1&count=33&price=0%3B62000&order=default&campaign=&productTag=-1&outlet=-1&wcategories=1")

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            title_element = product.find_element(By.CLASS_NAME, "mkd-product-list-title").find_element(By.TAG_NAME, "a")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")

            # Check if the product is in stock
            if "out-of-stock" in product.get_attribute("class"):
                print(f"Product {index + 1} is out of stock.")
                continue

            # Try different methods to extract price information
            price_element = None
            try:
                # Method 1: Find price element using specific class
                price_element = product.find_element(By.CSS_SELECTOR, ".one-column-content-price .one-column-current-price .pix-aem-price")
            except NoSuchElementException:
                try:
                    # Method 2: Find price element using different class
                    price_element = product.find_element(By.CSS_SELECTOR, ".one-column-content-price .one-column-minor-price .one-column-street-price")
                except NoSuchElementException:
                    try:
                        # Method 3: Find price element using different class
                        price_element = product.find_element(By.CSS_SELECTOR, ".price span.amount")
                    except NoSuchElementException:
                        # If price cannot be found, skip this product
                        print(f"Price not found for product {index + 1}.")
                        continue

            price_text = price_element.text.strip()
            # Remove non-numeric characters and convert to float
            price_text = re.sub(r'[^\d.,]', '', price_text)
            price = float(price_text.replace(',', '.'))

            # Scrape image URL
            try:
                image_element = product.find_element(By.CLASS_NAME, "mkd-pl-image").find_element(By.TAG_NAME, "img")
                image_url = image_element.get_attribute("src")
            except:
                image_url = None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results



def scrape_bestmark(query):
    print("----------SCRAPING BESTMARK----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.bestmark.ma/catalogsearch/result/?q=" + query)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            title_element = product.find_element(By.CSS_SELECTOR, ".product-item-name a")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")

            price_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".price-box .price"))
            )
            if price_element:
                price_text = price_element.text.strip()
                # Remove non-numeric characters and convert to float
                price_text = re.sub(r'[^\d.,]', '', price_text)
                price = float(price_text.replace(',', '.'))
            else:
                price = "N/A"

            # Check for price of 0 and print "out of stock" message
            if price == 0:
                print(f"Product {index + 1} is out of stock.")
                continue

            image_element = product.find_element(By.CSS_SELECTOR, ".product-image-photo")
            if image_element:
                image_url = image_element.get_attribute("src")
            else:
                image_url = None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results




def scrape_cosmoselectro(query):
    print("----------SCRAPING COSMOSELECTRO----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    driver.get("https://www.cosmoselectro.ma/products?categories%5B%5D=0&q=" + query)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ps-product"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            title_element = product.find_element(By.CSS_SELECTOR, ".ps-product__container .ps-product__content h4 a")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")

            try:
                price_element = product.find_element(By.CSS_SELECTOR, ".ps-product__price")
                price_text = price_element.text.strip()

                # Handle sale prices by extracting both the current and old prices
                if "sale" in price_element.get_attribute("class"):
                    prices = re.findall(r'\d{1,3}(?:[.,\s]?\d{3})*(?:[.,]\d{2})?', price_text)
                    if len(prices) > 0:
                        current_price_text = prices[0].replace(' ', '').replace(',', '')
                        price = float(current_price_text)
                    else:
                        price = None
                else:
                    price_text = re.sub(r'[^\d.,]', '', price_text).replace(',', '')
                    price = float(price_text)

            except NoSuchElementException:
                # If the price cannot be found, skip this product
                print(f"Price not found for product {index + 1}. Skipping...")
                continue

            image_element = product.find_element(By.CSS_SELECTOR, ".ps-product__thumbnail a img")
            if image_element:
                image_url = image_element.get_attribute("src")
            else:
                # If the image cannot be found, set a default image
                image_url = None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results




def scrape_iris(query):
    print("----------SCRAPING IRIS----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the Iris search results page
    driver.get("https://www.iris.ma/search?controller=search&orderby=position&orderway=desc&search_query=" + query)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.product_list li.product_item"))
        )
    except TimeoutException:
        print("No products found.")
        driver.quit()
        return []

    results = []
    for index, product in enumerate(products):
        if index >= 10:  # Stop after 10 products
            break
        try:
            # Check if the product is out of stock
            if product.find_elements(By.CSS_SELECTOR, ".product-unavailable"):
                print(f"Product {index + 1} is out of stock.")
                continue

            title_element = product.find_element(By.CSS_SELECTOR, ".product-title a")
            title = title_element.text.strip()
            url = title_element.get_attribute("href")

            try:
                price_element = product.find_element(By.CSS_SELECTOR, ".product-price-and-shipping .price")
                price_text = price_element.text.strip()
                # Handle empty price text
                if price_text:
                    # Remove non-numeric characters and convert to float
                    price_text = re.sub(r'[^\d.,]', '', price_text).replace(',', '.')
                    price = float(price_text)
                else:
                    price = None
            except NoSuchElementException:
                # If the price cannot be found, skip this product
                print(f"Price not found for product {index + 1}. Skipping...")
                continue

            image_element = product.find_element(By.CSS_SELECTOR, ".product-thumbnail img")
            image_url = image_element.get_attribute("data-src") if image_element else None

            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    driver.quit()
    return results




def scrape_biougnach(query):
    print("----------SCRAPING BIOUGNACH----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    # Navigate to the website
    driver.get("https://www.biougnach.ma")

    # Locate the search box and type the query
    search_box = driver.find_element(By.CLASS_NAME, "search__input")
    driver.execute_script("arguments[0].click();", search_box)
    search_box.send_keys(query)
    search_box.send_keys(Keys.ENTER)

    try:
        # Wait for products to load
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "products-list__item"))
        )

    except TimeoutException:
        # If products do not load within 10 seconds, print message and exit
        print("No products found.")
        driver.quit()
        return []

    # Initialize an empty list to store product details
    results = []

    # Iterate over each product
    for index, product in enumerate(products):
        if index >= 8:  # Stop after 10 products
            break

        try:
            # Check if the product is out of stock
            try:
                out_of_stock_element = product.find_element(By.CLASS_NAME, "product-card__badge--outOfStock")
                if out_of_stock_element:
                    print(f"Product {index + 1} is out of stock.")
                    continue
            except NoSuchElementException:
                # If the out-of-stock element is not found, continue as usual
                pass

            # Extract product title and URL
            title_element = product.find_element(By.CLASS_NAME, "product-card__name")
            title = title_element.text.strip()

            url_element = product.find_element(By.CLASS_NAME, "ng-star-inserted")
            url = url_element.get_attribute("href")

            # Extract product prices
            price_element = product.find_element(By.CLASS_NAME, "product-card__prices")
            price_texts = price_element.text.strip().split()

            if len(price_texts) == 1:
                # Product not on sale
                price_text = price_texts[0]
            else:
                # Product on sale
                price_text = price_texts[0]  # Consider using the new price for the product

            # Split price text at the comma
            price_parts = price_text.split(',')

            # Remove non-numeric characters from each part and join them back with a period
            price = float('.'.join(re.sub(r'[^\d]+', '', part) for part in price_parts))

            # Extract product image URL
            try:
                image_element = product.find_element(By.TAG_NAME, "img")
                image_url = image_element.get_attribute("src")
            except:
                image_url = None

            # Append product details to the results list
            result = {"title": title, "url": url, "price": price, "image_url": image_url}
            results.append(result)
            print(result)

        except NoSuchElementException as e:
            print(f"An element was not found for product {index + 1}: {e}")
            continue

    # Close the webdriver
    driver.quit()

    return results




def scrape_micromagma(query):
    print("----------SCRAPING MICROMAGMA----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    # Navigate to the website
    driver.get("https://www.micromagma.ma")

    try:
        # Locate the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "products-search"))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        # Wait for products to load
        try:
            products = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "MuiAutocomplete-option"))
            )
        except TimeoutException:
            print("No products found.")
            driver.quit()
            return []

        # Initialize an empty list to store product details
        results = []

        # Iterate over each product (up to 10 products)
        for index, product in enumerate(products):
            if index >= 10:  # Stop after 10 products
                break
            try:
                # Locate the product elements again
                products = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "MuiAutocomplete-option"))
                )

                product = products[index]

                # Extract product title
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-1qfapge"))
                )
                title = title_element.text.strip()

                # Extract product price
                try:
                    # Wait for the search page to load again
                    price_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "p.MuiTypography-root.MuiTypography-body1.css-1tp9glm"))
                    )
                    price_text = price_element.text.strip()
                    price = float(re.sub(r'[^\d.]', '', price_text))
                except:
                    price = "N/A"

                # Extract product image URL
                try:
                    image_element = product.find_element(By.CSS_SELECTOR, "img.MuiCardMedia-root.MuiCardMedia-media.MuiCardMedia-img.css-1vky1st")
                    image_url = image_element.get_attribute("src")
                except:
                    image_url = None

                title_element.click()

                # Wait for the product detail page to load
                WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

                url = driver.current_url

                # Construct the result dictionary
                result = {"title": title, "url": url, "price": price, "image_url": image_url}
                results.append(result)
                print(result)

                # Wait for the search page to load again
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "products-search"))
                )

                # Re-enter the search query
                search_box = driver.find_element(By.ID, "products-search")
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.ENTER)

            except Exception as e:
                print(f"An element was not found or timed out for product {index + 1}: {e}")
                continue

    finally:
        # Close the webdriver
        driver.quit()

    return results




def scrape_uno(query):
    print("----------SCRAPING UNO----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    # Navigate to the Kitea search results page
    driver.get("https://uno.ma/catalogsearch/result/?q=" + query)

    try:
        # Find all product elements
        products = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "product-item-info")))

        # Check if it's a product page based on URL structure
        is_product_page = "catalogsearch/result" not in driver.current_url

        # Initialize an empty list to store product details
        results = []

        if is_product_page:
            # Extract product details from the product page
            try:
                #Check if the product is out of stock
                try:
                    out_of_stock_element = driver.find_element(By.ID,
                                                               "button[id='product-addtocart-button'] span")
                    if not out_of_stock_element:
                        print("Product is out of stock.")
                        return []
                except NoSuchElementException:
                    pass

                # Extract product title
                title_element = driver.find_element(By.CSS_SELECTOR, ".base")
                title = title_element.text.strip()

                url = driver.current_url


                # Extract product price
                price_element = driver.find_element(By.CSS_SELECTOR, ".price")
                price_text = price_element.text.strip()

                # Adjust price text to remove decimal part and non-digit characters
                price_text = re.search(r'(\d+,\d+)(?=,)', price_text).group(1)
                price = float(price_text.replace(',', ''))


                # Extract product image URL
                try:
                    image_element = driver.find_element(By.CSS_SELECTOR, ".fotorama__img")
                    image_url = image_element.get_attribute("src")
                except:
                    image_url = None

                # Construct the result dictionary
                result = {"title": title, "url": url, "price": price, "image_url": image_url}
                results.append(result)
                print(result)

            except:
                print("product 1 out of stock")
        else:
            # Find all product elements
            products = driver.find_elements(By.CLASS_NAME, "product-item-info")

            # Initialize an empty list to store product details
            results = []

            # Iterate over each product
            for index, product in enumerate(products):
                if index >= 10:  # Stop after 10 products
                    break
                try:
                    # Extract product title
                    title_element = product.find_element(By.CLASS_NAME, "product-item-link")
                    title = title_element.text.strip()

                    # Extract product URL
                    url = title_element.get_attribute("href")

                    # Extract product price
                    try:
                        # Extract product price
                        price_element = product.find_element(By.CSS_SELECTOR, ".price")
                        price_text = price_element.text.strip()

                        # Adjust price text to remove decimal part and non-digit characters
                        price_text = re.search(r'(\d+,\d+)(?=,)', price_text).group(1)
                        price = float(price_text.replace(',', ''))
                    except:
                        print(f"Product {index + 1} is out of stock.")
                        continue

                    # Extract product image URL
                    try:
                        image_element = product.find_element(By.CSS_SELECTOR, ".product-image-photo")
                        image_url = image_element.get_attribute("data-original")
                    except:
                        image_url = None

                    # Construct the result dictionary
                    result = {"title": title, "url": url, "price": price, "image_url": image_url}
                    results.append(result)
                    print(result)

                except NoSuchElementException as e:
                    print(f"An element was not found: {e}")
                    continue

    finally:
        # Close the webdriver
        driver.quit()

    if not results:
        print("No products found.")

    return results




def scrape_ikea(query):
  print("----------SCRAPING IKEA----------")

  # Set up Chrome options for headless mode
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("window-size=1920x1080")
  chrome_options.add_argument("start-maximized")
  chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  # Initialize the Chrome webdriver with options
  driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

  # Navigate to the IKEA website
  driver.get(f"https://www.ikea.com/ma/en/search/?q=" + query)

  try:
    # Wait for products to load
    try:
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, "plp-fragment-wrapper"))
      )
    except TimeoutException:
      print("No products found.")
      driver.quit()
      return []

    # Find all product elements
    products = driver.find_elements(By.CLASS_NAME, "plp-fragment-wrapper")

    # Initialize an empty list to store product details
    results = []

    # Iterate over each product
    for product in products:
      try:
        # Extract product title
        title_element = product.find_element(By.XPATH, ".//span[@class='notranslate plp-price-module__product-name']")
        title = title_element.text.strip()

        # Extract product URL
        url_element = product.find_element(By.XPATH, ".//a[@class='plp-product__image-link link']")
        url = url_element.get_attribute("href")

        # Extract product price (target current price regardless of strikethrough)
        price_text = ""
        try:
            current_price_element = product.find_element(By.XPATH, ".//span[contains(@class, 'plp-price-module__current-price')]")
            price_text = current_price_element.find_element(By.CLASS_NAME, "plp-price__integer").text.strip()
        except NoSuchElementException:
            try:
                current_price_element = product.find_element(By.XPATH, ".//em[contains(@class, 'plp-price-module__current-price')]")
                price_text = current_price_element.find_element(By.CLASS_NAME, "plp-price__integer").text.strip()
            except NoSuchElementException:
                print(f"Price element not found on product page: {url}")
        # Convert price to float
        if price_text:
            price = float(price_text.replace('DH', '').replace(' ', '').strip())
        else:
            price = None

        # Extract product image URL
        try:
            image_element = product.find_element(By.XPATH, ".//img[@class='plp-image plp-product__image']")
            image_url = image_element.get_attribute("src")
        except:
            image_url = None

        # Check if the product is out of stock
        stock_status = "In Stock"
        try:
          out_of_stock_element = product.find_element(By.XPATH, ".//p[contains(@class, 'pip-label-text')]")
          if "Out of stock" in out_of_stock_element.text or "épuisé" in out_of_stock_element.text:
            stock_status = "Out of Stock"
        except NoSuchElementException:
          pass  # If no out-of-stock element is found, assume the product is in stock

        # Construct the result dictionary
        result = {"title": title, "url": url, "price": price, "image_url": image_url}
        results.append(result)
        print(result)

      except NoSuchElementException as e:
        print(f"An element was not found for a product: {e}")
        continue

      except Exception as e:
        print(f"An error occurred while scraping a product: {e}")
        continue

  finally:
    # Close the webdriver
    driver.quit()

  return results




def scrape_kitea(query):
    print("----------SCRAPING KITEA----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    # Navigate to the Kitea search results page
    driver.get(f"https://www.kitea.com/catalogsearch/result/?cat=&q=" + query)

    try:
        # Check if it's a product page based on URL structure
        is_product_page = "catalogsearch/result" not in driver.current_url

        # Initialize an empty list to store product details
        results = []

        if is_product_page:
            # Extract product details from the product page
            try:
                # Check if the product is out of stock
                try:
                    out_of_stock_element = driver.find_element(By.XPATH, "/html/body/div[3]/main/div[2]/div/div[1]/div[3]/form/div[1]/div[3]")
                    if out_of_stock_element:
                        print("Product is out of stock.")
                        return []
                except NoSuchElementException:
                    pass

                title_element = driver.find_element(By.CSS_SELECTOR, ".page-title .base")
                title = title_element.text.strip()

                url = driver.current_url

                # Locate the image within the gallery placeholder
                try:
                    image_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/main[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[1]/img[1]")
                    image_url = image_element.get_attribute("src")
                except NoSuchElementException:
                    print("Image element not found on product page")
                    image_url = None

                price_text = ""
                try:
                    special_price_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/main[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span[2]/span[1]/span[2]/span[1]")
                    price_text = special_price_element.text.strip()
                except NoSuchElementException:
                    try:
                        regular_price_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/main[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span[2]/span[1]/span[2]/span[1]")
                        price_text = regular_price_element.text.strip()
                    except NoSuchElementException:
                        print(f"Price element not found on product page: {url}")

                if price_text:
                    price_text = re.sub(r'[^\d,]', '', price_text)  # Remove non-numeric except comma
                    price = float(price_text.replace('.', '').replace(',', '.'))
                else:
                    price = None

                result = {"title": title, "url": url, "price": price, "image_url": image_url}
                results.append(result)
                print(result)

            except Exception as e:
                print(f"An error occurred while scraping the product page: {e}")

        else:
            # Extract product details from the search results page
            products = driver.find_elements(By.CLASS_NAME, "product-item-info")
            # Iterate over each product
            for index, product in enumerate(products):
                if index >= 10:  # Stop after 10 products
                    break
                try:
                    # Check if the product is out of stock
                    try:
                        out_of_stock_element = product.find_element(By.CSS_SELECTOR, "div[class='row info-product-list skyinfo'] a:nth-child(1)")
                        if out_of_stock_element:
                            print(f"Product {index + 1} is out of stock.")
                            continue
                    except NoSuchElementException:
                        pass

                    title_element = product.find_element(By.CLASS_NAME, "product-item-link")
                    title = title_element.text.strip()

                    url = title_element.get_attribute("href")

                    # Try multiple selectors for the image element
                    try:
                        image_element = product.find_element(By.CSS_SELECTOR, ".product-image-photo")
                    except NoSuchElementException:
                        try:
                            image_element = product.find_element(By.CSS_SELECTOR, "img")
                        except NoSuchElementException:
                            image_element = None

                    if image_element:
                        image_url = image_element.get_attribute("src")
                    else:
                        image_url = None

                    price_text = ""
                    try:
                        special_price_element = product.find_element(By.XPATH, ".//span[@class='special-price']//span[@class='price']")
                        price_text = special_price_element.text.strip()
                    except NoSuchElementException:
                        try:
                            regular_price_element = product.find_element(By.XPATH, ".//span[contains(@id, 'product-price')]//span[@class='price']")
                            price_text = regular_price_element.text.strip()
                        except NoSuchElementException:
                            print(f"Price element not found for product: {url}")

                    if price_text:
                        price_text = re.sub(r'[^\d,]', '', price_text)  # Remove non-numeric except comma
                        price = float(price_text.replace('.', '').replace(',', '.'))
                    else:
                        price = None

                    result = {"title": title, "url": url, "price": price, "image_url": image_url}
                    results.append(result)
                    print(result)

                except NoSuchElementException as e:
                    print(f"An element was not found: {e}")
                    continue

    finally:
        # Close the webdriver
        driver.quit()

    if not results:
        print("No products found.")

    return results




def scrape_bricoma(query):
    print("----------SCRAPING BRICOMA----------")

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome webdriver with options
    driver = webdriver.Chrome(options=chrome_options)  # options=chrome_options

    # Navigate to the Bricoma search results page
    driver.get(f"https://www.bricoma.ma/catalogsearch/result/?q=" + query)

    try:
        # Wait for products to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-item-info"))
            )
        except TimeoutException:
            print("No products found.")
            driver.quit()
            return []

        # Find all product elements
        products = driver.find_elements(By.CLASS_NAME, "product-item-info")

        # Initialize an empty list to store product details
        results = []

        # Iterate over each product
        for index, product in enumerate(products):
            if index >= 10:  # Stop after 10 products
                break
            try:
                # Extract product title
                title_element = product.find_element(By.CLASS_NAME, "product-item-link")
                title = title_element.text.strip()

                # Extract product URL
                url = title_element.get_attribute("href")

                # Extract product image URL
                try:
                    image_element = product.find_element(By.CLASS_NAME, "product-image-photo")
                    image_url = image_element.get_attribute("data-src")
                except:
                    image_url = None

                # Extract product price
                try:
                    # Try to find the special price
                    price_element = product.find_element(By.XPATH, ".//span[@class='special-price']//span[@class='price']")
                    price_text = price_element.text.strip()
                except NoSuchElementException:
                    # If special price is not found, use the regular price
                    price_element = product.find_element(By.XPATH, ".//span[@class='price-container price-final_price tax weee rewards_earn']//span[@class='price']")
                    price_text = price_element.text.strip()

                # Remove spaces and convert to float
                price_text = re.sub(r'[^\d,]', '', price_text)  # Remove non-numeric except comma
                price = float(price_text.replace(',', '.'))

                # Construct the result dictionary
                result = {"title": title, "url": url, "price": price, "image_url": image_url}
                results.append(result)
                print(result)

            except NoSuchElementException as e:
                print(f"An element was not found for a product: {e}")
                continue

            except Exception as e:
                print(f"An error occurred while scraping a product: {e}")
                continue

    finally:
        # Close the webdriver
        driver.quit()

    return results
