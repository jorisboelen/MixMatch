import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { UserModel } from '../../models';

@Component({
    selector: 'app-modal-user-add',
    imports: [FormsModule],
    templateUrl: './modal-user-add.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './modal-user-add.component.css'
})
export class ModalUserAddComponent {
  @Input() user!: UserModel;

  constructor(public activeModal: NgbActiveModal) {}
}
