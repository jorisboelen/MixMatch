import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { ButtonStatsComponent } from '../../components/button-stats/button-stats.component';
import { TrackListComponent } from '../../components/track-list/track-list.component';
import { MixMatchService } from '../../services/mixmatch.service';
import { PlaylistResponse, TrackResponse } from '../../interfaces';

@Component({
    selector: 'app-main',
    imports: [NgFor, NgIf, ButtonStatsComponent, TrackListComponent],
    templateUrl: './main.component.html',
    styleUrl: './main.component.css'
})
export class MainComponent {
  track_count?: TrackResponse;
  playlist_count?: PlaylistResponse;
  track_modified?: TrackResponse;
  track_new?: TrackResponse;
  track_rated?: TrackResponse;
  
  constructor(private mixmatchService: MixMatchService) {}
  
  ngOnInit(): void {
    this.mixmatchService.getTracks({size: 1, page: 1}).subscribe((track_count) => (this.track_count = track_count));
    this.mixmatchService.getPlaylists({size: 1, page: 1}).subscribe((playlist_count) => (this.playlist_count = playlist_count));
    this.mixmatchService.searchTracks({size: 10, page: 1}, {sort_by: 'mtime', sort_order: 'desc'}).subscribe((track_modified) => (this.track_modified = track_modified));
    this.mixmatchService.searchTracks({size: 10, page: 1}, {sort_by: 'date', sort_order: 'desc', random: true}).subscribe((track_new) => (this.track_new = track_new));
    this.mixmatchService.searchTracks({size: 10, page: 1}, {sort_by: 'rating', sort_order: 'desc', random: true}).subscribe((track_rated) => (this.track_rated = track_rated));
  }
}
