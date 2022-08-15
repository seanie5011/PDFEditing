import PySimpleGUI as sg
from pathlib import Path
from PDFEditing.EditPDF import PDFEditing


def sort_path_by_number(x, excluding_text=''):
    ''' Returns the int at the end of a pdf path, exluding suffix text
    x should be a path, excluding_text should be a string
    '''

    basename = str(x).split('\\')[-1]  # get basename from path
    basename_excluding = basename.removeprefix(excluding_text).removesuffix('.pdf')  # a 3.9+ feature

    if basename_excluding.isnumeric():
        return int(basename_excluding)
    else:
        return -1  # if the string after prefix removal is still not a number, make it return before all others


def main():
    tab1_layout = [
        [sg.Text('Prefix:'), sg.Input(key='-PREFIX_IP-', size=(24, 1))],
        [sg.Button('Import Folder', key='-INPUT_BTN-', expand_x=True)],
        [sg.Listbox('', key='-INPUTS_LST-', horizontal_scroll=True, size=(30, 10))],
        [sg.Button('Merge', key='-MERGE_BTN-', expand_x=True)]
        ]

    tab2_layout = [
        [sg.Button('Select Initial PDF', key='-INS_INITIAL_PDF_BTN-', expand_x=True)],
        [sg.Button('Select PDF to Insert', key='-INS_INSERT_PDF_BTN-', expand_x=True)],
        [sg.Text('Page Number to Insert PDF at:'), sg.Input(key='-INS_PAGE_NO_IP-', size=(3, 1))],
        [sg.VPush()],
        [sg.Button('Insert', key='-INSERT_BTN-', expand_x=True)]
        ]

    tab3_layout = [
        [sg.Button('Button')]
        ]

    tab4_layout = [
        [sg.Button('Button')]
        ]

    layout = [
            [sg.Button('Output Folder', key='-OUTPUT_BTN-', expand_x=True)],
            [sg.TabGroup([
                [sg.Tab('Merge', tab1_layout), sg.Tab('Insert', tab2_layout), sg.Tab('Cut', tab3_layout), sg.Tab('Add Bookmark', tab4_layout)]
                ])]
            ]

    window = sg.Window('PDF Editor', layout)

    output_folder_path = None
    pdf = PDFEditing()

    while True:
        event, values = window.read()
        print(values)

        if event == sg.WIN_CLOSED:
            break

        # Merge Tab
        if event == '-INPUT_BTN-':
            # get all pdf paths from folder
            input_folder_path = sg.popup_get_folder('Select Input Folder', no_window=True)
            path_list = list(Path(input_folder_path).glob("*.pdf"))  # gets all paths of pdf type and put into list

            # sort paths numerically, removing prefixes
            prefix = values['-PREFIX_IP-']
            path_list.sort(key=lambda x: sort_path_by_number(x, prefix))

            window['-INPUTS_LST-'].update(path_list)

        if event == '-MERGE_BTN-' and output_folder_path != None:
            pdf.reset()
            pdf.add_readers_from_list(path_list)

            pdf.write_to_file(output_folder_path)

        # Insert Tab
        if event == '-INS_INITIAL_PDF_BTN-':
            # get initial pdf path
            initial_pdf_path = Path(sg.popup_get_file('Select PDF', no_window=True, file_types=(("PDF Files", "*.pdf"),)))

        if event == '-INS_INSERT_PDF_BTN-':
            # get insert pdf path
            insert_pdf_path = Path(sg.popup_get_file('Select PDF', no_window=True, file_types=(("PDF Files", "*.pdf"),)))

        if event == '-INSERT_BTN-' and output_folder_path != None:
            # insert pdf into initial pdf
            pdf.reset()
            pdf.add_readers_from_list([initial_pdf_path])

            try:  # ensure page_number is of type int, if not dont do anything
                page_number = int(values['-INS_PAGE_NO_IP-'])
            except:
                print("ERROR: page_number not type int")
            else:
                pdf.insert_pdf(insert_pdf_path, page_number)
                pdf.write_to_file(output_folder_path)

        # Outside tabs
        if event == '-OUTPUT_BTN-':
            output_folder_path = sg.popup_get_folder('Select Output Folder', no_window=True)

    window.close()

if __name__ == '__main__':
    main()
