from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileMerger
from pathlib import Path  # pathlib is local to Python3


def main():
    # Extracting Text from a PDF
    # Paths
    pdf_path = Path.cwd() / "testdocs"  # the Path cwd object, which is where this .py file is located + the path to the folder

    # PDFs
    pdf_reader = PdfFileReader(str(pdf_path / "Test1.pdf"))  # must add path to pdf
    pdf_writer = PdfFileWriter()  # a writer
    pdf_merger = PdfFileMerger()  # a merger

    # Testing Attributes
    print(pdf_reader.getNumPages())
    print(pdf_reader.documentInfo)  # metadata
    print(pdf_reader.documentInfo.title)

    # Extracting Text from a Page
    first_page = pdf_reader.pages[0]  # get the first page
    print(type(first_page))

    print(first_page.extractText())  # prints text from first page, if applicable
    for page in pdf_reader.pages:
        print(page.extractText())  # prints text from all pages, if applicable

    # Saving this text to a .txt file
    output_file_path = pdf_path / "Test1_converted.txt"  # add name of new .txt file
    with output_file_path.open(mode="w") as output_file:  # use pathlibs inbuilt open
        # Get attributes and write them
        title = pdf_reader.documentInfo.title
        num_pages = pdf_reader.getNumPages()
        output_file.write(f"{title}\\nNumber of pages: {num_pages}\\n\\n")

        # write in .txt the text for each page
        for page in pdf_reader.pages:
            text = page.extractText()
            output_file.write(text)

    # Extracting Pages from a PDF
    # Using PDF Writer
    pdf_writer.addBlankPage(width=72, height=72)  # write a blank page object to the writer, each unit is 1/72 of an inch, so we have a 1in-1in pdf page now
    # write a new blank pdf, in binary write mode
    with Path("testdocs\\blank.pdf").open(mode="wb") as output_file:  # have to specify path - starting from current directory, "blank" is the desired name
        pdf_writer.write(output_file)  # pdf_writer writes a blank page as determined above
        # the above line may seem backwards, the output_file is actually the new file and pdf_writer.write() writes whatever pdf_writer holds onto it

    # Extracting a single page from a PDF
    # open pdf, extract first page, save to new pdf
    input_pdf = PdfFileReader(str(pdf_path / "Test1.pdf"))
    first_page = input_pdf.pages[0]

    pdf_writer = PdfFileWriter()
    pdf_writer.add_page(first_page)

    with Path('testdocs\\Test1_first_page.pdf').open(mode='wb') as output_file:
        pdf_writer.write(output_file)

    # Extracting multiple pages from a PDF
    # can do the same as above using a loop
    # lets use a lecture instead, we want pages 2 and 3
    input_pdf = PdfFileReader(str(pdf_path / "reports" / "PY3109Lecture2.pdf"))
    pdf_writer = PdfFileWriter()
    for page in input_pdf.pages[1:3]:  # pages 2 and 3 are indexes 1 and 2
        pdf_writer.add_page(page)

    with Path('testdocs\\Lecture2_page2n3.pdf').open(mode='wb') as output_file:
        pdf_writer.write(output_file)

    # Extracting every page from a pdf
    # shortcut to take every page from a pdf and write to pdf_writer
    # use same input_pdf
    pdf_writer = PdfFileWriter()
    pdf_writer.append_pages_from_reader(input_pdf)

    with Path('testdocs\\Lecture2_all.pdf').open(mode='wb') as output_file:
        pdf_writer.write(output_file)

    # Concatenating PDFs
    # using .append()
    # concatenates to the end of the pdf doc
    reports_dir = Path.cwd() / "testdocs" / "reports"  # get directory of the pdfs to be merged
    for path in reports_dir.glob("*.pdf"):  # glob finds pathnames that match the one specified
        print(path.name)

    # need to sort these to be certain of order
    reports = list(reports_dir.glob("*.pdf"))
    reports.sort()  # this sorts the pdfs alphabetically
    for i, path in enumerate(reports):  # check it and merge em
        print(path.name)
        pdf_merger.append(str(path), "PY3109Lecture{0}".format(i + 1))  # merges the pdfs in order given by reports, with name in second comma for the bookmark

    # now write new pdf, with in-built write from pdf_merger
    with Path("testdocs\\merged_reports.pdf").open(mode="wb") as output_file:
        pdf_merger.write(output_file)  # writes the merged pdf to merged_reports.pdf, a new file

    # using .merge()
    # concatenates at insertion point specified
    # put first page of test pdf into lecture 2 at 3rd page
    merge_pdf = PdfFileReader(str(pdf_path / "Test1.pdf"))  # reader instance so we can get specific pages
    main_pdf_path = str(pdf_path / "reports" / "PY3109Lecture2.pdf")

    pdf_merger = PdfFileMerger()
    pdf_merger.append(main_pdf_path)  # initialise with main pdf

    pdf_merger.merge(2, merge_pdf, pages=(0, 1))  # insert first page (index 0, spans to 1 but not including 1) into doc at page 3 (index 2); page 3 is moved to after merge_pdf
    pdf_merger.add_outline_item('Test Page!', 2)  # create bookmark for page 3 (index 2), seems to mess up order of bookmarks though

    with Path("testdocs\\merged_test.pdf").open(mode="wb") as output_file:
        pdf_merger.write(output_file)

    # Rotating and Cropping

    # Encrypting and Decrypting

    # PDF File from scratch

    # merging using a writer
    main_pdf = PdfFileReader(str(pdf_path / "reports" / "PY3109Lecture2.pdf"))
    merge_pdf = PdfFileReader(str(pdf_path / "Test1.pdf"))
    writer = PdfFileWriter()
    writer.append_pages_from_reader(main_pdf)
    writer.add_outline_item('PY3109Lecture2', 0)
    for index, page in enumerate(merge_pdf.pages):
        writer.add_page(page)
        if index == 0:
            writer.add_outline_item('Test1', len(writer.pages))

    with Path("testdocs\\merged_testyyuiuagf.pdf").open(mode="wb") as output_file:
        writer.write(output_file)



if __name__ == '__main__':
    main()
