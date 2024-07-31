import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { MixMatchService } from '../../services/mixmatch.service';
import { ModalPlaylistAddComponent } from '../../components/modal-playlist-add/modal-playlist-add.component';
import { PaginationComponent } from '../../components/pagination/pagination.component';
import { PlaylistMusicListComponent } from '../../components/playlist-music-list/playlist-music-list.component';
import { PlaylistResponse, Playlist, User } from '../../interfaces';
import { PlaylistModel } from '../../models';

@Component({
  selector: 'app-playlist',
  standalone: true,
  imports: [NgFor, NgIf, PaginationComponent, PlaylistMusicListComponent],
  templateUrl: './playlist.component.html',
  styleUrl: './playlist.component.css'
})
export class PlaylistComponent {
  playlist_list?: PlaylistResponse;
  current_page: number = 1;
  current_size: number = 9;

  constructor(private mixmatchService: MixMatchService, private modalService: NgbModal) {}

  ngOnInit(): void {
    this.getPlaylists();
  }

  openPlaylistAddModal(): void {
    const playlist = new PlaylistModel();
    const modal = this.modalService.open(ModalPlaylistAddComponent, {});
    modal.componentInstance.playlist = playlist;
    modal.result.then(
      (result) => {this.addPlaylist(playlist)},
      (reason) => {},
    );
  }

  changePage(page: number){
    this.current_page = page;
    this.getPlaylists();
  }

  addPlaylist(playlist: PlaylistModel){
    this.mixmatchService.addPlaylist(playlist).subscribe((playlist) => this.getPlaylists());
  }

  getPlaylists(){
    let params = {size: this.current_size, page: this.current_page}
    this.mixmatchService.searchPlaylists(params, {sort_by: 'modified', sort_order: 'desc'}).subscribe((playlist_list) => (this.playlist_list = playlist_list));
  }

  deletePlaylist(playlist: Playlist){
    this.mixmatchService.deletePlaylist(playlist.id).subscribe((playlist) => this.getPlaylists());
  }

  updatePlaylist(playlist: Playlist){
    this.mixmatchService.patchPlaylist(playlist.id, {name: playlist.name}).subscribe((playlist) => this.getPlaylists());
  }
}
