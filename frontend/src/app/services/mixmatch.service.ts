import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, repeat, of, tap, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { NotificationService } from './notification.service';
import { Genre, MusicItem, MusicListResponse, Playlist, PlaylistResponse, PlaylistItem, NotificationLevel, Task, TaskRunning, User } from '../interfaces';
import { PlaylistModel, PlaylistItemModel, UserModel, UserLoginModel } from '../models';

@Injectable({
  providedIn: 'root'
})
export class MixMatchService {
  private apiBaseUrl = environment.mixmatchApiBaseUrl;
  private key_list = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B',
                      '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B', '12A', '12B'];
  private current_user?: User;

  constructor(private http: HttpClient, private notification: NotificationService, private router: Router) { }
  
  getDocs(): string {
    return this.apiBaseUrl + '/docs';
  }
  
  getKey(): String[] {
    return this.key_list;
  }

  getGenre(): Observable<Genre[]> {
    let apiUrl = this.apiBaseUrl + '/genre/';
    return this.http.get<Genre[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getMusic(params = {}): Observable<MusicListResponse> {
    let apiUrl = this.apiBaseUrl + '/music/';
    return this.http.get<MusicListResponse>(apiUrl, {withCredentials: true, params: new HttpParams({fromObject: params})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getMusicItem(music_item_id: number): Observable<MusicItem> {
    let apiUrl = this.apiBaseUrl + '/music/' + music_item_id;
    return this.http.get<MusicItem>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getMusicItemCover(music_item_id: number): string {
    return this.apiBaseUrl + '/music/' + music_item_id + '/cover?' + Date.now();
  }

  getMusicItemMedia(music_item_id: number): string {
    return this.apiBaseUrl + '/music/' + music_item_id + '/media';
  }

  searchMusic(params = {}, music_search_query = {}): Observable<MusicListResponse> {
    let apiUrl = this.apiBaseUrl + '/music/search';
    return this.http.post<MusicListResponse>(apiUrl, music_search_query, {withCredentials: true, params: new HttpParams({fromObject: params})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  deleteMusicItem(music_item_id: number): Observable<MusicItem> {
    let apiUrl = this.apiBaseUrl + '/music/' + music_item_id;
    return this.http.delete<MusicItem>(apiUrl, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Item removed')),
      catchError(this.handleError.bind(this))
    );
  }

  patchMusicItem(music_item_id: number, music_item_data: Object): Observable<MusicItem> {
    let apiUrl = this.apiBaseUrl + '/music/' + music_item_id;
    return this.http.patch<MusicItem>(apiUrl, music_item_data, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Changes saved')),
      catchError(this.handleError.bind(this))
    );
  }

  updateMusicItemCover(music_item_id: number, file: File): Observable<any> {
    let apiUrl = this.apiBaseUrl + '/music/' + music_item_id + '/cover';
    let formData = new FormData();
    formData.append("music_cover", file, file.name);
    return this.http.put(apiUrl, formData, {withCredentials: true}).pipe(
      tap(_ => this.handleEvent('Cover updated')),
      catchError(this.handleError.bind(this))
    );
  }

  getPlaylist(playlist_id: number): Observable<Playlist> {
    let apiUrl = this.apiBaseUrl + '/playlist/' + playlist_id ;
    return this.http.get<Playlist>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getPlaylists(params = {}): Observable<PlaylistResponse> {
    let apiUrl = this.apiBaseUrl + '/playlist/';
    return this.http.get<PlaylistResponse>(apiUrl, {withCredentials: true, params: new HttpParams({fromObject: params})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  searchPlaylists(params = {}, playlist_search_query = {}): Observable<PlaylistResponse> {
    let apiUrl = this.apiBaseUrl + '/playlist/search';
    return this.http.post<PlaylistResponse>(apiUrl, playlist_search_query, {withCredentials: true, params: new HttpParams({fromObject: params})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  addPlaylist(playlist: PlaylistModel): Observable<PlaylistModel> {
    let apiUrl = this.apiBaseUrl + '/playlist/';
    return this.http.post<PlaylistModel>(apiUrl, playlist, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json'})}).pipe(
      tap(_ => this.handleEvent('Playlist created')),
      catchError(this.handleError.bind(this))
    );
  }

  getPlaylistExport(playlist_id: number): string {
    return this.apiBaseUrl + '/playlist/' + playlist_id + '/export';
  }

  addPlaylistItem(playlist_item: PlaylistItemModel): Observable<PlaylistItemModel> {
    let apiUrl = this.apiBaseUrl + '/playlist_item/';
    return this.http.post<PlaylistItemModel>(apiUrl, playlist_item, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json'})}).pipe(
      tap(_ => this.handleEvent('Item added to playlist')),
      catchError(this.handleError.bind(this))
    );
  }

  deletePlaylist(playlist_id: number): Observable<Playlist> {
    let apiUrl = this.apiBaseUrl + '/playlist/' + playlist_id;
    return this.http.delete<Playlist>(apiUrl, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Playlist removed')),
      catchError(this.handleError.bind(this))
    );
  }

  deletePlaylistItem(playlist_item_id: number): Observable<PlaylistItem> {
    let apiUrl = this.apiBaseUrl + '/playlist_item/' + playlist_item_id;
    return this.http.delete<PlaylistItem>(apiUrl, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json'})}).pipe(
      tap(_ => this.handleEvent('Item removed from playlist')),
      catchError(this.handleError.bind(this))
    );
  }

  patchPlaylist(playlist_id: number, playlist_data: Object): Observable<PlaylistResponse> {
    let apiUrl = this.apiBaseUrl + '/playlist/' + playlist_id ;
    return this.http.patch<PlaylistResponse>(apiUrl, playlist_data, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Changes saved')),
      catchError(this.handleError.bind(this))
    );
  }

  patchPlaylistItem(playlist_item_id: number, playlist_item_data: Object): Observable<PlaylistItem> {
    let apiUrl = this.apiBaseUrl + '/playlist_item/' + playlist_item_id;
    return this.http.patch<PlaylistItem>(apiUrl, playlist_item_data, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json'})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getTasks(): Observable<Task[]> {
    let apiUrl = this.apiBaseUrl + '/task/';
    return this.http.get<Task[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getTask(task_id: string): Observable<Task> {
    let apiUrl = this.apiBaseUrl + '/task/' + task_id;
    return this.http.get<Task>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getTasksRunning(): Observable<TaskRunning[]> {
    let apiUrl = this.apiBaseUrl + '/task/running';
    return this.http.get<TaskRunning[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this)),
      repeat({ delay: 3_000 }),
    );
  }

  runTask(task_id: string): Observable<Task> {
    let apiUrl = this.apiBaseUrl + '/task/' + task_id + '/run';
    return this.http.get<Task>(apiUrl, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json'})}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getUsers(): Observable<User[]> {
    let apiUrl = this.apiBaseUrl + '/user/';
    return this.http.get<User[]>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }

  getUser(username: string): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/' + username;
    return this.http.get<User>(apiUrl, {withCredentials: true}).pipe(
      catchError(this.handleError.bind(this))
    );
  }
  
  getUserCurrent(): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/me';
    return this.http.get<User>(apiUrl, {withCredentials: true}).pipe(
      tap(current_user => this.current_user = current_user),
      catchError(this.handleError.bind(this))
    );
  }

  addUser(user: UserModel): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/';
    return this.http.post<User>(apiUrl, user, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('User created')),
      catchError(this.handleError.bind(this))
    );
  }

  deleteUser(username: string): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/' + username;
    return this.http.delete<User>(apiUrl, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('User removed')),
      catchError(this.handleError.bind(this))
    );
  }

  patchUser(username: string, user_data: Object): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/' + username;
    return this.http.patch<User>(apiUrl, user_data, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Changes saved')),
      catchError(this.handleError.bind(this))
    );
  }

  patchUserCurrent(user_data: Object): Observable<User> {
    let apiUrl = this.apiBaseUrl + '/user/me';
    return this.http.patch<User>(apiUrl, user_data, {withCredentials: true, headers: new HttpHeaders({ 'Content-Type': 'application/json' })}).pipe(
      tap(_ => this.handleEvent('Changes saved')),
      catchError(this.handleError.bind(this))
    );
  }

  isAdminUser(): boolean {
    if (this.current_user && this.current_user.is_admin){return true;}
    else {return false;}
  }

  login(user_login: UserLoginModel): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/login';
    return this.http.post<string>(apiUrl, user_login, {withCredentials: true}).pipe(
      tap(_ => {this.getUserCurrent().subscribe(); this.router.navigateByUrl('')}),
      catchError(this.handleError.bind(this))
    );
  }

  logout(): Observable<string> {
    let apiUrl = this.apiBaseUrl + '/logout';
    return this.http.post<string>(apiUrl, {}, {withCredentials: true}).pipe(
      tap(_ => {this.current_user = undefined; this.router.navigateByUrl('/login')}),
      catchError(this.handleError.bind(this))
    );
  }

  private handleEvent(message: string): void {
    this.notification.addNotification(NotificationLevel.INFO, message)
  }

  private handleError(error: HttpErrorResponse) {
    let error_message = 'An error occurred: ' + error.message;
    if (error.status === 401){error_message = 'Incorrect username and/or password';}
    if (error.status === 403){error_message = 'Permission denied'; this.router.navigateByUrl('/login');}
    else {this.notification.addNotification(NotificationLevel.ERROR, error_message);}
    return throwError(() => new Error(error_message));
  }
}
