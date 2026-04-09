/**
 * mock-frontend-data.service.spec.ts intent header.
 *
 * This test file validates the MockFrontendDataService class.
 */
import { TestBed } from '@angular/core/testing';
import { MockFrontendDataService } from './mock-frontend-data.service';

describe('MockFrontendDataService', () => {
  let service: MockFrontendDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MockFrontendDataService]
    });
    service = TestBed.inject(MockFrontendDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
