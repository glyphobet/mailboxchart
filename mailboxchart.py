#!/usr/bin/env python
import sys
import time
import datetime
from mailbox import Maildir, MaildirMessage
import Image, ImageDraw, ImageFont

# Config
maildir_path = '~/Maildir/.Sent/'
output_path = 'mailboxchart.png'

font_path = '/home/matt/fonts/downloaded/inconsolata.otf'
font_size = 24
if font_path is not None:
    font = ImageFont.truetype(font_path, font_size)
else:
    font = ImageFont.load_default()

white = (0xff, 0xff, 0xff, 0xff)
black = (0, 0, 0, 0xff)
grey = (0x40, 0x40, 0x40, 0xff)
red = (0xff, 0x80, 0x80, 0xff)
background = grey
point = white

start = datetime.datetime(2000, 8, 29, 0, 0, 0)
tomorrow = datetime.date.today() + datetime.timedelta(1)
end = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)

display_timezone_name = 'America/Los_Angeles'
display_timezone = None
try:
    from pytz import timezone, utc
    display_timezone = timezone(display_timezone_name)
    start = display_timezone.localize(start)
    end = display_timezone.localize(end)
except ImportError:
    print("Install pytz (http://pytz.sourceforge.net/) for timezone-aware charts.\n")

# end Config

width = (end - start).days + 1
height = 24 * 60

scatterplot = Image.new('RGBA', (width, height), background)
pao = scatterplot.load()

count = 0

dayvolume = [0,] * width
minutevolume = [0,] * height

print("Reading sent mail and drawing scatterplot")

b = Maildir(maildir_path)
for m in b.itervalues():
    t = m.getdate_tz('Date')
    d = datetime.datetime.fromtimestamp(time.mktime(t[:9])) - datetime.timedelta(seconds=t[9])
    if display_timezone is not None:
        d = utc.localize(d).astimezone(display_timezone)
    if d < start:
        continue
    x = (d - start).days
    y = d.hour * 60 + d.minute
    try:
        pao[x, y] = point
    except:
        print x, y, width, height
    dayvolume[x] += 1
    minutevolume[y] += 1
    count += 1

print("Drawing day volume plot")

max_per_day = max(dayvolume)
dayvolumeplot = Image.new('RGBA', (width, max_per_day), white)
dayvolumedraw = ImageDraw.Draw(dayvolumeplot)
for x, d in enumerate(dayvolume):
    dayvolumedraw.line(((x,max_per_day  - d), (x, max_per_day)), fill=red)
    davg = sum(dayvolume[x-3:x+4]) / 7
    dayvolumedraw.line(((x,max_per_day  - davg), (x, max_per_day)), fill=background)
    if d == max_per_day:
        print d, 'emails sent on', start + datetime.timedelta(x)

print("Drawing minute volume plot")

max_per_min = max(minutevolume)
minvolumeplot = Image.new('RGBA', (max_per_min, height), white)
minvolumedraw = ImageDraw.Draw(minvolumeplot)
for y, m in enumerate(minutevolume):
    minvolumedraw.line(((0,y), (m, y)), fill=red)
    mrange = minutevolume[y-5:y+6]
    if (y<5):
        mrange = minutevolume[y-5:] + minutevolume[:y+6]
    if (height-y < 6):
        mrange += minutevolume[:(y + 6) % height]

    mavg = sum(mrange) / 11
    minvolumedraw.line(((0,y), (mavg, y)), fill=background)


offset = 32
image = Image.new('RGBA', (width + max_per_min + offset*3, height + max_per_day + offset*3), (0xff, 0xff, 0xff, 0xff))
image.paste(scatterplot, (offset, offset))
image.paste(dayvolumeplot, (offset, height + offset*2))
image.paste(minvolumeplot, (offset * 2 + width, offset))

d = ImageDraw.Draw(image)

y = start.year + 1
while y <= end.year:
    year = datetime.datetime(y, 1, 1)
    if display_timezone is not None:
        year = utc.localize(year).astimezone(display_timezone)
    x = (year - start).days + offset
    d.line(((x, 0              ), (x,          offset  )), fill=black)
    d.line(((x, height + offset), (x, height + offset*2)), fill=black)

    ts = font.getsize(str(y))
    d.text((x+182 - ts[0]/2,          offset / 2   - ts[1]/2), str(y), fill=black, font=font)
    d.text((x+182 - ts[0]/2, height + offset * 1.5 - ts[1]/2), str(y), fill=black, font=font)
    y += 1

for h in xrange(25):
    y = offset+h*60
    if h == 24:
        y -= 1
    d.line(((0             , y), (offset          , y)), fill=black)
    d.line(((width + offset, y), (width + offset*2, y)), fill=black)
    if h == 24:
        break
    hour = str((h-1) % 12 + 1)
    ts = font.getsize(hour)
    d.text((        offset*0.5 - ts[0]/2, y+30-ts[1]/2), hour, fill=black, font=font)
    d.text((width + offset*1.5 - ts[0]/2, y+30-ts[1]/2), hour, fill=black, font=font)

image.save(output_path)
print("%d total emails sent." % count)
