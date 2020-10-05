#!/usr/bin/python

import argparse
import re
import os
import os.path
import shutil
import glob
import time
import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from os import path
from pathlib import Path

# start timer to determine how long program takes to run
start_time = time.time()

# CONSTANTS - Override by entering command line args instead
# with command line arg overrides
PDFS_FOLDER = "/Volumes/Location/of/PDFs/Files/to/Batch/"                           # Override with -d
PDFS_FILENAME = ""                                                                  # Override with -i
PDFS_SUFFIX = "crop"                                                                # Override with -s
PDFS_FILTER = "Commercial Invoice"                                                  # Override with -f
PDFS_MERGE_OUTPUT = "pdf_crop_merge.pdf"                                            # Override with -o
PDFS_BOUNDING_BOX = [470.0, 748.0, 542.0, 140.0]                                    # Override with -b
PDFS_ARCHIVE_DIR = "Archived"                                                       # Override with -x


def create_parsers():
    p = argparse.ArgumentParser(
        prog='Crop PDF',
        description='"%(prog)s" leave args blank to use CONSTANTS instead.',
    )

    p.add_argument(
        '-i', '--input',
        type=str,
        # required=True,
        help='Input filename of single PDF',
    )

    p.add_argument(
        '-o', '--output',
        type=str,
        # required=True,
        help='Output filename of merged PDF',
    )

    p.add_argument(
        '-f', '--filter',
        type=str,
        # required=True,
        help='Do not crop pages containing this text',
    )

    p.add_argument(
        '-s', '--suffix',
        type=str,
        # required=True,
        help='Cropped PDF filename suffix',
    )

    p.add_argument(
        '-d', '--dir',
        type=str,
        # required=True,
        help='Directory to batch crop',
    )

    p.add_argument(
        '-b', '--bbox',
        type=float,
        nargs='*',
        # required=True,
        help='Bounding box [y0 y1 x0 x1]',
    )

    p.add_argument(
        '-v', '--verbose',
        action="store_true",
        help='Verbose Mode',
    )

    p.add_argument(
        '-m', '--merge',
        action="store_true",
        help='Create merged file of all cropped PDFs',
    )

    p.add_argument(
        '-r', '--rotate',
        action="store_true",
        help='Rotate all Portrait to Landscape',
    )

    p.add_argument(
        '-c', '--archivebymonth',
        action="store_true",
        help='Put archived PDFs in sub folders archived by month',
    )

    p.add_argument(
        '-a', '--archive',
        action="store_true",
        help='Move processed PDFs into a sub-directory',
    )

    p.add_argument(
        '-x', '--archivedirectory',
        type=str,
        help='Name of subdirectory for archive (NOTE: this is not an absolute path, just the name of a subdirectory)',
    )

    return p


def pluralize_text(number_input):
    if number_input > 1 or number_input == 0:
        return "s"
    else:
        return ""


def crop_shipping_label(pdf_file, file_suffix, text_filter, bounding_box):
    # if the file doesn't exist, exit the function
    try:
        input_file = PdfFileReader(open(pdf_file, "rb"))
    except OSError:
        return

    output_file = PdfFileWriter()

    numPages = input_file.getNumPages()

    i = 0
    for i in range(numPages):
        page = input_file.getPage(i)

        # Skip page if filtered text appears on that page.
        if text_filter:
            text_result = page.extractText()
            if re.search(text_filter,text_result):
                continue

        # trim the PDF
        page.trimBox.lowerLeft = (bounding_box[0], bounding_box[2])
        page.trimBox.upperRight = (bounding_box[1], bounding_box[3])
        page.cropBox.lowerLeft = (bounding_box[0], bounding_box[2])
        page.cropBox.upperRight = (bounding_box[1], bounding_box[3])

        # If Portrait, rotate to Landscape
        if args.rotate:
            if page.mediaBox.getUpperRight_x() - page.mediaBox.getUpperLeft_x() > page.mediaBox.getUpperRight_y() - page.mediaBox.getLowerRight_y():
                page.rotateCounterClockwise(90)

        output_file.addPage(page)

    # create a new file with suffix
    new_filename = pdf_file.replace(".pdf","-" + file_suffix + ".pdf")
    outputStream = open(new_filename, "wb")
    output_file.write(outputStream)
    numPagesnew = output_file.getNumPages()
    outputStream.close()

    if args.verbose:
        print(f"Converting: {pdf_file}")
        print(f"SUCCESS: Input has {numPages} page{pluralize_text(numPages)}, output has {numPagesnew} page{pluralize_text(numPagesnew)}.")

    # return the newly created filename as String
    return new_filename


# ------------------------------------------------------

