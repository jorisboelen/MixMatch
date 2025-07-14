import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalPlaylistItemAddComponent } from './modal-playlist-item-add.component';

describe('ModalPlaylistItemAddComponent', () => {
  let component: ModalPlaylistItemAddComponent;
  let fixture: ComponentFixture<ModalPlaylistItemAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalPlaylistItemAddComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalPlaylistItemAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
