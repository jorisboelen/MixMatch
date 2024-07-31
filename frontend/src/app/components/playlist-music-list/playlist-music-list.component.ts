import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DatePipe, NgFor } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPlaylistEditComponent } from '../../components/modal-playlist-edit/modal-playlist-edit.component';
import { Playlist } from '../../interfaces';

@Component({
  selector: 'app-playlist-music-list',
  standalone: true,
  imports: [DatePipe, NgFor, RouterLink],
  templateUrl: './playlist-music-list.component.html',
  styleUrl: './playlist-music-list.component.css'
})
export class PlaylistMusicListComponent {
  @Input() playlist!: Playlist;
  @Output() deletePlaylistEvent = new EventEmitter<Playlist>();
  @Output() updatePlaylistEvent = new EventEmitter<Playlist>();

  constructor(private modalService: NgbModal) {}

  openPlaylistDeleteModal(playlist: Playlist): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = playlist.name;
    modal.result.then(
      (result) => {this.deletePlaylist(playlist)},
      (reason) => {},
    );
  }

  openPlaylistEditModal(playlist: Playlist): void {
    const modal = this.modalService.open(ModalPlaylistEditComponent, {});
    modal.componentInstance.playlist = playlist;
    modal.result.then(
      (result) => {this.updatePlaylist(playlist)},
      (reason) => {},
    );
  }

  deletePlaylist(playlist: Playlist) {
    this.deletePlaylistEvent.emit(playlist);
  }

  updatePlaylist(playlist: Playlist) {
    this.updatePlaylistEvent.emit(playlist);
  }
}
