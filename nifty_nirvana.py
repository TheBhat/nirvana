import os
import pdfkit
from bs4 import BeautifulSoup

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

parent_folder = r'D:\my_projects\Nirvana\Archive'
year_dir = None
month_dir = None


def dir_check(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def download_archive(link):
    global year_dir
    global month_dir
    if not link[0].endswith("html") and link[1].isdigit():
        year_dir = link[1]
        dir_check(os.path.join(parent_folder, year_dir))
        print(f"year --> {year_dir}")
    elif not link[0].endswith("html"):
        month_dir = link[1]
        dir_check(os.path.join(parent_folder, year_dir, month_dir))
        print(f"month --> {month_dir}")
    elif link[0].endswith("html"):
        file_name = f'{link[1]}.pdf'
        file_name = file_name.replace(":", "_")
        if not os.path.exists(os.path.join(parent_folder, year_dir, month_dir, file_name)):
            print(f"filename : {file_name}")
            pdfkit.from_url(link[0], os.path.join(parent_folder, year_dir, month_dir, file_name), configuration=config)


def get_all_nn_archives():
    with open("nn_archive.html") as fh:
        soup = BeautifulSoup(fh, 'html.parser')

    output = []
    for link in soup.find_all('a'):
        url = None
        text = None
        if link.get('class'):
            if link.get('class')[0] != "toggle":
                url = link.get('href')
                text = link.text.replace('\n', '')
        else:
            url = link.get('href')
            text = link.text.replace('\n', '')
        if url or text:
            output.append((url, text))

    print(output)
    for link in output:
        download_archive(link)


get_all_nn_archives()
