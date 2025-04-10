import argparse
import random
from pathlib import Path


def get_options():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--src-ds', type=str, nargs='+', default=[''])
    arg_parser.add_argument('--dst-ds', type=str, default='dst_dataset')
    arg_parser.add_argument('--train-split', type=float, default=0.9)
    arg_parser.add_argument('--training-structure', action='store_true', default=False)
    return arg_parser.parse_args()


def src_img_gen(src_ds, sub_folder):
    for ds in src_ds:
        for file in Path(ds).joinpath(sub_folder).iterdir():
            yield file


def copy_to_dst(dst_ds, src_ds, sub_folder):
    dst_folder = dst_ds.joinpath(sub_folder)
    dst_folder.mkdir(exist_ok=True, parents=True)

    for idx, file in enumerate(src_img_gen(src_ds, sub_folder), start=1):
        new_img_name = f'{idx:06d}.png'
        with open(dst_folder.joinpath(new_img_name), 'wb') as dst_file:
            with open(file, 'rb') as src_file:
                dst_file.write(src_file.read())


def copy_files(dst_ds, files):
    dst_folder = Path(dst_ds)
    dst_folder.mkdir(exist_ok=True, parents=True)

    for file in files:
        with open(dst_folder.joinpath(file.name), 'wb') as dst_file:
            with open(file, 'rb') as src_file:
                dst_file.write(src_file.read())


def main():
    opt = get_options()
    dst_ds = Path(opt.dst_ds)

    if opt.training_structure:
        patch_images = list(src_img_gen(opt.src_ds, 'patch'))
        random.shuffle(patch_images)
        patch_train_size = int(len(patch_images) * opt.train_split)
        train_patch_images = patch_images[:patch_train_size]
        val_patch_images = patch_images[patch_train_size:]

        copy_files(dst_ds.joinpath('train/patch'), train_patch_images)
        copy_files(dst_ds.joinpath('validation/patch'), val_patch_images)

        no_patch_images = list(src_img_gen(opt.src_ds, 'no_patch'))
        random.shuffle(no_patch_images)
        no_patch_train_size = int(len(no_patch_images) * opt.train_split)
        train_no_patch_images = no_patch_images[:no_patch_train_size]
        val_no_patch_images = no_patch_images[no_patch_train_size:]

        copy_files(dst_ds.joinpath('train/no_patch'), train_no_patch_images)
        copy_files(dst_ds.joinpath('validation/no_patch'), val_no_patch_images)
    else:
        copy_to_dst(dst_ds, opt.src_ds, 'patch')
        copy_to_dst(dst_ds, opt.src_ds, 'no_patch')


if __name__ == '__main__':
    main()
