About
-----

This is a Python command-line script that creates a chart of mails from a maildir-format mailbox. It was designed to show an individual's activity over many years, by processing their sent-mail mailbox.

The main body of the chart is a scatterplot. The vertical axis is minutes, and the horizontal axis is days. Each pixel represents a minute. If that pixel is white, that means an email was sent in that minute. If you're sending more than one email per minute, you have bigger problems. 

The bottom of the chart is a histogram of days. Red is the raw histogram; overlaid on that is a rolling seven day average histogram.

The right side of the chart is a histogram of hours. Red is the raw histogram; overlaid on that is a rolling eleven minute average histogram.


Requirements
------------

Requires Python 2.6 or greater. Optionally, for timezone-corrected charts, the pytz module should be installed (http://pytz.sourceforge.net/).


Usage
-----

    ./mailboxchart.py -s 2001-01-01 path/to/maildir/ [path/to/other/maildir [...]]

Since Python's Maildir object returns messages un-sorted, you must supply a start date on the command line, using the `-s` option. All other command line options are optional.


### Options ###

    -h, --help            show this help message and exit
    -o OUTPUT_PATH, --output=OUTPUT_PATH
                          path to write output image to
    -f FONT_PATH, --font=FONT_PATH
                          path to TTF/OTF font file to use for labels
    --fontsize=FONT_SIZE  font size, in pixels (requires that -f FONT is
                          specified)
    -s START, --start=START
                          process emails starting on this date (required)
    -e END, --end=END     process emails before this date
    -z DISPLAY_TIMEZONE, --timezone=DISPLAY_TIMEZONE
                          draw chart using this timezone


### Example ###

I've had the same email since August 29th, 2000, and I'm usually in the `America/Los_Angeles` timezone, so I use this command:

   ./mailboxchart.py -z America/Los_Angeles -s 2000-08-29 ~/Maildir/.Sent/