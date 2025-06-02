import { Component } from '@angular/core';
import { CommonModule, Location, NgIf } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { AudioPlayerComponent } from './components/audio-player/audio-player.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ToastNotificationComponent } from './components/toast-notification/toast-notification.component';

@Component({
    selector: 'app-root',
    imports: [AudioPlayerComponent, CommonModule, RouterOutlet, NavbarComponent, NgIf, ToastNotificationComponent],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(public location: Location) {}
}
