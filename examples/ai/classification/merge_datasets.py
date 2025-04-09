import argparse
from pathlib import Path


def get_options():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--src-ds', type=str, nargs='+', default=[''])
    arg_parser.add_argument('--dst-ds', type=str, default='dst_dataset')
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


def main():
    opt = get_options()
    dst_ds = Path(opt.dst_ds)
    copy_to_dst(dst_ds, opt.src_ds, 'patch')
    copy_to_dst(dst_ds, opt.src_ds, 'no_patch')


if __name__ == '__main__':
    main()
