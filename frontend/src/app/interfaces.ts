export interface Genre {
  id: number;
  name: string;
}

export interface Playlist {
  id: number;
  name: string;
  owner: string;
  created: Date;
  modified: Date;
  playlist_items: Array<PlaylistItem>;
}

export interface PlaylistItem {
  id: number;
  track: Track;
  order: number;
}

export interface PlaylistResponse {
  total: number;
  page: number;
  size: number;
  pages: number;
  items: Array<Playlist>;
}

export enum NotificationLevel {
  ERROR = 'danger',
  WARN = 'warning',
  INFO = 'success',
  DEBUG = 'info',
}

export interface NotificationMessage {
  level: NotificationLevel;
  message: string;
  timestamp: Date;
}

export interface Task {
  id: string;
  name: string;
  results: Array<TaskResult>;
}

export interface TaskResult {
  id: string;
  state: string;
  result: string;
  started: Date;
  completed: Date;
}

export interface TaskRunning {
  id: string;
  task: Task;
  state: string;
  result: string;
  started: Date;
  completed: Date;
}

export interface Track {
  id: number;
  path: string;
  mtime: number;
  type: string;
  bitrate: number;
  length: number;
  artist: string;
  title: string;
  album: string;
  genre: Genre;
  date: Date;
  bpm: number;
  key: string;
  rating: number;
}

export interface TrackResponse {
  total: number;
  page: number;
  size: number;
  pages: number;
  items: Array<Track>;
}

export interface User {
  username: string;
  is_admin: boolean;
}

export interface StreamState {
  playing: boolean;
  duration: number | undefined;
  currentTime: number | undefined;
  canplay: boolean;
  volume: number;
  muted: boolean;
  error: boolean;
}
