import { Component, Input } from '@angular/core';
import { NgIf, NgFor } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TrackResponse } from '../../interfaces';

@Component({
    selector: 'app-track-list',
    imports: [NgIf, NgFor, RouterLink],
    templateUrl: './track-list.component.html',
    styleUrl: './track-list.component.css'
})
export class TrackListComponent {
  @Input() label!: String;
  @Input() trackResponse!: TrackResponse;
}
