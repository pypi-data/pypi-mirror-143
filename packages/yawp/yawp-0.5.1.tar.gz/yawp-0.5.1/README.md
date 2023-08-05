```
usage: yawp [-h] [-H] [-V] [-v] [-U] [-N] [-p] [-w CHARS_PER_LINE] [-l] [-g]
            [-c CONTENTS_TITLE] [-i INDEX_TITLE] [-m MAX_SUBJECT] [-f] [-F]
            [-e EVEN_LEFT] [-E EVEN_RIGHT] [-o ODD_LEFT] [-O ODD_RIGHT] [-a]
            [-P FILE_PDF] [-W CHAR_WIDTH] [-A CHAR_ASPECT] [-S PAPER_SIZE]
            [-Z] [-Q PRINT_QUALITY] [-L LEFT_MARGIN] [-R RIGHT_MARGIN]
            [-T TOP_MARGIN] [-B BOTTOM_MARGIN] [-b] [-s] [-k]
            [file]

Yet Another Word Processor, an automatic word processor for text files, with PDF output

                       I sound my barbaric yawp over the roofs of the world

                                                               Walt Whitman

The  name  "yawp"  here  means  Yet  Another Word Processor, and yawp is an
automatic word processor for plain text files, with PDF output. If you want
to quickly create a no-frills but well-formatted document, you can:

    • edit a text file by your favorite editor
    • run yawp in order to:
        • backup read format and rewrite the text file
        • export the text file in a PDF file
        • open the PDF file for check or print
    • go back to the editor and update the text file or finish

The following flowchart illustrates inputs and outputs:

    ┌───────────┐                       ┌───────────┐
    │           │       ┌───────┐ read  │           │       ┌───────┐
    │           │ edit  │ text  ├──────▷│           │export │ PDF   │
    │  editor   ├──────▷│       │rewrite│   yawp    ├──────▷│       │
    │           │       │ file  │◁──────┤           │       │ file  │
    │           │       └───────┘       │           │       └───────┘
    └───────────┘                       └───┬───────┘
                                            │   △
                                            │   │
                                     backup │   │ restore (undo)
                                            │   │
                                            ▽   │
                                          ┌─────┴─┐
                                          │backup │
                                          │       │
                                          │ file  │
                                          └───────┘

Main features are:

    • yawp  processes  in place a single text file, hereinafter referred to
      simply as the "file"
    • yawp  before  processing  makes  a  timestamped  backup  of the file,
      allowing undo operation
    • yawp  processing  is  driven by the text in the file and by arguments
      only, not by commands or tags embedded in text
    • yawp justifies text at left and right in:
        • unindented paragraphs
        • dot-marked indented paragraphs (as this one)
    • yawp  accepts  unjustified  pictures  (as  schemas,  tables  and code
      examples) freely intermixed with text
    • you can sketch in pictures segments (by '`') and arrowheads (by '^'),
      yawp redraws them by proper graphic characters
    • yawp  adopts  an  ad  hoc  policy  for  Python  files, formatting the
      docstrings but not the Python code
    • yawp performs multi-level chapter renumbering
    • yawp inserts an automatic contents chapter in the file
    • yawp  recognizes  relevant  subjects  (quoted  by '"') and inserts an
      automatic index chapter in the file
    • yawp cuts the file in pages, by automatic insertion of two-lines page
      headers
    • yawp  exports  the  resulting  lines in PDF format, with control over
      character  size  and page layout, and opens for you the generated PDF
      file, allowing preview and printing
    • yawp  corrects  errors  made  by  CUPS-PDF  about  font size and page
      margins
    • yawp is "stable", namely if after a yawp execution you run yawp again
      on  the  same  file  with  the  same  arguments then the file content
      doesn't change (except date and time in page headers)
    • as  a  beta  release, yawp 0.5.1. contains some debug functionalities
      not aimed at the end user, they will disappear in some future release

To install, for example on a Debian-derived Linux, type:

    $ sudo apt-get -y update
    $ sudo apt-get -y install printer-driver-cups-pdf
    $ pip3 install -U yawp

For any detail, see the yawp-generated "yawp Manual" by typing:

    $ yawp -H

positional arguments:
  file                  text file to be processed

optional arguments:
  -h, --help            show this help message and exit
  -H, --manual          open yawp Manual in PDF format and exit
  -V, --version         show program's version number and exit
  -v, --verbose         display information messages on stderr
  -U, --undo            restore the file from its previous version
  -N, --no-format       leave the file unchanged
  -p, --print-file      at end print file on stdout
  -w CHARS_PER_LINE, --chars-per-line CHARS_PER_LINE
                        line width in chars per line (default: 0 = automatic)
  -l, --left-only       justify at left only (default: left and right)
  -g, --graphics        redraw '`'-segments and '^'-arrowheads
  -c CONTENTS_TITLE, --contents-title CONTENTS_TITLE
                        title of contents chapter (default: 'contents')
  -i INDEX_TITLE, --index-title INDEX_TITLE
                        title of index chapter (default: 'index')
  -m MAX_SUBJECT, --max-subject MAX_SUBJECT
                        max index subject length (default: 36)
  -f, --formfeed        insert page headers on full page
  -F, --formfeed-chapters
                        insert page headers on full page and before contents
                        index and level-one chapters
  -e EVEN_LEFT, --even-left EVEN_LEFT
                        even page headers, left (default: '%n/%N')
  -E EVEN_RIGHT, --even-right EVEN_RIGHT
                        even page headers, right (default: '%f.%e %Y-%m-%d
                        %H:%M:%S')
  -o ODD_LEFT, --odd-left ODD_LEFT
                        odd page headers, left (default: '%c')
  -O ODD_RIGHT, --odd-right ODD_RIGHT
                        odd page headers, right (default: '%n/%N')
  -a, --all-headers-E-e
                        all page headers contain -E at left and -e at right
  -P FILE_PDF, --file-PDF FILE_PDF
                        file name of exported PDF file (0 = no PDF export,
                        default: '%P/%f.pdf')
  -W CHAR_WIDTH, --char-width CHAR_WIDTH
                        character width (pt/in/mm/cm, default: 0 = automatic)
  -A CHAR_ASPECT, --char-aspect CHAR_ASPECT
                        char aspect ratio = char width / char height (1 =
                        square grid, default: 3/5')
  -S PAPER_SIZE, --paper-size PAPER_SIZE
                        portrait paper size (width x height, pt/in/mm/cm,
                        default: 'A4' = '210x297mm'
  -Z, --landscape       turn page by 90 degrees (default: portrait)
  -Q PRINT_QUALITY, --print-quality PRINT_QUALITY
                        print quality (0 1 or 2, default: 2')
  -L LEFT_MARGIN, --left-margin LEFT_MARGIN
                        left margin (pt/in/mm/cm, 2cm..8cm, default: 2cm)
  -R RIGHT_MARGIN, --right-margin RIGHT_MARGIN
                        right margin (pt/in/mm/cm, 2cm..8cm, default: -L)
  -T TOP_MARGIN, --top-margin TOP_MARGIN
                        top margin (pt/in/mm/cm, 2cm..8cm, default: 2cm)
  -B BOTTOM_MARGIN, --bottom-margin BOTTOM_MARGIN
                        bottom margin (pt/in/mm/cm, 2cm..8cm, default: -T)
  -b, --dump-buffer     debug, dump content of internal buffer
  -s, --echo-shell      debug, display invoked Unix commands
  -k, --calibration     debug, don't adjust char size and page margins
```
