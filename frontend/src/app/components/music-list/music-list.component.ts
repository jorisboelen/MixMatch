import { Component, Input } from '@angular/core';
import { NgIf, NgFor } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MusicListResponse } from '../../interfaces';

@Component({
  selector: 'app-music-list',
  standalone: true,
  imports: [NgIf, NgFor, RouterLink],
  templateUrl: './music-list.component.html',
  styleUrl: './music-list.component.css'
})
export class MusicListComponent {
  @Input() label!: String;
  @Input() musicListResponse!: MusicListResponse;
}
