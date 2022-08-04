#---Imports---#
from PyPDF2 import PdfFileMerger
from pathlib import Path # pathlib is local to Python3

#---Paths---#
pdfs_dir = Path("C:\\Users\\seani\\Desktop\\Phys_Astro\\Phys_Astro - Third Year\\Semester2\\PY3106\\Lectures")

#---PDFs---#
pdf_merger = PdfFileMerger() # a merger

#---Concatenating PDFs---#
# need to sort these to be certain of order, use helper function to sort
pdfs = list(pdfs_dir.glob("*.pdf"))
pdfs.sort() # be careful with names, ensure there is a 0 infront of single digit numbers

# write to merger, with bookmarks
for i, path in enumerate(pdfs):
    print(path.name)
    pdf_merger.append(str(path), "PY3106Lecture{0}".format(i + 1))

# now write new pdf, with in-built write from pdf_merger
with Path("C:\\Users\\seani\\Desktop\\Phys_Astro\\Phys_Astro - Third Year\\Semester2\\PY3106\\PY3106AllLectures.pdf").open(mode="wb") as output_file:
    pdf_merger.write(output_file)