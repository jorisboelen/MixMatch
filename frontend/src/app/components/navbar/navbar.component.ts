import { Component } from '@angular/core';

import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { MixMatchService } from '../../services/mixmatch.service';
import { ModalUserResetComponent } from '../../components/modal-user-reset/modal-user-reset.component';
import { User } from '../../interfaces';
import { UserModel } from '../../models';

@Component({
    selector: 'app-navbar',
    imports: [RouterLink],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  current_user?: User;
  
  constructor(private mixmatchService: MixMatchService, private modalService: NgbModal) {}
  
  ngOnInit(): void {
    this.mixmatchService.getUserCurrent().subscribe((current_user) => (this.current_user = current_user));
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

  updateUserPassword(user: UserModel): void {
    if (user.username && user.password) {
      this.mixmatchService.patchUserCurrent({password: user.password}).subscribe();
    };
  }

  isAdminUser(): boolean {
    return this.mixmatchService.isAdminUser();
  }

  logout(): void {
    this.mixmatchService.logout().subscribe();
  }
}
