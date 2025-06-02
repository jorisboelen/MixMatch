import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { UserModel } from '../../models';

@Component({
    selector: 'app-modal-user-reset',
    imports: [FormsModule],
    templateUrl: './modal-user-reset.component.html',
    styleUrl: './modal-user-reset.component.css'
})
export class ModalUserResetComponent {
  @Input() user!: UserModel;

  constructor(public activeModal: NgbActiveModal) {}
}
