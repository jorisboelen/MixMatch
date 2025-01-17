import { Routes } from '@angular/router';
import { MainComponent } from './pages/main/main.component';
import { LoginComponent } from './pages/login/login.component';
import { ManageComponent } from './pages/manage/manage.component';
import { ManageTaskDetailComponent } from './pages/manage-task-detail/manage-task-detail.component';
import { PlaylistComponent } from './pages/playlist/playlist.component';
import { PlaylistDetailComponent } from './pages/playlist-detail/playlist-detail.component';
import { TrackComponent } from './pages/track/track.component';
import { TrackDetailComponent } from './pages/track-detail/track-detail.component';
import { TrackEditComponent } from './pages/track-edit/track-edit.component';

export const routes: Routes = [
    { path: '', component: MainComponent },
    { path: 'login', component: LoginComponent },
    { path: 'manage', component: ManageComponent },
    { path: 'manage/task/:id/detail', component: ManageTaskDetailComponent },
    { path: 'playlist', component: PlaylistComponent },
    { path: 'playlist/:id', component: PlaylistDetailComponent },
    { path: 'track', component: TrackComponent },
    { path: 'track/:id', component: TrackDetailComponent },
    { path: 'track/:id/edit', component: TrackEditComponent },
];
