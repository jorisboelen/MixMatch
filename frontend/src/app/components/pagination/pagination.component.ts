import { Component, EventEmitter, Input, Output, ChangeDetectionStrategy } from '@angular/core';
import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
    selector: 'app-pagination',
    imports: [NgbPaginationModule],
    templateUrl: './pagination.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './pagination.component.css'
})
export class PaginationComponent {
  @Input() current_page: number = 0;
  @Input() items_count: number = 0;
  @Input() items_per_page: number = 0;
  @Output() changePageEvent = new EventEmitter();

  changePage(page: number){
    this.changePageEvent.emit(page);
  }
}
