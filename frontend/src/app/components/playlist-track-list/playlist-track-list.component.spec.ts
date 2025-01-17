import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaylistTrackListComponent } from './playlist-track-list.component';

describe('PlaylistTrackListComponent', () => {
  let component: PlaylistTrackListComponent;
  let fixture: ComponentFixture<PlaylistTrackListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaylistTrackListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PlaylistTrackListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
