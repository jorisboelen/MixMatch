import { Component, Input } from '@angular/core';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Genre } from '../../interfaces';
import { TrackSearchQueryModel } from '../../models';

@Component({
    selector: 'app-modal-track-filter',
    imports: [FormsModule, NgFor],
    templateUrl: './modal-track-filter.component.html',
    styleUrl: './modal-track-filter.component.css'
})
export class ModalTrackFilterComponent {
  @Input() genre_list!: Genre[];
  @Input() key_list!: String[];
  @Input() search_query!: TrackSearchQueryModel;

  constructor(public activeModal: NgbActiveModal) {}
}
