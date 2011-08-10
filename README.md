About
-----

This is a Python command-line script that creates a chart of mails from local Maildir format mailboxes or IMAP4 SSL mailboxes. It was designed to show an individual's activity over many years, by processing their sent-mail mailbox.

The main body of the chart is a scatterplot. The vertical axis is minutes, and the horizontal axis is days. Each pixel represents a minute. If that pixel is white, that means an email was sent in that minute. If you're sending more than one email per minute, you have bigger problems.

The bottom of the chart is a histogram of days. Red is the raw histogram; overlaid on that is a rolling seven day average histogram.

The right side of the chart is a histogram of hours. Red is the raw histogram; overlaid on that is a rolling eleven minute average histogram.


Requirements
------------

Requires Python 2.6 or greater. Optionally, for timezone-corrected charts, the pytz module should be installed (http://pytz.sourceforge.net/).


Usage
-----

    ./mailboxchart.py -s 2001-01-01 [OPTIONS] maildir_or_imaps_url [maildir_or_imaps_url [...]]

You may process as many Maildirs or IMAP4 mailboxes as you like, using a single command, and all the mails will be assembled on the same chart. You'll be prompted for IMAP passwords for each IMAP URL.

Only IMAP4 over SSL is supported. (If you really want to send your authentication and entire mailbox unencrypted over the Internets you can hack the code easily enough, but I'm not going to enable you.)

Since mailboxes might contain un-sorted messages, you must supply a start date on the command line, using the `-s` option. All other command line options are optional.


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
    --noninteractive      disable progress meter


### Example ###

I've had the same email since August 29th, 2000, and I'm usually in the `America/Los_Angeles` timezone, and my sent-mail is in `~/Maildir/.Sent/`, so I use this command:

    ./mailboxchart.py -s 2000-08-29 -z America/Los_Angeles ~/Maildir/.Sent/

Alternatively, if you'd like to process a remote Gmail mailbox over IMAP4, you may supply an `imaps://` URL. (Note that `USERNAME` must be URL-encoded, so if it has an `@` sign in it, that gets turned into `%40`.)

    ./mailboxchart.py -s 2001-01-01 'imaps://USERNAME@imap.gmail.com/"[Gmail]/Sent Mail"'

