def merge_task_results(task_results: list[dict]):
    combined_task_result = {'created': 0, 'updated': 0, 'removed': 0, 'skipped': 0}
    for task_result in task_results:
        combined_task_result['created'] += task_result['created']
        combined_task_result['updated'] += task_result['updated']
        combined_task_result['removed'] += task_result['removed']
        combined_task_result['skipped'] += task_result['skipped']
    return combined_task_result
