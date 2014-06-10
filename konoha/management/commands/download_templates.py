# coding=utf-8
import logging
from optparse import make_option
import requests
from path import path
from django.core.management.base import BaseCommand
from konoha.models import Page
from django.conf import settings



class Command(BaseCommand):
    args = '<directory>'
    help = 'Downloads Konoha templates, styles and images to the hard drive'

    def handle(self, *args, **options):
        settings.AWS_ACCESS_KEY_ID = r'AKIAJN53ZIKV4LC4OZCA'
        settings.AWS_SECRET_ACCESS_KEY = r'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'

        directory = path(args[0])

        img_dir = directory.joinpath('static/img').abspath()
        less_dir = directory.joinpath('static/css')
        yaml_dir = directory.joinpath('yaml')
        template_dir = directory.joinpath('templates')

        img_dir.makedirs_p()
        less_dir.makedirs_p()
        template_dir.makedirs_p()

        for page in Page.objects.all():
            page_less_path = less_dir.joinpath('%s.less' % page.name)
            with page_less_path.open('w') as less_file:
                print "Writing file: %s" % page_less_path
                less_file.write(page.style.encode('utf8'))

            page_yaml_path = yaml_dir.joinpath('%s.yaml' % page.name)
            with page_yaml_path.open('w') as yaml_file:
                print "Writing file: %s" % page_yaml_path
                yaml_file.write(page.data.encode('utf8'))

            page_template_path = template_dir.joinpath('%s.html' % page.name)
            with page_template_path.open('w') as template_file:
                print "Writing file: %s" % page_template_path
                template_file.write(page.template.encode('utf8'))

            page_img_dir = img_dir.joinpath(page.name)
            print "Page image dir: %s" % page_img_dir
            page_img_dir.makedirs_p()

            if page.image_folder:
                for image_obj in page.image_folder.all_files.all():
                    page_img_path = page_img_dir.joinpath(image_obj.label)
                    with open(page_img_path, 'wb') as img_file:
                        print "Downloading file %s to %s" % (image_obj.url, page_img_path)
                        r = requests.get("http:%s" % image_obj.url, stream=True)
                        if r.status_code == 200:
                            for chunk in r.iter_content():
                                img_file.write(chunk)
                        img_file.close()
