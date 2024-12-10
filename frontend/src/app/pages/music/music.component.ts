import { Component } from '@angular/core';
import { NgClass, NgFor, NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ButtonRatingComponent } from '../../components/button-rating/button-rating.component';
import { ButtonToggleOrderComponent } from '../../components/button-toggle-order/button-toggle-order.component';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalMusicFilterComponent } from '../../components/modal-music-filter/modal-music-filter.component';
import { ModalPlaylistItemAddComponent } from '../../components/modal-playlist-item-add/modal-playlist-item-add.component';
import { PaginationComponent } from '../../components/pagination/pagination.component';
import { MixMatchService } from '../../services/mixmatch.service';
import { Genre, MusicItem, MusicListResponse, PlaylistResponse } from '../../interfaces';
import { MusicSearchQueryModel, PlaylistItemModel } from '../../models';

@Component({
  selector: 'app-music',
  standalone: true,
  imports: [ButtonRatingComponent, ButtonToggleOrderComponent, NgClass, NgFor, NgIf, PaginationComponent, RouterLink],
  templateUrl: './music.component.html',
  styleUrl: './music.component.css'
})
export class MusicComponent {
  genre_list?: Genre[];
  key_list?: String[];
  music_list?: MusicListResponse;
  playlist_list?: PlaylistResponse;
  search_query: MusicSearchQueryModel = new MusicSearchQueryModel();
  filter_enabled: boolean = false;
  current_page: number = 1;
  current_size: number = 25;

  constructor(private mixmatchService: MixMatchService, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.mixmatchService.getGenre().subscribe((genre_list) => (this.genre_list = genre_list));
    this.mixmatchService.getPlaylists({size: 100, page: 1}).subscribe((playlist_list) => (this.playlist_list = playlist_list));
    this.key_list = this.mixmatchService.getKey();
    this.initMusicSearchQuery();
    this.getMusic();
  }

  initMusicSearchQuery(){
    let local_current_page = localStorage.getItem('music_current_page');
    let local_search_query = localStorage.getItem('music_search_query');
    if (local_current_page){this.current_page = JSON.parse(local_current_page);}
    if (local_search_query){this.search_query = JSON.parse(local_search_query); this.filter_enabled = true;}
  }

  openFilterModal(): void {
    const modal = this.modalService.open(ModalMusicFilterComponent, {scrollable: true});
    modal.componentInstance.genre_list = this.genre_list;
    modal.componentInstance.key_list = this.key_list;
    modal.componentInstance.search_query = this.search_query;
    modal.result.then(
      (result) => {this.search()},
      (reason) => {},
    );
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

  reset(){
    this.filter_enabled = false;
    localStorage.removeItem('music_search_query');
    this.search_query = new MusicSearchQueryModel();
    this.resetCurrentPage();
    this.getMusic();
  }

  resetCurrentPage(){
    this.current_page = 1;
    localStorage.removeItem('music_current_page');
  }

  search(){
    this.filter_enabled = true;
    localStorage.setItem('music_search_query', JSON.stringify(this.search_query));
    this.resetCurrentPage();
    this.getMusic();
  }

  changePage(page: number){
    this.current_page = page;
    localStorage.setItem('music_current_page', JSON.stringify(this.current_page));
    this.getMusic();
  }

  toggleOrdering(ordering: string){
    if (this.search_query.sort_by == ordering){this.search_query.sort_order = this.search_query.sort_order == 'asc' ? 'desc' : 'asc';}
    else {this.search_query.sort_by = ordering; this.search_query.sort_order = 'asc';}
    localStorage.setItem('music_search_query', JSON.stringify(this.search_query));
    this.getMusic();
  }

  addPlaylistItem(playlist_item: PlaylistItemModel){
    this.mixmatchService.addPlaylistItem(playlist_item).subscribe();
  }

  deleteMusicItem(music_item: MusicItem){
    this.mixmatchService.deleteMusicItem(music_item.id).subscribe((music_item) => this.getMusic());
  }

  getMusic(){
    let params = {size: this.current_size, page: this.current_page};
    let music_search_query = JSON.parse(JSON.stringify(this.search_query));
    this.mixmatchService.searchMusic(params, music_search_query).subscribe((music_list) => (this.music_list = music_list));
  }

  updateMusicItemRating(music_item: MusicItem){
    this.mixmatchService.patchMusicItem(music_item.id, {rating: music_item.rating}).subscribe((music_item) => this.getMusic());
  }

  isAdminUser(): boolean {
    return this.mixmatchService.isAdminUser();
  }
}
