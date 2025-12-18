import { Component } from '@angular/core';

import { AudioService } from '../../services/audio.service';
import { StreamState } from '../../interfaces';

@Component({
    selector: 'app-audio-player',
    imports: [],
    templateUrl: './audio-player.component.html',
    styleUrl: './audio-player.component.css'
})
export class AudioPlayerComponent {
  stream_state?: StreamState;

  constructor(public audioService: AudioService) {}

  ngOnInit(): void {
    this.audioService.getState().subscribe((state) => (this.stream_state = state));
  }

  changeVolume(e: any): void{
    if(e.target && e.target.value){this.audioService.changeVolume(e.target.value);}
  }

  seekTo(e: any): void{
    if(e.target && e.target.value){this.audioService.seekTo(e.target.value);}
  }
}
