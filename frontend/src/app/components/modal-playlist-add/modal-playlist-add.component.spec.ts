import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalPlaylistAddComponent } from './modal-playlist-add.component';

describe('ModalPlaylistAddComponent', () => {
  let component: ModalPlaylistAddComponent;
  let fixture: ComponentFixture<ModalPlaylistAddComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalPlaylistAddComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalPlaylistAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
