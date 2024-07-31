import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { PlaylistModel } from '../../models'

@Component({
  selector: 'app-modal-playlist-add',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './modal-playlist-add.component.html',
  styleUrl: './modal-playlist-add.component.css'
})
export class ModalPlaylistAddComponent {
  @Input() playlist!: PlaylistModel;

  constructor(public activeModal: NgbActiveModal) {}
}
