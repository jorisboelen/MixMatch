import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { NgbRating } from '@ng-bootstrap/ng-bootstrap';
import { Track } from '../../interfaces';

@Component({
    selector: 'app-button-rating',
    imports: [NgbRating],
    templateUrl: './button-rating.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './button-rating.component.css'
})
export class ButtonRatingComponent {
  @Input() track!: Track;
  @Output() updateTrackRatingEvent = new EventEmitter();

  updateRating(track: Track) {
    this.updateTrackRatingEvent.emit(track);
  }
}