def get_all_pdfs(folder_path):
    # return os.listdir(folder_path)

    file_list = []
    # add a / to the end of the path if it doesn't have one
    if not folder_path.endswith('/'):
        folder_path += '/'

    for filename in glob.glob(os.path.join(folder_path, '*.pdf')):
        # filename = filename.replace(input_directory,"")
        file_list.append(filename)

    return file_list

def get_single_pdf(file_name):
    single_pdf_file = "" # this is added only to avoid the name 'can be undefined' error
    try:
        single_pdf_file = PdfFileReader(open(file_name, "rb"))
    except OSError:
        print("ERROR: Input file not found")
        return

    return single_pdf_file


def get_absolute_path(file_name):
    return os.path.abspath(file_name)


if __name__ == '__main__':
    # check for command line arguments, if they don't exist use the constants instead.
    p = create_parsers()
    args = p.parse_args()

    if args.dir:
        input_directory = args.dir
    else:
        input_directory = PDFS_FOLDER

    if args.input:
        input_filename = args.input
    elif PDFS_FILENAME:
        input_filename = PDFS_FILENAME
    else:
        input_filename = ""

    if args.suffix:
        output_suffix = args.suffix
    else:
        output_suffix = PDFS_SUFFIX

    if args.output:
        output_filename = args.output
    else:
        output_filename = PDFS_MERGE_OUTPUT

    if args.filter:
        filtered_from_crop = args.filter
    else:
        filtered_from_crop = PDFS_FILTER

    if args.archivedirectory:
        archive_folder = args.archivedirectory
    else:
        archive_folder = PDFS_ARCHIVE_DIR

    if args.bbox:
        bounding_box_params = args.bbox
    else:
        bounding_box_params = [float(i) for i in PDFS_BOUNDING_BOX]

    # get list of pdfs from input_directory
    file_list = get_all_pdfs(input_directory)

    # get single pdf from input_filename if it exists
    if input_filename != "":
        if get_single_pdf(input_filename):
            file_list.append(get_absolute_path(input_filename))

    pdf_merger = PdfFileMerger()

    if args.archive:
        # prepare to move the processed PDF
        # check the directory to make sure it ends with a /
        if not archive_folder.endswith('/'):
            archive_folder += '/'

        # put the PDF in a subfolder broken down by month (ie: 2020-08)
        if args.archivebymonth:
            now = datetime.datetime.now()
            now_append = f'{now.year}-{now.month:02d}/'
            archive_folder += now_append

        # make sure the archive folder ends with a / but does not begin with a /
        if archive_folder.startswith('/'):
            archive_folder = archive_folder[1:]
        if not input_directory.endswith('/'):
            input_directory += '/'

        pdf_archived_path = input_directory + archive_folder

        # create the directory if it doesn't exist
        if not path.exists(pdf_archived_path):
            Path(pdf_archived_path).mkdir(parents=True, exist_ok=True)

    # run through the list of PDF files collected from both the directory and the single file

    successful_processed = 0
    successful_merged = 0
    for pdf_file in file_list:
        # don't re-crop already cropped files
        if pdf_file.endswith(output_filename) or pdf_file.endswith(output_suffix + '.pdf'):
            continue

        # crop the file and create new file
        new_pdf_file = crop_shipping_label(pdf_file, output_suffix, filtered_from_crop, bounding_box_params)
        successful_processed += 1

        if args.merge:
            # add to the merged PDF
            add_to_merge = open(new_pdf_file, "rb")
            pdf_merger.append(add_to_merge)
            successful_merged += 1

            # delete the individual cropped file
            os.remove(new_pdf_file)

        if args.archive:
            # move the file
            pdf_archived_path_file = pdf_file.replace(input_directory,input_directory + archive_folder)
            shutil.move(pdf_file, pdf_archived_path_file)
            if args.verbose: print(f"ARCHIVED: Moved PDF file to {pdf_archived_path_file}")

    if args.merge:
        # Write to an output PDF document
        if not input_directory.endswith('/'):
            input_directory += '/'
        merged_pdf_output = open(input_directory + output_filename, "wb")
        pdf_merger.write(merged_pdf_output)

    if args.verbose: print("-----------------------------------------------")
    if args.merge:
        if args.verbose:
            print(f"MERGED: Merged to file: {input_directory + output_filename}")
            print("-----------------------------------------------")
        else:
            print(f"MERGED: Merged {successful_processed} PDF file{pluralize_text(successful_processed)} into {successful_merged} page{pluralize_text(successful_processed)}.")
    print(f"BATCH CROP PDF SUCCESS: Cropped {successful_processed} PDF file{pluralize_text(successful_processed)} in {round(time.time() - start_time,2)} seconds.")
    if args.verbose: print("-----------------------------------------------")



