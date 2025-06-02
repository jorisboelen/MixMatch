import { Component } from '@angular/core';
import { NgIf } from '@angular/common';
import { MixMatchService } from '../../services/mixmatch.service';

@Component({
    selector: 'app-navbar-resources',
    imports: [NgIf],
    templateUrl: './navbar-resources.component.html',
    styleUrl: './navbar-resources.component.css'
})
export class NavbarResourcesComponent {
  docs_url?: string;
  
  constructor(private mixmatchService: MixMatchService) {}
  
  ngOnInit(): void {
    this.docs_url = this.mixmatchService.getDocs();
  }
}
