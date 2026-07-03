import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Playlist } from '../../interfaces';

@Component({
    selector: 'app-modal-playlist-edit',
    imports: [FormsModule],
    templateUrl: './modal-playlist-edit.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './modal-playlist-edit.component.css'
})
export class ModalPlaylistEditComponent {
  @Input() playlist!: Playlist;

  constructor(public activeModal: NgbActiveModal) {}
}
