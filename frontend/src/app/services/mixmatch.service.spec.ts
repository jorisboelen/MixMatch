import { TestBed } from '@angular/core/testing';

import { MixMatchService } from './mixmatch.service';

describe('MixMatchService', () => {
  let service: MixMatchService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MixMatchService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
