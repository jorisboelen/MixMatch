import { Component } from '@angular/core';

import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MixMatchService } from '../../services/mixmatch.service';
import { Genre, Track } from '../../interfaces';

@Component({
    selector: 'app-track-edit',
    imports: [FormsModule],
    templateUrl: './track-edit.component.html',
    styleUrl: './track-edit.component.css'
})
export class TrackEditComponent {
  track?: Track;
  genre_list?: Genre[];
  key_list?: String[];
  track_cover?: string;
  track_media?: string;

  constructor(private mixmatchService: MixMatchService, private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.getTrack();
    this.getTrackCover();
    this.mixmatchService.getGenre().subscribe((genre_list) => (this.genre_list = genre_list));
    this.key_list = this.mixmatchService.getKey();
  }

  getTrack(){
    const track_id = Number(this.route.snapshot.paramMap.get('id'));
    this.track_media = this.mixmatchService.getTrackMedia(track_id);
    this.mixmatchService.getTrack(track_id).subscribe((track) => (this.track = track));
  }

  getTrackCover(){
    const track_id = Number(this.route.snapshot.paramMap.get('id'));
    this.track_cover = this.mixmatchService.getTrackCover(track_id);
  }

  updateTrack(track: Track){
    let track_data = {artist: track.artist, title: track.title, album: track.album,
                           genre_id: track.genre.id, date: track.date, rating: track.rating}
    this.mixmatchService.patchTrack(track.id, track_data).subscribe((track) => this.router.navigateByUrl('/track/' + track.id));
  }

  updateTrackCover(track: Track, event: any) {
    const file:File = event.target.files[0];
    this.mixmatchService.updateTrackCover(track.id, file).subscribe((track)=> this.getTrackCover());
  }
}
