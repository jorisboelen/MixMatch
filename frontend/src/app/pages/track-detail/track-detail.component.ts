import { Component } from '@angular/core';
import { LowerCasePipe, NgIf } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPlaylistItemAddComponent } from '../../components/modal-playlist-item-add/modal-playlist-item-add.component';
import { TrackTableComponent } from '../../components/track-table/track-table.component';
import { AudioService } from '../../services/audio.service';
import { MixMatchService } from '../../services/mixmatch.service';
import { PlaylistResponse, Track } from '../../interfaces';
import { PlaylistItemModel } from '../../models';

@Component({
    selector: 'app-track-detail',
    imports: [LowerCasePipe, TrackTableComponent, NgIf, RouterLink],
    templateUrl: './track-detail.component.html',
    styleUrl: './track-detail.component.css'
})
export class TrackDetailComponent {
  track?: Track;
  track_cover?: string;
  track_media?: string;
  playlist_list?: PlaylistResponse;

  constructor(private audioService: AudioService, private mixmatchService: MixMatchService, private route: ActivatedRoute, private router: Router, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.mixmatchService.getPlaylists({size: 100, page: 1}).subscribe((playlist_list) => (this.playlist_list = playlist_list));
    this.getTrack();
  }

  openTrackDeleteModal(track: Track): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = track.artist + ' - ' + track.title;
    modal.componentInstance.modal_body = 'Are you sure you want to delete this item? This will also remove the file from disk.';
    modal.result.then(
      (result) => {this.deleteTrack(track)},
      (reason) => {},
    );
  }

  openPlaylistItemAddModal(track: Track): void {
    const playlist_item = new PlaylistItemModel();
    const modal = this.modalService.open(ModalPlaylistItemAddComponent, {});
    modal.componentInstance.modal_title = track.artist + ' - ' + track.title;
    modal.componentInstance.playlist_list = this.playlist_list;
    modal.componentInstance.playlist_item = playlist_item;
    playlist_item.track_id = track.id;
    modal.result.then(
      (result) => {this.addPlaylistItem(playlist_item)},
      (reason) => {},
    );
  }

  getTrack(){
    const track_id = Number(this.route.snapshot.paramMap.get('id'));
    this.track_cover = this.mixmatchService.getTrackCover(track_id);
    this.track_media = this.mixmatchService.getTrackMedia(track_id);
    this.mixmatchService.getTrack(track_id).subscribe((track) => (this.track = track));
  }

  addPlaylistItem(playlist_item: PlaylistItemModel){
    this.mixmatchService.addPlaylistItem(playlist_item).subscribe();
  }

  deleteTrack(track: Track){
    this.mixmatchService.deleteTrack(track.id).subscribe((track) => this.router.navigateByUrl('/track'));
  }

  updateTrackRating(track: Track){
    this.mixmatchService.patchTrack(track.id, {rating: track.rating}).subscribe((track) => this.getTrack());
  }

  isAdminUser(): boolean {
    return this.mixmatchService.isAdminUser();
  }

  playStream(url: string): void {
    this.audioService.stop();
    this.audioService.playStream(url).subscribe(state => {});
  }
}
