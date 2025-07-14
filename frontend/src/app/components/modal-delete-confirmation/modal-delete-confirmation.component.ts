import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-modal-delete-confirmation',
    imports: [],
    templateUrl: './modal-delete-confirmation.component.html',
    styleUrl: './modal-delete-confirmation.component.css'
})
export class ModalDeleteConfirmationComponent {
  @Input() modal_title: string = '';
  @Input() modal_body: string = 'Are you sure you want to delete this item?';

  constructor(public activeModal: NgbActiveModal) {}
}
