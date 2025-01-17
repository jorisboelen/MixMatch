import { Component, Input, Output, EventEmitter } from '@angular/core';
import { NgbRating } from '@ng-bootstrap/ng-bootstrap';
import { Track } from '../../interfaces';

@Component({
  selector: 'app-button-rating',
  standalone: true,
  imports: [NgbRating],
  templateUrl: './button-rating.component.html',
  styleUrl: './button-rating.component.css'
})
export class ButtonRatingComponent {
  @Input() track!: Track;
  @Output() updateTrackRatingEvent = new EventEmitter();

  updateRating(track: Track) {
    this.updateTrackRatingEvent.emit(track);
  }
}
