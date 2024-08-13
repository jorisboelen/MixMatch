export class MusicSearchQueryModel {

  constructor(
    public artist?: string,
    public title?: string,
    public genre_id?: number,
    public year_lowest?: string,
    public year_highest?: string,
    public bpm_lowest?: number,
    public bpm_highest?: number,
    public key?: Array<string>,
    public include_compatible_keys?: boolean,
    public rating_lowest?: number,
    public rating_highest?: number,
    public sort_by: string = '',
    public sort_order: string = 'asc',
    public random?: boolean
  ) { }

}

export class PlaylistModel {

  constructor(
    public name?: string
  ) { }

}

export class PlaylistItemModel {

  constructor(
    public playlist_id?: number,
    public music_id?: number,
    public order: number = 0
  ) { }

}

export class UserModel {

  constructor(
    public username?: string,
    public password?: string,
    public is_admin?: boolean
  ) { }
}

export class UserLoginModel {

  constructor(
    public username?: string,
    public password?: string
  ) { }

}
