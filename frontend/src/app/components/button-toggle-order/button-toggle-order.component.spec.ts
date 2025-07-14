import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ButtonToggleOrderComponent } from './button-toggle-order.component';

describe('ButtonToggleOrderComponent', () => {
  let component: ButtonToggleOrderComponent;
  let fixture: ComponentFixture<ButtonToggleOrderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ButtonToggleOrderComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ButtonToggleOrderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
