from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
from PIL import Image
import os, ssl
import argparse

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def requestpage(input_link):
    req = Request(input_link, headers={'User-Agent': 'Mozilla/5.0'})
    gcontext = ssl._create_unverified_context()
    uClient = urlopen(req, context=gcontext)
    page_html = uClient.read()
    uClient.close()
    return soup(page_html, "html.parser")

def generate_url(id, seq, size):
    return f"https://babel.hathitrust.org/cgi/imgsrv/image?id={id};seq={seq};size={size};rotation=0"

def get_id(url):
    id = url.replace('https://babel.hathitrust.org/cgi/pt?id=', '')
    if '&' in id:
        id = id[:id.index('&')]
    return id

def download_image(url, directory):
    # try:
    urlretrieve(url, directory)
    # except:
    #     print('Exception occurred')
    #     return False
    # return True

def get_length(page_soup):
    return (int)(page_soup.find('section', {'class':'section-container'})['data-total-seq'])

def get_title(page_soup):
    return page_soup.find('div', {'class':'bibLinks panel'}).h1.span.text

def download_book(url, to_pdf=True):
    id = get_id(url)
    soup = requestpage(url)
    length = get_length(soup)

    rmchars = ['*', '.' '"', '/', '\\', '[', ']', ':', ';', '|', ',']
    title = get_title(soup)
    for char in rmchars:
        title = title.replace(char, '')

    directory = f'E:\\Documents\\Python Projects\\HathiTrust\\Downloads\\{title}\\'
    images = []

    print(f"Downloading {title}")

    if not os.path.exists(directory):
        os.makedirs(directory)

    printProgressBar(0, length, prefix='Progress:', suffix='Complete', length=50)

    for i in range(1, length+1):
        # print(f"Downloading Page {i} of {length}")
        printProgressBar(i, length, prefix='Progress:', suffix='Complete', length=50)
        url = f"\t{generate_url(id, i, 100)}"
        ext = "png"
        if not os.path.isfile(f"{directory}{i}.{ext}"):
            download_image(url, f"{directory}{i}.{ext}")
        # image = Image.open(f"{directory}{i}.{ext}")
        #
        # if image.format != ext:
        #     image.convert()
        #
        # print(image.format)

        images.append(f"{directory}{i}.{ext}")


    if to_pdf:
        pdf_new(images=images, title=title, directory=directory)

def pdf_new(images, title, directory):
    temp_images = []
    for image in images:
        # print(image)
        temp_images.append(Image.open(image).convert('RGB'))
    temp_images[0].save(f"{directory}{title}.pdf", save_all=True, append_images=temp_images)

def download_list(books, to_pdf=True):
    for book in books:
        print(book)
        download_book(book, to_pdf)

parser = argparse.ArgumentParser(description='Downloader for HathiTrust')

parser.add_argument('--url', help='Download url')
parser.add_argument('--file', help='Add text file with books')

args = parser.parse_args()

if args.url is not None:
    download_book(args.url, True)
elif args.file is not None:
    file = open(args.file)
    download_list(file.readlines())

# url = 'https://babel.hathitrust.org/cgi/pt?id=keio.10810467038&view=1up&seq=5'
# download_book(url, True)
