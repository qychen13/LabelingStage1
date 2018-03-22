import windows
from appJar import gui

import os
import datetime
import collections

# ============= Settings ================
user_id = ''
img_folder = 'imgs'
log_folder = 'logs'
img_folder_checklist_file = 'img-folder-checklist.txt'
img_folder_checklist = collections.OrderedDict()
img_subfolders = []
cur_folder = -1
group_imgs = None
cur_img = -1
like_imgs = []
max_selection_num = 15
min_selection_num = 5


def main():
    # load image folder to rate
    with open(img_folder_checklist_file, 'r') as f:
        for line in f:
            folder, mark = line.split()
            if mark == '0':
                img_subfolders.append(folder)
            img_folder_checklist[folder] = mark
    img_subfolders.sort()

    # start gui and init windows
    app = gui('Rating')
    rating_win = windows.RatingWindow(app)
    selection_win = windows.SelectWindow(app, img_folder, group_imgs)
    login_win = windows.LoginWindow(app)
    warning_win = windows.WarningWindow(app)

    # ================= Help Functions ===========

    def log_like_imgs():
        global like_imgs
        today = datetime.date.today()
        log_file = '{}-{:02d}{:02d}.txt'.format(user_id, today.month, today.day)
        with open(os.path.join(log_folder, log_file), 'a') as f:
            for img_id in like_imgs:
                f.write(img_id + '\n')
        like_imgs = []

    def next_group():
        global cur_folder
        global group_imgs
        global cur_img

        if cur_folder != -1:
            img_folder_checklist[img_subfolders[cur_folder]] = '1'
            with open(img_folder_checklist_file, 'w') as f:
                for folder, mark in img_folder_checklist.items():
                    f.write('{} {}\n'.format(folder, mark))
            log_like_imgs()
        cur_folder += 1
        if cur_folder == len(img_subfolders):
            exit(1)
        group_imgs = [img for img in os.listdir(os.path.join(img_folder, img_subfolders[cur_folder])) if
                      img.endswith('.jpg')]
        group_imgs.sort()
        rating_win.set_group_id(img_subfolders[cur_folder])
        rating_win.set_group_progress(0)
        rating_win.set_total_progress(cur_folder / len(img_subfolders) * 100)

        cur_img = -1
        next_image()

    def next_image():
        global cur_img
        global like_imgs

        cur_img += 1
        if cur_img == len(group_imgs):
            if len(like_imgs) > max_selection_num:
                selection_win.set_img_folder(os.path.join(img_folder, img_subfolders[cur_folder]))
                selection_win.select_imgs(like_imgs)
                for i in range(len(like_imgs)):
                    app.setImageSubmitFunction('pic{}'.format(i), selection_callback)
                app.setButtonSubmitFunction('submit', submit_callback)
                app.showSubWindow('Selection')
            elif len(like_imgs) < min_selection_num:
                warning_win.show_message('Selected images are less than 5. Go back to the group again.')
                like_imgs = []
                cur_img = -1
                next_image()
            else:
                next_group()
        else:
            rating_win.set_group_progress(cur_img / len(group_imgs) * 100)
            rating_win.set_img(os.path.join(img_folder, img_subfolders[cur_folder], group_imgs[cur_img]))

    # ============ Callback Functions ============
    def like_callback(btn):
        global like_imgs

        like_imgs.append(group_imgs[cur_img])
        next_image()

    def dislike_callback(btn):
        next_image()

    def login_callback(btn):
        global user_id
        user_id = app.getEntry('username')
        rating_win.set_user_id(user_id)
        gui.trace("Showing topLevel")
        app.destroySubWindow('Login')
        app._bringToFront()
        app.topLevel.deiconify()

    def selection_callback(img):
        selection_win.reload_img(img)

    def submit_callback(btn):
        global like_imgs
        count = selection_win.count_selections()
        if count >= min_selection_num and count <= max_selection_num:
            selection = selection_win.selections
            select_imgs = [like_imgs[i] for i in range(len(selection)) if selection[i]]
            like_imgs = select_imgs
            app.destroySubWindow('Selection')
            next_group()
        else:
            app.setLabel('selection_warning', 'Warning: Selection number should be within {} and {}!. You have chosen {}.'.format(max_selection_num, min_selection_num, count))

    def init_callback():
        app.setButtonSubmitFunction('like', like_callback)
        app.setButtonSubmitFunction('dislike', dislike_callback)
        app.setButtonSubmitFunction('login', login_callback)

    # =============================================
    init_callback()
    next_group()
    app.go(startWindow='Login')


if __name__ == '__main__':
    main()
