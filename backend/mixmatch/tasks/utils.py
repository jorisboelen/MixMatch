from mimetypes import guess_extension
from mixmatch.core.settings import settings
from mixmatch.file import MixMatchFileCover
from os.path import basename, join
from uuid import uuid4


def merge_task_results(task_results: list[dict]) -> dict:
    combined_task_result = {'created': 0, 'updated': 0, 'removed': 0, 'skipped': 0}
    for task_result in task_results:
        combined_task_result['created'] += task_result['created']
        combined_task_result['updated'] += task_result['updated']
        combined_task_result['removed'] += task_result['removed']
        combined_task_result['skipped'] += task_result['skipped']
    return combined_task_result


def save_cover(cover: MixMatchFileCover) -> str:
    if cover and guess_extension(cover.mime, strict=False):
        cover_file_extension = guess_extension(cover.mime, strict=False)
        cover_file = open(join(settings.IMAGE_DIRECTORY, str(uuid4()) + cover_file_extension), 'wb')
        cover_file.write(cover.data)
        cover_file.close()
        return basename(cover_file.name)
    else:
        return ''
