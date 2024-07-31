import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { ButtonStatsComponent } from '../../components/button-stats/button-stats.component';
import { MusicListComponent } from '../../components/music-list/music-list.component';
import { MixMatchService } from '../../services/mixmatch.service';
import { MusicListResponse, PlaylistResponse } from '../../interfaces';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [NgFor, NgIf, ButtonStatsComponent, MusicListComponent],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})
export class MainComponent {
  music_count?: MusicListResponse;
  playlist_count?: PlaylistResponse;
  music_modified?: MusicListResponse;
  music_new?: MusicListResponse;
  music_rated?: MusicListResponse;
  
  constructor(private mixmatchService: MixMatchService) {}
  
  ngOnInit(): void {
    this.mixmatchService.getMusic({size: 1, page: 1}).subscribe((music_count) => (this.music_count = music_count));
    this.mixmatchService.getPlaylists({size: 1, page: 1}).subscribe((playlist_count) => (this.playlist_count = playlist_count));
    this.mixmatchService.searchMusic({size: 10, page: 1}, {sort_by: 'mtime', sort_order: 'desc'}).subscribe((music_modified) => (this.music_modified = music_modified));
    this.mixmatchService.searchMusic({size: 10, page: 1}, {sort_by: 'date', sort_order: 'desc', random: true}).subscribe((music_new) => (this.music_new = music_new));
    this.mixmatchService.searchMusic({size: 10, page: 1}, {sort_by: 'rating', sort_order: 'desc', random: true}).subscribe((music_rated) => (this.music_rated = music_rated));
  }
}
