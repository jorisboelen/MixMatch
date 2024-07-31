import { Routes } from '@angular/router';
import { MainComponent } from './pages/main/main.component';
import { LoginComponent } from './pages/login/login.component';
import { ManageComponent } from './pages/manage/manage.component';
import { ManageTaskDetailComponent } from './pages/manage-task-detail/manage-task-detail.component';
import { MusicComponent } from './pages/music/music.component';
import { MusicDetailComponent } from './pages/music-detail/music-detail.component';
import { MusicEditComponent } from './pages/music-edit/music-edit.component';
import { PlaylistComponent } from './pages/playlist/playlist.component';
import { PlaylistDetailComponent } from './pages/playlist-detail/playlist-detail.component';

export const routes: Routes = [
    { path: '', component: MainComponent },
    { path: 'login', component: LoginComponent },
    { path: 'manage', component: ManageComponent },
    { path: 'manage/task/:id/detail', component: ManageTaskDetailComponent },
    { path: 'music', component: MusicComponent },
    { path: 'music/:id', component: MusicDetailComponent },
    { path: 'music/:id/edit', component: MusicEditComponent },
    { path: 'playlist', component: PlaylistComponent },
    { path: 'playlist/:id', component: PlaylistDetailComponent },
];
