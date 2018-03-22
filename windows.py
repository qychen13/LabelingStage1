from PIL import Image, ImageTk

import os
import math
import numpy


class RatingWindow(object):
    def __init__(self, app):
        window_size = 600
        app.setSize([window_size, int(window_size * 1.1875)])

        app.setStretch('both')
        app.setSticky('nesw')
        # *************** Headline **************
        app.startFrame('headline')
        app.setStretch('both')
        app.setSticky('nesw')

        app.addLabel('user_id', 'User ID: {}'.format('xxxx'), 0, 0)
        app.addLabel('hf_l1', 'Total Progress:', 0, 2)
        app.addMeter('folder_progress', 0, 3, colspan=2)
        app.setMeterFill('folder_progress', 'blue')
        app.setMeter('folder_progress', 70)
        app.addLabel('group_id', 'Group ID: {}'.format('xxx'), 0, 5)

        app.stopFrame()

        # *************** Panel *****************

        app.startFrame('panel', rowspan=18)
        app.setStretch('both')
        app.setSticky('nesw')
        # =============== SubHeadline ============

        app.startPanedFrameVertical('sub_headline')
        app.setStretch('both')
        app.setSticky('nesw')
        app.addLabel('sf_l1', 'Group Progress:', 0, 0)
        app.addMeter('gp_progress', 0, 1)
        app.setMeter('gp_progress', 30)
        app.addLabel('img_id', 'Image ID: {}'.format('xxxx'), 0, 2)
        app.stopPanedFrame()

        # =============== Image ==================
        app.startPanedFrameVertical('image', rowspan=16)
        img = numpy.zeros([window_size, window_size, 3], dtype=numpy.uint8)
        img = Image.fromarray(img, 'RGB')
        photo = ImageTk.PhotoImage(img)
        app.addImageData('pic', photo, fmt='PhotoImage')
        app.stopPanedFrame()

        # =============== Button =================
        app.startPanedFrameVertical('rate', row=17)
        app.setStretch('both')
        app.setSticky('nesw')

        app.addLabel('r_l1', '')
        app.addButton('like', None, 0, column=1)
        app.addButton('dislike', None, 0, column=2)
        app.addLabel('r_l2', '', 0, column=3)
        app.stopPanedFrame()

        app.stopFrame()

        self.app = app
        self.window_size = window_size

    def set_group_id(self, group_id):
        self.app.setLabel('group_id', 'Group ID:{}'.format(group_id))

    def set_user_id(self, user_id):
        self.app.setLabel('user_id', 'User ID:{}'.format(user_id))

    def set_total_progress(self, progress):
        self.app.setMeter('folder_progress', progress)

    def set_group_progress(self, progress):
        self.app.setMeter('gp_progress', progress)

    def set_img(self, img_file):
        img_id = os.path.split(img_file)[1]
        img_id = os.path.splitext(img_id)[0]
        self.app.setLabel('img_id', 'Image ID:{}'.format(img_id))
        img = Image.open(img_file)
        img.thumbnail((self.window_size, self.window_size))
        photo = ImageTk.PhotoImage(img)
        self.app.setImageData('pic', photo, fmt='PhotoImage')


class SelectWindow(object):
    def __init__(self, app, img_folder, imgs):
        self.coln = 5
        self.window_size = [1000, 500]
        self.selections = None
        self.app = app
        self.img_folder = img_folder
        self.imgs = imgs

    def select_imgs(self, img_files):
        # **************** Image Panel *****************
        app = self.app
        app.startSubWindow('Selection', modal=True, blocking=True).protocol('WM_DELETE_WINDOW', lambda: exit(-1))
        app.setSize(self.window_size)
        app.setStretch('both')
        app.setSticky('nesw')

        img_num = len(img_files)
        self.selections = [True] * img_num
        self.imgs = img_files
        rows = math.ceil(img_num / self.coln)
        app.startScrollPane('images', rowspan=5)
        count = 0
        for r in range(rows):
            for c in range(self.coln):
                if count < img_num:
                    img_file = os.path.join(self.img_folder, self.imgs[count])
                    photo = Image.open(os.path.join(img_file))
                    photo.thumbnail((self.window_size[0] // self.coln, self.window_size[0] // self.coln))
                    photo = ImageTk.PhotoImage(photo)
                    app.addImageData('pic{}'.format(count), photo, r, c, fmt='PhotoImage')
                    count += 1
        app.stopScrollPane()

        # **************** Buttons **********************
        app.startPanedFrameVertical('selection_buttons', row=5, rowspan=1)
        app.setStretch('both')
        app.setSticky('nesw')
        app.addLabel('selection_warning', '', colspan=3)
        app.addLabel('st_l1', '', 1, 0)
        app.addButton('submit', None, 1, 1)
        app.addLabel('st_l2', '', 1, 2)
        app.stopPanedFrame()

        app.stopSubWindow()

    def set_img_folder(self, folder):
        self.img_folder = folder

    def reload_img(self, img):
        img_id = int(img[3:])
        img_file = os.path.join(self.img_folder, self.imgs[img_id])
        photo = Image.open(os.path.join(img_file))
        photo.thumbnail((self.window_size[0] // self.coln, self.window_size[0] // self.coln))
        if self.selections[img_id]:
            photo = photo.convert('L')
        photo = ImageTk.PhotoImage(photo)
        self.app.setImageData(img, photo, fmt='PhotoImage')
        self.selections[img_id] = not self.selections[img_id]

    def count_selections(self):
        count = 0
        for s in self.selections:
            if s:
                count += 1
        return count


class LoginWindow(object):
    def __init__(self, app):
        app.startSubWindow('Login', modal=True).protocol('WM_DELETE_WINDOW', lambda: exit(-1))

        app.addLabelEntry('username')
        app.addButton('login', None)

        app.stopSubWindow()
        self.app = app


class WarningWindow(object):
    def __init__(self, app):
        app.startSubWindow('warning', modal=True)
        app.setsize([500, 500])
        app.setStretch('both')
        app.setSticky('nesw')
        app.addMessage('warning_message', None)
        app.stopSubWindow()
        self.app = app

    def show_message(self, mess):
        self.app.setMessage('warning_message', mess)
        self.app.showSubWindow('warning')
