import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalMusicFilterComponent } from './modal-music-filter.component';

describe('ModalMusicFilterComponent', () => {
  let component: ModalMusicFilterComponent;
  let fixture: ComponentFixture<ModalMusicFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalMusicFilterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalMusicFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
