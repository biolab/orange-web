import os
from django.conf import settings
from django.template import Template, Context

from django.test import TestCase
from django.test.utils import override_settings
from homepage.templatetags.tag_extras import download_choices

base_dir = os.path.abspath(os.path.dirname(__file__))
TEST_DOWNLOAD_SET_PATTERN = os.path.join(base_dir, 'filenames_%s.set')


@override_settings(DOWNLOAD_SET_PATTERN=TEST_DOWNLOAD_SET_PATTERN)
class TestDownloadChoices(TestCase):
    def test_download_choices_win(self):
        downloads = download_choices('win')

        self.assertIn('win27', downloads)
        self.assertEqual('WIN_SNAPSHOT-py2.7.exe', downloads['win27'])

        self.assertIn('winw27', downloads)
        self.assertEqual('WIN_PYTHON_SNAPSHOT-py2.7.exe', downloads['winw27'])

        self.assertIn('bio27', downloads)
        self.assertEqual('ADDON_BIOINFORMATICS_SNAPSHOT-py2.7.exe',
                         downloads['bio27'])

        self.assertIn('text27', downloads)
        self.assertEqual('ADDON_TEXT_SNAPSHOT-py2.7.exe', downloads['text27'])

    def test_download_choices_mac(self):
        downloads = download_choices('mac')

        self.assertIn('mac', downloads)
        self.assertEqual('MAC_DAILY', downloads['mac'])

        self.assertIn('bundle-orange3', downloads)
        self.assertEqual('MAC_ORANGE3_DAILY', downloads['bundle-orange3'])


@override_settings(DOWNLOAD_SET_PATTERN=TEST_DOWNLOAD_SET_PATTERN)
class TestDownloadLink(TestCase):
    def test_win(self):
        template = Template("""
{% load tag_extras %}
{% download_link 'windows' %}
        """)
        self.assertEqual('WIN_PYTHON_SNAPSHOT-py2.7.exe',
                         template.render(Context()).strip())

        settings.DOWNLOAD_SET_PATTERN = ''
        self.assertEqual('', template.render(Context()).strip())

    def test_osx(self):
        template = Template("""
{% load tag_extras %}
{% download_link 'mac-os-x' %}
        """)
        self.assertEqual('MAC_DAILY', template.render(Context()).strip())

        settings.DOWNLOAD_SET_PATTERN = ''
        self.assertEqual('', template.render(Context()).strip())

    def test_linux(self):
        template = Template("""
{% load tag_extras %}
{% download_link 'linux' %}
        """)
        self.assertEqual('SOURCE_SNAPSHOT',
                         template.render(Context()).strip())

        settings.DOWNLOAD_SET_PATTERN = ''
        self.assertEqual('', template.render(Context()).strip())

    def test_other(self):
        template = Template("""
{% load tag_extras %}
{% download_link 'other' %}
        """)
        self.assertEqual('WIN_SNAPSHOT', template.render(Context()).strip())

        settings.DOWNLOAD_SET_PATTERN = ''
        self.assertEqual('', template.render(Context()).strip())
