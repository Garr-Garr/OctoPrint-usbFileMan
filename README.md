# OctoPrint-usbFileMan

usbFileMan is intended to allow easy control and interaction with USB flashdrives inserted into a computer running OctoPrint.  The primary goal is to allow a user to plug in a USB flashdrive, and choose what to do - what files to copy, where to, etc.

Initial version responds to an API get by looking at the folder "/media/usb1/toprint", and comparing the files there to the files in "/home/pi/.octoprint/uploads/USB".  If there are new files, they are copied over, and the file in ../toprint is prefixed with "COPIED"; if there is a file with the same name as one that already exists, but a different MD5 hash, the new different file is copied to ../USB with a datetime string appended to the filename (before extension, to ensure OctoPrint recognizes the file correctly), and again the original is prefixed with "COPIED".  Finally, OctoPrint's UpdatedFiles event is triggered, so any clients or plugins subscribed to that event will be alerted and can act; this is most useful for the normal OctoPrint client, as this triggers the filelist to refresh.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/MakerGear/OctoPrint-usbFileMan/archive/refs/heads/installer.zip

The computer running OctoPrint needs to be configured to automatically mount USB flashdrives to /media/usb1 (right now).  All testing, and the only currently targeted system, is a Raspberry Pi 3B/3B+ running OctoPi 0.15.1 .

Current best instructions for this process are here: https://raspberrypi.stackexchange.com/a/66324 .  The /usr/local/bin/cpmount file needs two changes - it needs to also trigger the OctoPrint-usbFileMan api, and to be executable (per GeertVc's comment on that post).  Current best option for triggering is to add to line 23, as second to last line of the file, before "fi":

`sudo -u pi /home/pi/oprint/bin/octoprint client get '/api/plugin/usbfileman'`

That will trigger OctoPrint's cli client functionality to perform the API get against usbFileMan.  If you anticipate connecting multiple flashdrives, add that line to each "else" statement, below the call to /usr/bin/pmount .

To make that file executable:

`sudo chmod u+x /usr/local/bin/cpmount`

ntfs-3g may need to be installed to support NTFS formatted drives:

`sudo apt-get install ntfs-3g`

## Configuration

**TODO:** Describe your plugin's configuration options (if any).
