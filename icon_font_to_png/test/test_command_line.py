from __future__ import unicode_literals

import pytest
import os
import shutil

from icon_font_to_png import command_line


def test_list_option(capfd):
    """Test listing CSS icons"""
    css_file = os.path.join('files', 'test-foo.css')
    ttf_file = os.path.join('files', 'test.ttf')  # Required argument

    # No CSS and TTF files
    with pytest.raises(SystemExit):
        command_line.run(
            '--list'.split()
        )
    out, err = capfd.readouterr()
    assert out == ''

    # Lists correctly
    with pytest.raises(SystemExit):
        command_line.run(
            '--css {css_file} --ttf {ttf_file} --list'.format(
                css_file=css_file, ttf_file=ttf_file
            ).split()
        )
    out, err = capfd.readouterr()
    assert out == 'bar\ntest\n'

    # Lists correctly, with the prefix
    with pytest.raises(SystemExit):
        command_line.run(
            '--css {css_file} --ttf {ttf_file} --keep_prefix --list'.format(
                css_file=css_file, ttf_file=ttf_file
            ).split()
        )
    out, err = capfd.readouterr()
    assert out == 'foo-bar\nfoo-test\n'


def test_icon_export(capfd):
    """Test exporting icons (on Font Awesome files)"""
    css_file = os.path.join('files', 'font-awesome.css')
    ttf_file = os.path.join('files', 'fontawesome-webfont.ttf')

    # Export one icon
    command_line.run(
        '--css {css_file} --ttf {ttf_file} github'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'github.png'))

    # Export two icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} github star'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'github.png'))
    assert os.path.isfile(os.path.join('exported', 'star.png'))

    # Export all icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} ALL'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout


def test_filename_option(capfd):
    """Test whether """
    css_file = os.path.join('files', 'font-awesome.css')
    ttf_file = os.path.join('files', 'fontawesome-webfont.ttf')

    # Export one icon
    command_line.run(
        '--css {css_file} --ttf {ttf_file} '
        '--filename foo github'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'foo.png'))

    # Export multiple icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} '
        '--filename foo- github star'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'foo-github.png'))
    assert os.path.isfile(os.path.join('exported', 'foo-star.png'))


def teardown_module(module):
    """Delete exported icons directory"""
    if os.path.isdir('exported'):
        shutil.rmtree('exported')
