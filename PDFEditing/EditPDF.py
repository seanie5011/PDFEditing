from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pathlib import Path


class PDFEditing():
    def __init__(self):
        self.pdf_writer = PdfFileWriter()
        self.pdf_reader_list = []
        self.pdf_bookmarks_list = []

    def reset(self):
        ''' Resets pdf_writer, pdf_reader_list, and pdf_bookmarks_list back to init state
        '''

        self.pdf_writer = PdfFileWriter()
        self.pdf_reader_list = []
        self.pdf_bookmarks_list = []

    def add_readers_from_list(self, path_list):
        ''' Looks at each path in path_list and appends to the pdf_reader_list, with bookmarks added to pdf_bookmarks_list
        path_list can hold strings or pathlib.WindowsPath variables
        '''

        for path in path_list:
            path = str(path)
            new_reader = PdfFileReader(path)

            # split up list seperated by the \\
            # so that the title of the pdf is the final ([-1]) entry
            # then remove the .pdf ([:-4])
            # append to pdf
            bookmark_title = path.split('\\')[-1][:-4]

            self.pdf_reader_list.append(new_reader)
            self.pdf_bookmarks_list.append(bookmark_title)

    def add_all_readers(self):
        ''' Takes all readers from pdf_readers_list and appends each page to pdf_writer, with bookmarks
        '''

        # pass through all readers
        for reader_index, reader in enumerate(self.pdf_reader_list):
            # pass through all pages
            for page_index, page in enumerate(reader.pages):
                self.pdf_writer.add_page(page)
                if page_index == 0:  # if first new page, add bookmark, note indexing requires -1
                    self.pdf_writer.add_outline_item(self.pdf_bookmarks_list[reader_index], len(self.pdf_writer.pages) - 1)

    def insert_pdf(self, path, page_number):
        ''' can insert a new pdf at the specified page_number, adds a bookmark
        path must be of type string or pathlib.WindowsPath variable and page_number must be of type int
        '''

        path = str(path)
        bookmark_title = path.split('\\')[-1][:-4]

        for index, page in enumerate(PdfFileReader(path).pages):  # make a temp reader for this pdf
            self.pdf_writer.insert_page(page, page_number - 1 + index)

        self.pdf_writer.add_outline_item(bookmark_title, page_number - 1)  # CAN MESS UP OTHER BOOKMARKS

    def cut_page(self, page_number):
        ''' Removes the page at a specific page_number
        page_number must be an int
        '''
        # CURRENTLY DOES NOT KEEP BOOKMARKS
        pages = self.pdf_writer.pages

        self.pdf_writer = PdfFileWriter()
        for page_index, page in enumerate(pages):
            if page_index != page_number - 1:  # add all pages bar one at page_number
                self.pdf_writer.add_page(page)

    def remove_bookmarks(self):
        ''' Removes all bookmarks from pdf_writer
        '''

        pages = self.pdf_writer.pages

        self.pdf_writer = PdfFileWriter()
        for page in pages:
            self.pdf_writer.add_page(page)  # does not retain bookmarks

    def add_bookmark(self, text, page_number):
        ''' Adds a bookmark of title text onto page_number
        text must be of type string and page_number of type int
        '''

        self.pdf_writer.add_outline_item(text, page_number - 1)

    def write_to_file(self, output_folder_path):
        ''' Writes the pdf instance to the designated folder.
        output_folder_path should be a string or pathlib.WindowsPath variable
        '''

        output_path = Path(output_folder_path / 'new_pdf-000.pdf')

        # find correct path to create
        counter = 1
        while output_path.exists():
            output_path = Path(output_folder_path / f'new_pdf-{counter:03d}.pdf')  # while current desired directory already exists, try same title with increasing number
            counter += 1

        # write to file
        with output_path.open(mode="wb") as output_file:
            self.pdf_writer.write(output_file)


def main():
    print("Hello World!")


if __name__ == '__main__':
    main()
