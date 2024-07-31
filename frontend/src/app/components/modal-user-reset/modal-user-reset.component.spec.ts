import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalUserResetComponent } from './modal-user-reset.component';

describe('ModalUserResetComponent', () => {
  let component: ModalUserResetComponent;
  let fixture: ComponentFixture<ModalUserResetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalUserResetComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModalUserResetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
