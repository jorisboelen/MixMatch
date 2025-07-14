import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalTrackFilterComponent } from './modal-track-filter.component';

describe('ModalTrackFilterComponent', () => {
  let component: ModalTrackFilterComponent;
  let fixture: ComponentFixture<ModalTrackFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalTrackFilterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalTrackFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
