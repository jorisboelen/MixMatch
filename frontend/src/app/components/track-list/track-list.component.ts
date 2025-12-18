import { Component, Input } from '@angular/core';

import { RouterLink } from '@angular/router';
import { TrackResponse } from '../../interfaces';

@Component({
    selector: 'app-track-list',
    imports: [RouterLink],
    templateUrl: './track-list.component.html',
    styleUrl: './track-list.component.css'
})
export class TrackListComponent {
  @Input() label!: String;
  @Input() trackResponse!: TrackResponse;
}
