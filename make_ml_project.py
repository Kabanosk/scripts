import argparse
from pathlib import Path
from shutil import copyfile
from git import Repo

def parse_arguments():
    parser = argparse.ArgumentParser("Script which make structure for ml projects")
    parser.add_argument(
        '--name', '-n',
        required=True,
        type=str,
        help='Name of the project',
    )
    parser.add_argument(
        '--destination', '-d',
        default=Path('.'),
        type=Path,
        help='Destination where the files will be created'
    )
    parser.add_argument(
        '-f',
        action='store_true',
        help='Make destination directory if not exists'
    )
    parser.add_argument(
        '--github_url', '-gh',
        type=str,
        help='Add files to remote repository on Github'
    )
    parser.add_argument(
        '--without_git',
        action='store_false',
        help='Create files without git repository'
    )
    return parser.parse_args()


def make_folders(base_folder):
    data_dir = base_folder / 'data'
    src_dir = base_folder / 'src'
    generated_models_dir = base_folder / 'models'

    data_generation_dir = src_dir / 'data'
    model_generation_dir = src_dir / 'models'

    src_dir.mkdir(parents=True)
    data_dir.mkdir()
    generated_models_dir.mkdir()
    model_generation_dir.mkdir()
    data_generation_dir.mkdir()


def make_files(base_folder):
    requirements_path = base_folder / 'requirements.txt'
    gitignore_path = base_folder / '.gitignore'
    license_path = base_folder / 'LICENCE'
    readme_path = base_folder / 'README.md'

    init_path = base_folder / 'src' / '__init__.py'
    model_path = base_folder / 'src' / 'models' / 'model.py'
    gen_dataset_path = base_folder / 'src' / 'data' / 'get_dataset.py'

    requirements_path.touch()
    gitignore_path.touch()
    license_path.touch()
    readme_path.touch()

    init_path.touch()
    model_path.touch()
    gen_dataset_path.touch()

    copyfile(Path('scripts/LICENCE'), license_path)


def initialize_git(base_folder, url):
    repo = Repo.init(base_folder)

    paths = ['requirements.txt', 'LICENCE', 'README.md', '.gitignore',
             'src/__init__.py', 'src/models/model.py',
             'src/data/get_dataset.py', 'models/', 'data/']

    for path in paths:
        repo.index.add(path)
    repo.index.commit("Add structure files")

    if url:
        repo.create_remote('origin', url)
        repo.remotes.origin.push('main:main')


if __name__ == '__main__':
    args = parse_arguments()
    assert (
        args.destination.exists() or args.f
    ), f"Destination '{args.destination}' doesn't exists"

    base_dir = args.destination / args.name

    make_folders(base_dir)
    make_files(base_dir)

    initialize_git(base_dir, args.github_url)



