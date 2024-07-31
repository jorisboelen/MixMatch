import { Injectable } from '@angular/core';
import { NotificationLevel, NotificationMessage } from '../interfaces';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  notification_list: NotificationMessage[] = [];

  constructor() { }

  addNotification(level: NotificationLevel, message: string): void {
    let notification: NotificationMessage = {level: level, message: message, timestamp: new Date()};
    this.notification_list.push(notification)
  }

  getNotifications(): NotificationMessage[] {
    return this.notification_list;
  }

  removeNotification(notification: NotificationMessage): void {
    this.notification_list.splice(this.notification_list.indexOf(notification), 1);
  }
}
