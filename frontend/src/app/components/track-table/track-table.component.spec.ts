import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrackTableComponent } from './track-table.component';

describe('TrackTableComponent', () => {
  let component: TrackTableComponent;
  let fixture: ComponentFixture<TrackTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrackTableComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TrackTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
