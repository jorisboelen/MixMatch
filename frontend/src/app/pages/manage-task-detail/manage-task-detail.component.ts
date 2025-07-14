import { Component } from '@angular/core';
import { DatePipe, NgFor, NgIf } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { MixMatchService } from '../../services/mixmatch.service';
import { Task, TaskResult } from '../../interfaces';

@Component({
    selector: 'app-manage-task-detail',
    imports: [DatePipe, NgFor, NgIf],
    templateUrl: './manage-task-detail.component.html',
    styleUrl: './manage-task-detail.component.css'
})
export class ManageTaskDetailComponent {
  task?: Task;

  constructor(private mixmatchService: MixMatchService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.getTask();
  }

  getTask(): void {
    const task_id = String(this.route.snapshot.paramMap.get('id'));
    this.mixmatchService.getTask(task_id).subscribe((task) => (this.task = task));
  }
}
