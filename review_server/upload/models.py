from django.db import models
from .storage import OverwriteStorage
from filebrowser.fields import FileBrowseField
from filebrowser.signals import filebrowser_post_upload
import sys, zipfile, os, os.path
import shutil
from django.conf import settings
from zipfile import ZipFile
import glob

class Course(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    deletion_date = models.DateField()
    description = models.CharField(max_length=300)
    file = FileBrowseField("File", max_length=200, directory="shells/",  blank=True,
        null=True, help_text="Upload a SCORM Zip-File")
    path = models.CharField(max_length=200, editable=False)

    extract_path = ''

    def post_upload_callback(sender, **kwargs):
        """
        Signal receiver called each time an upload has finished.
        Triggered by Filebrowser's filebrowser_post_upload signal:
        http://code.google.com/p/django-filebrowser/wiki/signals .
        We'll use this to unzip .zip files in place when/if they're uploaded.
        """
        print("****** FILEBROWSER CALLBACK TRIGGERED ********")
        print(kwargs)
        print('####################################')

        if kwargs['file'].extension == ".zip":
            # Note: this doesn't test for corrupt zip files.
            # If encountered, user will get an HTTP Error
            # and file will remain on the server.
            # We get returned relative path names from Filebrowser

            path = kwargs['path']
            thefile = kwargs['file']
            print("************** " + str(thefile))
            # Convert file and dir into absolute paths
            fullpath = os.path.join(settings.MEDIA_ROOT, str(thefile))
            print(fullpath)

            with ZipFile(fullpath, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                global extract_path
                extract_path = os.path.join(settings.UNZIP_ROOT, str(thefile))
                # extract_path = os.path.join(settings.MEDIA_ROOT[:21], "test", str(thefile)[:-4])
                zipObj.extractall(extract_path[:-4])

    def save(self, *args, **kwargs):
        os.chdir(extract_path[:-4])
        for file in glob.glob("*.html"):
            print(file)

        self.path = extract_path[:-4]
        super().save(*args, **kwargs)

    # Signal provided by FileBrowser on every successful upload.
    filebrowser_post_upload.connect(post_upload_callback)


