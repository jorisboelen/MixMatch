import { Component, Input } from '@angular/core';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { UserModel } from '../../models';

@Component({
    selector: 'app-modal-user-add',
    imports: [FormsModule, NgFor],
    templateUrl: './modal-user-add.component.html',
    styleUrl: './modal-user-add.component.css'
})
export class ModalUserAddComponent {
  @Input() user!: UserModel;

  constructor(public activeModal: NgbActiveModal) {}
}
