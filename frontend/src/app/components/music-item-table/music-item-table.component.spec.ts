import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MusicItemTableComponent } from './music-item-table.component';

describe('MusicItemTableComponent', () => {
  let component: MusicItemTableComponent;
  let fixture: ComponentFixture<MusicItemTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MusicItemTableComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MusicItemTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
