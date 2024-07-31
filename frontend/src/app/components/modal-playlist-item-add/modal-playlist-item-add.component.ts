import { Component, Input } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { PlaylistItemModel } from '../../models';
import { PlaylistResponse } from '../../interfaces';

@Component({
  selector: 'app-modal-playlist-item-add',
  standalone: true,
  imports: [FormsModule, NgFor, NgIf],
  templateUrl: './modal-playlist-item-add.component.html',
  styleUrl: './modal-playlist-item-add.component.css'
})
export class ModalPlaylistItemAddComponent {
  @Input() modal_title: string = '';
  @Input() playlist_list!: PlaylistResponse;
  @Input() playlist_item!: PlaylistItemModel;

  constructor(public activeModal: NgbActiveModal) {}
}
