import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-button-stats',
    imports: [RouterLink],
    templateUrl: './button-stats.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './button-stats.component.css'
})
export class ButtonStatsComponent {
  @Input() label!: String;
  @Input() count!: Number;
  @Input() routerLinkText!: string;
}
