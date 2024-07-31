import { Component, Input, Output, EventEmitter } from '@angular/core';
import { DatePipe, DecimalPipe, NgIf, UpperCasePipe } from '@angular/common';
import { ButtonRatingComponent } from '../button-rating/button-rating.component';
import { MusicItem } from '../../interfaces';

@Component({
  selector: 'app-music-item-table',
  standalone: true,
  imports: [ButtonRatingComponent, DatePipe, DecimalPipe, NgIf, UpperCasePipe],
  templateUrl: './music-item-table.component.html',
  styleUrl: './music-item-table.component.css'
})
export class MusicItemTableComponent {
  @Input() music_item!: MusicItem;
  @Input() music_item_media!: string;
  @Output() updateMusicItemRatingEvent = new EventEmitter<MusicItem>();

  updateMusicItemRating(music_item: MusicItem) {
      this.updateMusicItemRatingEvent.emit(music_item);
  }
}
