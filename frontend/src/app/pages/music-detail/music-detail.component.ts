import { Component } from '@angular/core';
import { LowerCasePipe, NgIf } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPlaylistItemAddComponent } from '../../components/modal-playlist-item-add/modal-playlist-item-add.component';
import { MusicItemTableComponent } from '../../components/music-item-table/music-item-table.component';
import { AudioService } from '../../services/audio.service';
import { MixMatchService } from '../../services/mixmatch.service';
import { MusicItem, PlaylistResponse } from '../../interfaces';
import { PlaylistItemModel } from '../../models';

@Component({
  selector: 'app-music-detail',
  standalone: true,
  imports: [LowerCasePipe, MusicItemTableComponent, NgIf, RouterLink],
  templateUrl: './music-detail.component.html',
  styleUrl: './music-detail.component.css'
})
export class MusicDetailComponent {
  music_item?: MusicItem;
  music_item_cover?: string;
  music_item_media?: string;
  playlist_list?: PlaylistResponse;

  constructor(private audioService: AudioService, private mixmatchService: MixMatchService, private route: ActivatedRoute, private router: Router, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.mixmatchService.getPlaylists({size: 100, page: 1}).subscribe((playlist_list) => (this.playlist_list = playlist_list));
    this.getMusicItem();
  }

  openMusicDeleteModal(music_item: MusicItem): void {
    const modal = this.modalService.open(ModalDeleteConfirmationComponent, {});
    modal.componentInstance.modal_title = music_item.artist + ' - ' + music_item.title;
    modal.componentInstance.modal_body = 'Are you sure you want to delete this item? This will also remove the file from disk.';
    modal.result.then(
      (result) => {this.deleteMusicItem(music_item)},
      (reason) => {},
    );
  }

  openPlaylistItemAddModal(music_item: MusicItem): void {
    const playlist_item = new PlaylistItemModel();
    const modal = this.modalService.open(ModalPlaylistItemAddComponent, {});
    modal.componentInstance.modal_title = music_item.artist + ' - ' + music_item.title;
    modal.componentInstance.playlist_list = this.playlist_list;
    modal.componentInstance.playlist_item = playlist_item;
    playlist_item.music_id = music_item.id;
    modal.result.then(
      (result) => {this.addPlaylistItem(playlist_item)},
      (reason) => {},
    );
  }

  getMusicItem(){
    const music_item_id = Number(this.route.snapshot.paramMap.get('id'));
    this.music_item_cover = this.mixmatchService.getMusicItemCover(music_item_id);
    this.music_item_media = this.mixmatchService.getMusicItemMedia(music_item_id);
    this.mixmatchService.getMusicItem(music_item_id).subscribe((music_item) => (this.music_item = music_item));
  }

  addPlaylistItem(playlist_item: PlaylistItemModel){
    this.mixmatchService.addPlaylistItem(playlist_item).subscribe()
  }

  deleteMusicItem(music_item: MusicItem){
    this.mixmatchService.deleteMusicItem(music_item.id).subscribe((music_item) => this.router.navigateByUrl('/music'));
  }

  updateMusicItemRating(music_item: MusicItem){
    this.mixmatchService.patchMusicItem(music_item.id, {rating: music_item.rating}).subscribe((music_item) => this.getMusicItem());
  }

  isAdminUser(): boolean {
    return this.mixmatchService.isAdminUser();
  }

  playStream(url: string): void {
    this.audioService.stop();
    this.audioService.playStream(url).subscribe(state => {});
  }
}
