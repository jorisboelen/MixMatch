import { Component } from '@angular/core';
import { DatePipe, NgClass, NgFor, NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalUserAddComponent } from '../../components/modal-user-add/modal-user-add.component';
import { ModalUserResetComponent } from '../../components/modal-user-reset/modal-user-reset.component';
import { NavbarResourcesComponent } from '../../components/navbar-resources/navbar-resources.component';
import { MixMatchService } from '../../services/mixmatch.service';
import { Task, TaskRunning, User } from '../../interfaces';
import { UserModel } from '../../models';

@Component({
    selector: 'app-manage',
    imports: [DatePipe, NavbarResourcesComponent, NgClass, NgFor, NgIf, RouterLink],
    templateUrl: './manage.component.html',
    styleUrl: './manage.component.css'
})
export class ManageComponent {
  current_user?: User;
  task_list?: Task[];
  task_running_list?: TaskRunning[];
  user_list?: User[];
  
  constructor(private mixmatchService: MixMatchService, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.mixmatchService.getUserCurrent().subscribe((current_user) => (this.current_user = current_user));
    this.getTasks();
    this.getUsers();
  }

  openUserAddModal(): void {
    const user = new UserModel();
    const modal = this.modalService.open(ModalUserAddComponent, {});
    modal.componentInstance.user = user;
    modal.result.then(
      (result) => {this.addUser(user)},
      (reason) => {},
    );
  }

  openUserDeleteModal(user: User): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = user.username;
    modal.result.then(
      (result) => {this.deleteUser(user)},
      (reason) => {},
    );
  }

  openUserResetModal(username: string): void {
    const user = new UserModel();
    user.username = username;
    const modal = this.modalService.open(ModalUserResetComponent, {});
    modal.componentInstance.user = user;
    modal.result.then(
      (result) => {this.updateUserPassword(user)},
      (reason) => {},
    );
  }

  addUser(user: UserModel){
    this.mixmatchService.addUser(user).subscribe((user) => this.getUsers());
  }

  deleteUser(user: User): void {
    this.mixmatchService.deleteUser(user.username).subscribe((user) => this.getUsers());
  }

  getUsers(): void {
    this.mixmatchService.getUsers().subscribe((user_list) => (this.user_list = user_list));
  }

  updateUserType(user: User): void {
    user.is_admin = !user.is_admin;
    this.mixmatchService.patchUser(user.username, {is_admin: user.is_admin}).subscribe((user) => this.getUsers());
  }

  updateUserPassword(user: UserModel): void {
    if (user.username && user.password) {
      this.mixmatchService.patchUser(user.username, {password: user.password}).subscribe((user) => this.getUsers());
    };
  }

  getTasks(): void {
    this.mixmatchService.getTasks().subscribe((task_list) => (this.task_list = task_list));
    this.mixmatchService.getTasksRunning().subscribe((task_running_list) => (this.task_running_list = task_running_list));
  }

  runTask(task: Task): void {
    this.mixmatchService.runTask(task.id).subscribe((task) => this.getTasks());
  }
}
