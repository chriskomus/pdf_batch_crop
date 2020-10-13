# Batch Crop, Merge, and Move PDFs

- Easily crop single PDFs, or batch crop entire directories
- Merge batched PDFs all into one PDF
- Filter out pages if they contain a custom string
- Move/Archive original PDFs to a subdirectory after they have been processed
- Subdirectory archive folders can be broken down by month (ie: 2020-08)
- Rotate Portrait to Landscape (useful for shipping labels that are printed on 8.5" x 11")
- Set a custom filename suffix for cropped PDFs
- Set a custom name for merged PDFs
- Set a custom sub-directory for Archived PDFs
- Use command line arguments in a command batch file, or constant variables set in the .py file for easier routine batch jobs.
- Fast! Completely dependent on the PDF content and hardware specs but it should crop, merge, and archive 100 Shipping Label PDFs in about 3-5 seconds.

## Ideal for Cropping 8.5" x 11" Shipping Labels to 4" x 6" Thermal Labels.

- This was created specifically to Crop Shipping Labels from 8.5" x 11" to 4" x 6" Mailing Thermal Labels.
- The default settings are designed to automatically crop Canada Post 8.5" x 11" shipping labels to 4" x 6" Mailing Thermal Labels.

## Help

#### Optional Arguments:
- -h, --help **(show this help message and exit)**
- -i INPUT **(Input filename of single PDF)**
- -o OUTPUT **(Output filename of merged PDF)**
- -f FILTER **(Do not crop pages containing this text)**
- -s SUFFIX **(Cropped PDF filename suffix)**
- -d DIR **(Directory to batch crop)**
- -x ARCHIVEDIRECTORY **(Name of subdirectory for archive (NOTE: this is not an absolute path, just the name of a subdirectory))**
- -b **(Bounding box [y0 y1 x0 x1])**

#### toggles:                
- -v, --verbose         **(Verbose Mode)**
- -m, --merge           **(Create merged file of all cropped PDFs)**
- -a, --archive         **(Move processed PDFs into a sub-directory)**
- -r, --rotate          **(Rotate all Portrait to Landscape)**
- -c, --archivebymonth  **(Put archived PDFs in sub folders archived by date)**                

# Requires PyPDF2

You will need to get PyPDF2 up and running first.

`pip install PyPDF2`

PyPDF2 is a pure-python PDF library capable of splitting, merging together, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. It can retrieve text and metadata from PDFs as well as merge entire files together.

Homepage  
http://mstamy2.github.io/PyPDF2/
