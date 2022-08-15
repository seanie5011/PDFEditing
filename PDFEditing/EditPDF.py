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
            self.pdf_bookmarks_list.append([bookmark_title, 0, None, None])  # bookmark_list contains the text, the index of the bookmark, the parent (None is no parent), and the object reference

        self._add_all_readers()

    def _add_all_readers(self):
        ''' Takes all readers from pdf_readers_list and appends each page to pdf_writer, with bookmarks
        '''

        # pass through all readers
        for reader_index, reader in enumerate(self.pdf_reader_list):
            # pass through all pages
            for page_index, page in enumerate(reader.pages):
                self.pdf_writer.add_page(page)
                if page_index == 0:  # if first new page, add bookmark, note indexing requires -1
                    self.pdf_bookmarks_list[reader_index][1] = len(self.pdf_writer.pages) - 1  # update the index of the bookmark
                    self.pdf_bookmarks_list[reader_index][3] = self.pdf_writer.add_outline_item(*self.pdf_bookmarks_list[reader_index][:-1])  # see _update_bookmarks

    def insert_pdf(self, path, page_number):
        ''' Can insert a new pdf at the specified page_number, adds a bookmark
        path must be of type string or pathlib.WindowsPath variable and page_number must be of type int
        '''

        # add pdf to writer
        path = str(path)
        new_reader_pages = PdfFileReader(path).pages
        new_page_index = page_number - 1

        for index, page in enumerate(new_reader_pages):  # make a temp reader for this pdf
            self.pdf_writer.insert_page(page, new_page_index + index)

        # add and fix bookmarks
        bookmark_title = path.split('\\')[-1][:-4]
        self._fix_bookmarks(len(new_reader_pages), new_page_index, bookmark_title=bookmark_title)

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

        self._fix_bookmarks(-1, page_number - 1)

    def _fix_bookmarks(self, alter_amount, threshold_index, bookmark_title=None, parent=None):
        ''' Move every bookmark after by alter_amount and insert new bookmark_title under parent at threshold_index if desired
        alter_amount and threshold_index must be ints, bookmark_title must be a string and parent must be another bookmark if desired
        '''

        bookmark_added = False  # whether the new bookmark was added yet
        for list_index, bookmark_list in enumerate(self.pdf_bookmarks_list):
            altered_page_index = bookmark_list[1] + alter_amount  # each index gets moved by the new amount
            if bookmark_list[1] >= threshold_index:
                if not bookmark_added and bookmark_title is not None:
                    self.pdf_bookmarks_list.insert(list_index, [bookmark_title, threshold_index, parent, None])  # add the bookmark in proper place in list
                    bookmark_added = True
                else:
                    self.pdf_bookmarks_list[list_index][1] = altered_page_index  # all bookmarks after the new one need to be altered

        # if bookmark we want to add is after all other bookmarks
        if not bookmark_added and bookmark_title is not None:
            self.pdf_bookmarks_list.append([bookmark_title, threshold_index, parent, None])
            bookmark_added = True

        self._update_bookmarks()

    def _update_bookmarks(self):
        ''' Helper function that can be used to update bookmarks
        '''

        self.remove_bookmarks()  # remove all currently added
        for index, bookmark in enumerate(self.pdf_bookmarks_list):  # add them all back and new ones now in pdf_bookmarks_list
            self.pdf_bookmarks_list[index][3] = self.pdf_writer.add_outline_item(*bookmark[:-1])  # unpack bookmark except last item (the reference which is assigned here)

    def remove_bookmarks(self):
        ''' Removes all bookmarks from pdf_writer
        '''

        pages = self.pdf_writer.pages

        self.pdf_writer = PdfFileWriter()  # reset it
        for page in pages:
            self.pdf_writer.add_page(page)  # does not retain bookmarks when we add back

    def add_bookmark(self, text, page_number, parent=None):
        ''' Adds a bookmark of title text onto page_number under parent
        text must be of type string, page_number of type int and parent of TreeObject from bookmark-reference
        '''
        # PARENT FUNCTIONALITY NOT FULLY ADDED
        # NEED TO FIND OUT HOW TO TELL FUNCTION WHICH PARENT WE WANT FROM LIST
        self._fix_bookmarks(0, page_number - 1, text, parent)

    def write_to_file(self, output_folder_path):
        ''' Writes the pdf instance to the designated folder.
        output_folder_path should be a string or pathlib.WindowsPath variable
        '''
        if type(output_folder_path) == str: output_folder_path = Path(output_folder_path)
        output_path = output_folder_path / 'new_pdf-000.pdf'

        # find correct path to create
        counter = 1
        while output_path.exists():
            output_path = output_folder_path / f'new_pdf-{counter:03d}.pdf'  # while current desired directory already exists, try same title with increasing number
            counter += 1

            # break loop and function if too many files
            if counter == 99:
                print("ERROR: Too Many Files")
                return

        # write to file
        with output_path.open(mode="wb") as output_file:
            self.pdf_writer.write(output_file)
            print('YES')


def main():
    pdf_path = Path.cwd() / 'testdocs' / 'reports'
    path = [pdf_path / 'PY3109Lecture1.pdf', pdf_path / 'PY3109Lecture2.pdf']
    output_path = Path.cwd() / 'testdocs'

    pdf = PDFEditing()
    pdf.add_readers_from_list(path)
    pdf.add_all_readers()
    pdf.insert_pdf(Path.cwd() / 'testdocs' / 'Test1.pdf', 1)
    pdf.add_bookmark("hello", 2)
    pdf.cut_page(1)
    pdf.write_to_file(output_path)


if __name__ == '__main__':
    main()
