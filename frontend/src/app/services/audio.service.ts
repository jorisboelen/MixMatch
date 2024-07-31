import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { NotificationService } from './notification.service';
import { NotificationLevel, StreamState } from '../interfaces';

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private stop$ = new Subject();
  private audioObj = new Audio();
  audioEvents = [
    'ended', 'error', 'play', 'playing', 'pause', 'timeupdate', 'canplay', 'loadedmetadata', 'loadstart'
  ];
  private state: StreamState = {
    playing: false,
    duration: undefined,
    currentTime: undefined,
    canplay: false,
    volume: 1,
    muted: false,
    error: false,
  };

  constructor(private notification: NotificationService) { }

  private streamObservable(url: string): Observable<any> {
    return new Observable(observer => {
      // Play audio
      this.audioObj.src = url;
      this.audioObj.load();
      this.audioObj.play();

      // Set volume & muted state
      this.state.volume = this.audioObj.volume;
      this.state.muted = this.audioObj.muted;

      const handler = (event: Event) => {
        this.updateStateEvents(event);
        observer.next(event);
      };

      this.addEvents(this.audioObj, this.audioEvents, handler);
      return () => {
        // Stop Playing
        this.audioObj.pause();
        this.audioObj.currentTime = 0;
        // remove event listeners
        this.removeEvents(this.audioObj, this.audioEvents, handler);
        // reset state
        this.resetState();
      };
    });
  }

  private addEvents(obj: any, events: string[], handler: any) {
    events.forEach(event => {
      obj.addEventListener(event, handler);
    });
  }

  private removeEvents(obj: any, events: string[], handler: any) {
    events.forEach(event => {
      obj.removeEventListener(event, handler);
    });
  }

  playStream(url: string) {
    return this.streamObservable(url).pipe(takeUntil(this.stop$));
  }

  play() {
    this.audioObj.play();
  }

  pause() {
    this.audioObj.pause();
  }

  stop() {
    this.stop$.next('ended');
  }

  seekTo(seconds: number) {
    this.audioObj.currentTime = seconds;
  }

  changeVolume(volume: number) {
    if (volume >= 0 && volume <= 1){
      this.audioObj.volume = volume;
      this.state.volume = volume;
    }
  }

  mute(muted: boolean){
    this.audioObj.muted = muted;
    this.state.muted = muted;
  }

  private stateChange: BehaviorSubject<StreamState> = new BehaviorSubject(this.state);

  private updateStateEvents(event: Event): void {
    switch (event.type) {
      case 'canplay':
        this.state.duration = this.audioObj.duration;
        this.state.canplay = true;
        break;
      case 'playing':
        this.state.playing = true;
        break;
      case 'pause':
        this.state.playing = false;
        break;
      case 'timeupdate':
        this.state.currentTime = this.audioObj.currentTime;
        break;
      case 'error':
        this.handleError();
        break;
      case 'ended':
        this.stop();
        break;
    }
    this.stateChange.next(this.state);
  }

  private handleError() {
    if (this.audioObj && this.audioObj.error && this.audioObj.error.code == 4){
      this.notification.addNotification(NotificationLevel.ERROR, 'Playback failed, unsupported format');
    } else {
      this.notification.addNotification(NotificationLevel.ERROR, 'Playback failed');
    }
    this.resetState();
    this.state.error = true;
  }

  private resetState() {
    this.state.playing = false;
    this.state.canplay = false;
    this.state.duration = undefined;
    this.state.currentTime = undefined;
    this.state.error = false;
  }

  getState(): Observable<StreamState> {
    return this.stateChange.asObservable();
  }
}
