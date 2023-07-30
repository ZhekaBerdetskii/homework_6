import shutil
from pathlib import Path
import sys
from normalize import normalize

IMAGE = ['jpeg', 'png', 'jpg', 'svg']
VIDEO = ['avi', 'mp4', 'mov', 'mkv']
DOC = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
AUDIO = ['mp3', 'ogg', 'wav', 'amr']
ARCHIVE = ['zip', 'gz', 'tar']

image = []
video = []
documents = []
audio = []
archive = []
other = []

EXTENSION = set()
OTHER = set()


def read_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            if el.name in ('images', 'video', 'documents', 'audio', 'archive', 'other'):
                continue
            else:
                read_folder(el)
        else:
            move_file(el)


def move_file(file: Path):
    ext = file.suffix
    file_name = normalize(file.name.replace(ext, '')) + ext
    new_path = source / 'other'
    if ext[1:] in IMAGE:
        new_path = source / 'images'
        image.append(file_name)
        EXTENSION.add(ext[1:])
    elif ext[1:] in VIDEO:
        new_path = source / 'video'
        video.append(file_name)
        EXTENSION.add(ext[1:])
    elif ext[1:] in DOC:
        new_path = source / 'documents'
        documents.append(file_name)
        EXTENSION.add(ext[1:])
    elif ext[1:] in AUDIO:
        new_path = source / 'audio'
        audio.append(file_name)
        EXTENSION.add(ext[1:])
    elif ext[1:] in ARCHIVE:
        shutil.unpack_archive(file, source / 'archive' / file.name.replace(ext, ''))
        archive.append(file_name)
        EXTENSION.add(ext[1:])
        file.unlink()
    else:
        new_path = source / 'other'
        other.append(file_name)
        OTHER.add(ext[1:])
    if ext[1:] not in ARCHIVE:
        new_path.mkdir(exist_ok=True, parents = True)
        shutil.move(file, new_path / file_name)


def remove_empty_folders(path: Path):
    for el in path.iterdir():
        if el.is_dir() and el.name not in ('images', 'video', 'documents', 'audio', 'archive', 'other'):
            el.rmdir()


if __name__ == '__main__':
    try:
        source = Path(sys.argv[1])
        read_folder(source)
        remove_empty_folders(source)
        print(f'Images: {image}')
        print(f'Video: {video}')
        print(f'Documents: {documents}')
        print(f'Audio: {audio}')
        print(f'Archives: {archive}')
        print(f'Other: {other}')
        print(f'File extensions: {EXTENSION}')
        print(f'Unknown file extensions: {OTHER}')
    except IndexError:
        print('Please enter folder name to scan!')





