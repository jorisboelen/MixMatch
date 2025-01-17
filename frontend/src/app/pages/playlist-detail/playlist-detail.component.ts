import { Component } from '@angular/core';
import { DatePipe, NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray } from '@angular/cdk/drag-drop';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { MixMatchService } from '../../services/mixmatch.service';
import { NotificationService } from '../../services/notification.service';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPlaylistEditComponent } from '../../components/modal-playlist-edit/modal-playlist-edit.component';
import { NotificationLevel, Playlist, PlaylistItem } from '../../interfaces';

@Component({
  selector: 'app-playlist-detail',
  standalone: true,
  imports: [CdkDrag, CdkDropList, DatePipe, NgFor, NgIf, RouterLink],
  templateUrl: './playlist-detail.component.html',
  styleUrl: './playlist-detail.component.css'
})
export class PlaylistDetailComponent {
  playlist?: Playlist;
  playlist_export?: string;

  constructor(private mixmatchService: MixMatchService, private notification: NotificationService, private route: ActivatedRoute, private router: Router, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.getPlaylist();
  }

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

  openPlaylistItemDeleteModal(playlist_item: PlaylistItem): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = playlist_item.track.artist + " - " + playlist_item.track.title;
    modal.result.then(
      (result) => {this.deletePlaylistItem(playlist_item)},
      (reason) => {},
    );
  }

  getPlaylist(){
    const playlist_id = Number(this.route.snapshot.paramMap.get('id'));
    this.mixmatchService.getPlaylist(playlist_id).subscribe((playlist) => (this.playlist = playlist));
    this.playlist_export = this.mixmatchService.getPlaylistExport(playlist_id);
  }

  deletePlaylist(playlist: Playlist){
    this.mixmatchService.deletePlaylist(playlist.id).subscribe((playlist) => this.router.navigateByUrl('/playlist'));
  }

  deletePlaylistItem(playlist_item: PlaylistItem) {
    this.mixmatchService.deletePlaylistItem(playlist_item.id).subscribe((playlist_item) => this.getPlaylist());
  }

  updatePlaylist(playlist: Playlist){
    this.mixmatchService.patchPlaylist(playlist.id, {name: playlist.name}).subscribe((playlist) => this.getPlaylist());
  }

  changeOrder(event: CdkDragDrop<string[]>) {
    if (this.playlist) {
      moveItemInArray(this.playlist.playlist_items, event.previousIndex, event.currentIndex);
    }
  }

  saveOrder(){
    if (this.playlist) {
      for (let i = 0; i < this.playlist.playlist_items.length; i++) {
        this.playlist.playlist_items[i].order = i + 1;
        this.mixmatchService.patchPlaylistItem(this.playlist.playlist_items[i].id, {order: i + 1}).subscribe();
      }
      this.notification.addNotification(NotificationLevel.INFO, 'Changes saved');
    }
  }
}
