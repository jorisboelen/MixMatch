import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { DatePipe, DecimalPipe, UpperCasePipe } from '@angular/common';
import { ButtonRatingComponent } from '../button-rating/button-rating.component';
import { Track } from '../../interfaces';

@Component({
    selector: 'app-track-table',
    imports: [ButtonRatingComponent, DatePipe, DecimalPipe, UpperCasePipe],
    templateUrl: './track-table.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
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
