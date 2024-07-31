import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaylistMusicListComponent } from './playlist-music-list.component';

describe('PlaylistMusicListComponent', () => {
  let component: PlaylistMusicListComponent;
  let fixture: ComponentFixture<PlaylistMusicListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaylistMusicListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PlaylistMusicListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
