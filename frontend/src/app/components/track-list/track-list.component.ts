import { Component, Input, ChangeDetectionStrategy } from '@angular/core';

import { RouterLink } from '@angular/router';
import { TrackResponse } from '../../interfaces';

@Component({
    selector: 'app-track-list',
    imports: [RouterLink],
    templateUrl: './track-list.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './track-list.component.css'
})
export class TrackListComponent {
  @Input() label!: String;
  @Input() trackResponse!: TrackResponse;
}
