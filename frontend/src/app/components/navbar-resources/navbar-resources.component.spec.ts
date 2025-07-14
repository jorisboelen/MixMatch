import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NavbarResourcesComponent } from './navbar-resources.component';

describe('NavbarResourcesComponent', () => {
  let component: NavbarResourcesComponent;
  let fixture: ComponentFixture<NavbarResourcesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavbarResourcesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NavbarResourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
