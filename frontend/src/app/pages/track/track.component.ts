import { Component } from '@angular/core';
import { DatePipe, NgClass, NgFor, NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ButtonRatingComponent } from '../../components/button-rating/button-rating.component';
import { ButtonToggleOrderComponent } from '../../components/button-toggle-order/button-toggle-order.component';
import { ModalDeleteConfirmationComponent } from '../../components/modal-delete-confirmation/modal-delete-confirmation.component';
import { ModalPlaylistItemAddComponent } from '../../components/modal-playlist-item-add/modal-playlist-item-add.component';
import { ModalTrackFilterComponent } from '../../components/modal-track-filter/modal-track-filter.component';
import { PaginationComponent } from '../../components/pagination/pagination.component';
import { MixMatchService } from '../../services/mixmatch.service';
import { Genre, PlaylistResponse, Track, TrackResponse } from '../../interfaces';
import { TrackSearchQueryModel, PlaylistItemModel } from '../../models';

@Component({
    selector: 'app-track',
    imports: [ButtonRatingComponent, ButtonToggleOrderComponent, DatePipe, NgClass, NgFor, NgIf, PaginationComponent, RouterLink],
    templateUrl: './track.component.html',
    styleUrl: './track.component.css'
})
export class TrackComponent {
  genre_list?: Genre[];
  key_list?: String[];
  track_list?: TrackResponse;
  playlist_list?: PlaylistResponse;
  search_query: TrackSearchQueryModel = new TrackSearchQueryModel();
  filter_enabled: boolean = false;
  current_page: number = 1;
  current_size: number = 25;

  constructor(private mixmatchService: MixMatchService, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.mixmatchService.getGenre().subscribe((genre_list) => (this.genre_list = genre_list));
    this.mixmatchService.getPlaylists({size: 100, page: 1}).subscribe((playlist_list) => (this.playlist_list = playlist_list));
    this.key_list = this.mixmatchService.getKey();
    this.initTrackSearchQuery();
    this.getTracks();
  }

  initTrackSearchQuery(){
    let local_current_page = localStorage.getItem('track_current_page');
    let local_search_query = localStorage.getItem('track_search_query');
    if (local_current_page){this.current_page = JSON.parse(local_current_page);}
    if (local_search_query){this.search_query = JSON.parse(local_search_query); this.filter_enabled = true;}
  }

  openFilterModal(): void {
    const modal = this.modalService.open(ModalTrackFilterComponent, {scrollable: true});
    modal.componentInstance.genre_list = this.genre_list;
    modal.componentInstance.key_list = this.key_list;
    modal.componentInstance.search_query = this.search_query;
    modal.result.then(
      (result) => {this.search()},
      (reason) => {},
    );
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

  reset(){
    this.filter_enabled = false;
    localStorage.removeItem('track_search_query');
    this.search_query = new TrackSearchQueryModel();
    this.resetCurrentPage();
    this.getTracks();
  }

  resetCurrentPage(){
    this.current_page = 1;
    localStorage.removeItem('track_current_page');
  }

  search(){
    this.filter_enabled = true;
    localStorage.setItem('track_search_query', JSON.stringify(this.search_query));
    this.resetCurrentPage();
    this.getTracks();
  }

  changePage(page: number){
    this.current_page = page;
    localStorage.setItem('track_current_page', JSON.stringify(this.current_page));
    this.getTracks();
  }

  toggleOrdering(ordering: string){
    if (this.search_query.sort_by == ordering){this.search_query.sort_order = this.search_query.sort_order == 'asc' ? 'desc' : 'asc';}
    else {this.search_query.sort_by = ordering; this.search_query.sort_order = 'asc';}
    localStorage.setItem('track_search_query', JSON.stringify(this.search_query));
    this.getTracks();
  }

  addPlaylistItem(playlist_item: PlaylistItemModel){
    this.mixmatchService.addPlaylistItem(playlist_item).subscribe();
  }

  deleteTrack(track: Track){
    this.mixmatchService.deleteTrack(track.id).subscribe((track) => this.getTracks());
  }

  getTracks(){
    let params = {size: this.current_size, page: this.current_page};
    let track_search_query = JSON.parse(JSON.stringify(this.search_query));
    this.mixmatchService.searchTracks(params, track_search_query).subscribe((track_list) => (this.track_list = track_list));
  }

  updateTrackRating(track: Track){
    this.mixmatchService.patchTrack(track.id, {rating: track.rating}).subscribe((track) => this.getTracks());
  }

  isAdminUser(): boolean {
    return this.mixmatchService.isAdminUser();
  }
}
