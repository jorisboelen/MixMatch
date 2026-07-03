import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { NgClass } from '@angular/common';

@Component({
    selector: 'app-button-toggle-order',
    imports: [NgClass],
    templateUrl: './button-toggle-order.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './button-toggle-order.component.css'
})
export class ButtonToggleOrderComponent {
  @Input() label!: string;
  @Input() field!: string;
  @Input() current_sort_by!: string;
  @Output() toggleOrderingEvent = new EventEmitter();

  toggleOrdering(ordering: string) {
    this.toggleOrderingEvent.emit(ordering);
  }

}
