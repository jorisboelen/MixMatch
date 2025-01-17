import { Component, Input, Output, EventEmitter } from '@angular/core';
import { DatePipe, DecimalPipe, NgIf, UpperCasePipe } from '@angular/common';
import { ButtonRatingComponent } from '../button-rating/button-rating.component';
import { Track } from '../../interfaces';

@Component({
  selector: 'app-track-table',
  standalone: true,
  imports: [ButtonRatingComponent, DatePipe, DecimalPipe, NgIf, UpperCasePipe],
  templateUrl: './track-table.component.html',
  styleUrl: './track-table.component.css'
})
export class TrackTableComponent {
  @Input() track!: Track;
  @Input() track_media!: string;
  @Output() updateTrackRatingEvent = new EventEmitter<Track>();

  updateTrackRating(track: Track) {
      this.updateTrackRatingEvent.emit(track);
  }
}
