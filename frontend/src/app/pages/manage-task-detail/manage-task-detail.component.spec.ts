import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageTaskDetailComponent } from './manage-task-detail.component';

describe('ManageTaskDetailComponent', () => {
  let component: ManageTaskDetailComponent;
  let fixture: ComponentFixture<ManageTaskDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ManageTaskDetailComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ManageTaskDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
