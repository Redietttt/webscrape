import time
import requests
from bs4 import BeautifulSoup
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

bot_token = "6821124656:AAF-yllAl1m3wusP3Cap90cbgQGihhCCsP8"
bot = telegram.Bot(token=bot_token)

async def scrape_books():
    url = "https://www.jaferbooks.com/explore-books.php?label=All%20Time%20Great"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_elements = soup.find_all('div', class_='product__style--3')

    books = []
    for element in product_elements:
        title_element = element.find('h6')
        title = title_element.text.strip() if title_element else "N/A"

        img_element = element.find('img', class_='first__img')
        img_url = img_element['src'] if img_element else "N/A"

        category_element = element.find('span', class_='hot-label')
        category = category_element.text.strip() if category_element else "N/A"

        price_element = element.find('ul', class_='prize').find('li')
        price = price_element.text.strip() if price_element else "N/A"

        books.append({
            'title': title,
            'img_url': img_url,
            'category': category,
            'price': price
        })

    return books

async def send_books_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    books = await scrape_books()

    for book in books:
        message = f"Title: {book['title']}\n" \
                  f"Image URL: {book['img_url']}\n" \
                  f"Category: {book['category']}\n" \
                  f"Price: {book['price']}"

        try:
            await update.message.reply_text(message)
        except telegram.error.TelegramError as e:
            print(f"Failed to send message: {e}")

def main() -> None:
    time.sleep(5)  # Add a delay before starting polling
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", send_books_to_user))

    application.run_polling()

if __name__ == "__main__":
    main()
