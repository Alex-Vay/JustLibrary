import re

import mobi
import html2text
import ebookmeta
import ebooklib
from ebooklib import epub
import pypdf
import docx2txt


encode = "utf-8"
metadata_message = "NO METADATA"


class Book:
    def __init__(self, text, metadata):
        self.text = text
        self.metadata = metadata


def fb2_read(filepath):
    metadata = ebookmeta.get_metadata(filepath)
    with open(filepath, "r", encoding=encode) as file:
        text = file.read()
        start_main_text = text.find("body")
        end_main_text = text.rfind("body")
        text = (html2text.html2text(text[start_main_text + 5:end_main_text - 2]))
        return Book(text, metadata)
# разбиение по главам с помощью soup
# def compile_chapter(section: Tag):
#     title = title_tag.get_text(strip=True) if (
#         title_tag := section.find('title')
#     ) else ''
#     rows = '\n'.join(
#         [p.get_text(strip=True) for p in title_tag.find_next_siblings('p')]
#     )
#     return f'{title}\n{rows}'
#
# with open('book.fb2', 'r', encoding='utf-8') as xml:
#     soup = Soup(xml.read(), 'lxml')
#
# chapters = [*map(compile_chapter, soup.find_all('section'))]


def epub_read(filepath):
    metadata = ebookmeta.get_metadata(filepath)
    book = epub.read_epub(filepath)
    text = ''
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text += html2text.html2text(item.get_body_content().decode('utf-8')).replace("_", "\t")
    return Book(text, metadata)


def mobi_read(filepath):
    tempdir, filename = mobi.extract(filepath)
    with open(filename, "r", encoding=encode) as file:
        text = (html2text.html2text(file.read()))
        return Book(text, metadata_message)


def pdf_read(filepath):
    reader = pypdf.PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text().strip()
    return Book(text, metadata_message)


def docx_read(filepath):
    text = docx2txt.process(filepath)
    return Book(text, metadata_message)


def txt_read(filepath):
    with open(filepath, "r", encoding=encode) as file:
        return Book(file.read(), "NO METADATA")


def read_book(filepath):
    path = filepath.split(".")
    match path[len(path)-1]:
        case "fb2":
            metadata = fb2_read(filepath)
        case "epub":
            metadata = epub_read(filepath)
        case "mobi":
            metadata = mobi_read(filepath)
        case "pdf":
            metadata = pdf_read(filepath)
        case "docx":
            metadata = docx_read(filepath)
        case "txt":
            metadata = txt_read(filepath)
        case _:
            return "Я не работаю с таким форматом(("
    metadata.text = re.sub(r"(?<!\n)\n(?!\n)", " ", metadata.text)
    return metadata


'''
title
author_list
series
series_index
tag_list
description
cover_image_data

format
'''