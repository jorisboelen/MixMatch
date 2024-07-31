import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MixMatchService } from '../../services/mixmatch.service';
import { MusicItem, Genre } from '../../interfaces';

@Component({
  selector: 'app-music-edit',
  standalone: true,
  imports: [FormsModule, NgFor, NgIf],
  templateUrl: './music-edit.component.html',
  styleUrl: './music-edit.component.css'
})
export class MusicEditComponent {
  music_item?: MusicItem;
  genre_list?: Genre[];
  key_list?: String[];
  music_item_cover?: string;
  music_item_media?: string;

  constructor(private mixmatchService: MixMatchService, private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.getMusicItem();
    this.getMusicItemCover();
    this.mixmatchService.getGenre().subscribe((genre_list) => (this.genre_list = genre_list));
    this.key_list = this.mixmatchService.getKey();
  }

  getMusicItem(){
    const music_item_id = Number(this.route.snapshot.paramMap.get('id'));
    this.music_item_media = this.mixmatchService.getMusicItemMedia(music_item_id);
    this.mixmatchService.getMusicItem(music_item_id).subscribe((music_item) => (this.music_item = music_item));
  }

  getMusicItemCover(){
    const music_item_id = Number(this.route.snapshot.paramMap.get('id'));
    this.music_item_cover = this.mixmatchService.getMusicItemCover(music_item_id);
  }

  updateMusicItem(music_item: MusicItem){
    let music_item_data = {artist: music_item.artist, title: music_item.title, album: music_item.album,
                           genre_id: music_item.genre.id, date: music_item.date, rating: music_item.rating}
    this.mixmatchService.patchMusicItem(music_item.id, music_item_data).subscribe((music_item) => this.router.navigateByUrl('/music/' + music_item.id));
  }

  updateMusicItemCover(music_item: MusicItem, event: any) {
    const file:File = event.target.files[0];
    this.mixmatchService.updateMusicItemCover(music_item.id, file).subscribe((music_item)=> this.getMusicItemCover());
  }
}
