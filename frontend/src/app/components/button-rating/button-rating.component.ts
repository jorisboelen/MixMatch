import { Component, Input, Output, EventEmitter } from '@angular/core';
import { NgbRating } from '@ng-bootstrap/ng-bootstrap';
import { MusicItem } from '../../interfaces';

@Component({
  selector: 'app-button-rating',
  standalone: true,
  imports: [NgbRating],
  templateUrl: './button-rating.component.html',
  styleUrl: './button-rating.component.css'
})
export class ButtonRatingComponent {
  @Input() music_item!: MusicItem;
  @Output() updateMusicItemRatingEvent = new EventEmitter();

  updateRating(music_item: MusicItem) {
    this.updateMusicItemRatingEvent.emit(music_item);
  }
}
