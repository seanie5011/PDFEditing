# PDFEditing

## This project contains scripts to perform various operations on a pdf, with GUI.

This project uses PyPDF2 to perform various operations on pdf files, such as merging, inserting, cutting pages, and adding bookmarks. A GUI is created using PySimpleGUI for a user-friendly app. The app contains 4 apps to perform these operations, detailed below.

### Merging

This tab allows the user to select a folder that contains all the desired pdf files to merge. The order of merging is sorted numerically, with the user able to input what prefix to sort through.

![github_PDFEditor_Merge](https://user-images.githubusercontent.com/72211395/184697580-612149dd-46fd-42fe-9a40-fd565397967a.png)

### Inserting

This tab allows the user to insert one pdf into another at a user-specified page.

![github_PDFEditor_Insert](https://user-images.githubusercontent.com/72211395/184698168-0933492e-2985-4581-be7d-b5ab3d6b6da6.png)

### Cutting

This tab allows the user to select a pdf and cut the page as specified.

![github_PDFEditor_Cut](https://user-images.githubusercontent.com/72211395/184698257-d3d51b58-c96f-4147-a104-54567b31c70f.png)

### Adding Bookmarks

This tab allows the user to Add a Bookmark to a selected pdf at a specified page number.

![github_PDFEditor_AddBookmark](https://user-images.githubusercontent.com/72211395/184698344-160cffc6-e8c0-4cd1-a20b-835546ca7bc5.png)

## User Instructions

1. Clone this project
2. Install **PySimpleGUI** and **PyPDF2** using *pip*  
``pip install PySimpleGUI``  
``pip install PyPDF2``  
3. Run the desired scripts as listed above
