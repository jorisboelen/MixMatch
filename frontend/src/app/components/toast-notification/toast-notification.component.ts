import { Component, ChangeDetectionStrategy } from '@angular/core';

import { NgbToast } from '@ng-bootstrap/ng-bootstrap';
import { NotificationService } from '../../services/notification.service';

@Component({
    selector: 'app-toast-notification',
    imports: [NgbToast],
    templateUrl: './toast-notification.component.html',
    changeDetection: ChangeDetectionStrategy.Eager,
    styleUrl: './toast-notification.component.css'
})
export class ToastNotificationComponent {
  constructor(public notificationService: NotificationService) {}
}
