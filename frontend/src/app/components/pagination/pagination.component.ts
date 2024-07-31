import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-pagination',
  standalone: true,
  imports: [NgbPaginationModule],
  templateUrl: './pagination.component.html',
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
