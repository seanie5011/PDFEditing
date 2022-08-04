from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileMerger
from pathlib import Path  # pathlib is local to Python3

def main():
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
    first_page = pdf_reader.getPage(0)  # get the first page
    print(type(first_page))

    print(first_page.extractText())  # prints text from first page, if applicable
    for page in pdf_reader.pages:
        print(page.extractText())  # prints text from all pages, if applicable

    # Saving this text to a .txt file
    output_file_path = pdf_path / "Test1_converted.txt"  # add name of new .txt file
    with output_file_path.open(mode = "w") as output_file:  # use pathlibs inbuilt open
        # Get attributes and write them
        title = pdf_reader.documentInfo.title
        num_pages = pdf_reader.getNumPages()
        output_file.write(f"{title}\\nNumber of pages: {num_pages}\\n\\n")
        
        # write in .txt the text for each page
        for page in pdf_reader.pages:
            text = page.extractText()
            output_file.write(text)

    # Using PDF Writer
    pdf_writer.addBlankPage(width=72, height=72)  # write a blank page object to the writer, each unit is 1/72 of an inch, so we have a 1in-1in pdf page now
    # write a new blank pdf, in binary write mode
    with Path("testdocs\\blank.pdf").open(mode="wb") as output_file:  # have to specify path - starting from current directory, "blank" is the desired name
        pdf_writer.write(output_file)  # pdf_writer writes a blank page as determined above
        # the above line may seem backwards, the output_file is actually the new file and pdf_writer.write() writes whatever pdf_writer holds onto it

    # Extracting Pages from a PDF


    # Concatenating PDFs
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

    # Rotating and Cropping

    # Encrypting and Decrypting

    # PDF File from scratch


if __name__ == '__main__':
    main()
