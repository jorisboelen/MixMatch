import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-button-stats',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './button-stats.component.html',
  styleUrl: './button-stats.component.css'
})
export class ButtonStatsComponent {
  @Input() label!: String;
  @Input() count!: Number;
  @Input() routerLinkText!: string;
}
