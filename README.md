Go to Releases and download camil.exe

You can double click camil.exe and it will run with a default image.

Command to run with custom image: 
camil.exe img.png

Some strobing effect may look goofy depending on image used.

Recommended use, task scheduler:
* Search "Task Scheduler" in Windows search bar.
* Create Task (Not a Basic Task)
* Go to "Triggers" tab
* Click "New"
* Begin task: "On idle"
* Go to "Actions" tab
* Click "New"
* Program/Script: C:\path\to\camil.exe
* Arguments: C:\path\to\custom_img.png
