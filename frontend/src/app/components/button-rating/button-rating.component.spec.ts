import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ButtonRatingComponent } from './button-rating.component';

describe('ButtonRatingComponent', () => {
  let component: ButtonRatingComponent;
  let fixture: ComponentFixture<ButtonRatingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ButtonRatingComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ButtonRatingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
