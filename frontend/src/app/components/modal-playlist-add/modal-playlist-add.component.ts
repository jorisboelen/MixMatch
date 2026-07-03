import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { PlaylistModel } from '../../models';

@Component({
    selector: 'app-modal-playlist-add',
    imports: [FormsModule],
    templateUrl: './modal-playlist-add.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './modal-playlist-add.component.css'
})
export class ModalPlaylistAddComponent {
  @Input() playlist!: PlaylistModel;

  constructor(public activeModal: NgbActiveModal) {}
}
