import { Component, Input } from '@angular/core';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Genre } from '../../interfaces';
import { MusicSearchQueryModel } from '../../models';

@Component({
  selector: 'app-modal-music-filter',
  standalone: true,
  imports: [FormsModule, NgFor],
  templateUrl: './modal-music-filter.component.html',
  styleUrl: './modal-music-filter.component.css'
})
export class ModalMusicFilterComponent {
  @Input() genre_list!: Genre[];
  @Input() key_list!: String[];
  @Input() search_query!: MusicSearchQueryModel;

  constructor(public activeModal: NgbActiveModal) {}
}
