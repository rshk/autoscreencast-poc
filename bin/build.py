#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
import os
import subprocess
import time

from jinja2 import Environment, FileSystemLoader

from PIL import Image
from selenium.webdriver import Firefox

HERE = os.path.dirname(__file__)
ROOTDIR = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOTDIR, 'output')
TMPDIR = os.path.join(ROOTDIR, 'tmp')
TEMPLATEDIR = os.path.join(ROOTDIR, 'templates')


@contextlib.contextmanager
def setup_browser():
    browser = Firefox()
    browser.set_window_size(1280, 800)
    # WORKAROUND for recordmydesktop bug
    browser.set_window_position(10, 10)
    yield browser
    browser.quit()


@contextlib.contextmanager
def screencast_browser(browser, outfile):
    ws = browser.get_window_size()
    wp = browser.get_window_position()
    command = [
        'recordmydesktop',
        '-x', str(wp['x']),
        '-y', str(wp['y']),
        '--width', str(ws['width']),
        '--height', str(ws['height']),
        '--no-sound', '--overwrite',
        '-o', outfile]
    proc = subprocess.Popen(command)
    yield proc
    proc.terminate()  # Will start encoding, then quit
    proc.wait()


def screenshot_element(browser, element, destfile, padding=10):
    tempfile = os.path.join(TMPDIR, 'screenshot.png')

    browser.save_screenshot(tempfile)
    rect = element.rect

    img = Image.open(tempfile)

    left = rect['x'] - padding
    top = rect['y'] - padding
    right = rect['width'] + rect['x'] + padding
    bottom = rect['height'] + rect['y'] + padding

    cropped = img.crop((left, top, right, bottom))

    with open(destfile, 'wb') as fp:
        cropped.save(fp, 'png')

    os.unlink(tempfile)


jinja_env = Environment(loader=FileSystemLoader(TEMPLATEDIR))


def render_template(name, context):
    template = jinja_env.get_template(name)
    return template.render(**context)


def run(ctx, browser):
    ctx['url'] = 'https://www.google.com'
    ctx['query'] = 'Hello world!'
    ctx['searchbox_screenshot'] = 'searchbox.png'
    ctx['button_screenshot'] = 'button.png'

    browser.get(ctx['url'])

    ctx['page_title'] = browser.title

    q = browser.find_element_by_name('q')
    btn = browser.find_element_by_name('btnK')

    ctx['button_text'] = btn.get_attribute('value')

    screenshot_element(
        browser, btn, os.path.join(OUTDIR, ctx['button_screenshot']),
        padding=0)

    time.sleep(2)
    q.send_keys(ctx['query'])
    screenshot_element(
        browser, q, os.path.join(OUTDIR, ctx['searchbox_screenshot']),
        padding=10)

    time.sleep(1)
    q.submit()
    # btn.click()

    time.sleep(5)

    return ctx


def main():
    ctx = {
        'video_path': 'screencast.ogv',
    }

    outfile = os.path.join(OUTDIR, ctx['video_path'])
    html_outfile = os.path.join(OUTDIR, 'index.html')

    with setup_browser() as browser:
        with screencast_browser(browser, outfile):
            ctx = run(ctx, browser)

    rendered = render_template('index.html', ctx)
    with open(html_outfile, 'wb') as fp:
        fp.write(rendered)

    print('Done. Now visit {}'.format(html_outfile))

if __name__ == '__main__':
    main()
