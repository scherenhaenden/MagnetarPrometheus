/**
 * run-history-page.component.spec.ts intent header.
 *
 * This test validates the RunHistoryPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { RunHistoryPageComponent } from './run-history-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('RunHistoryPageComponent', () => {
  let component: RunHistoryPageComponent;
  let fixture: ComponentFixture<RunHistoryPageComponent>;

  beforeEach(async () => {
    const mockDataService = {
      getRunHistory: jasmine.createSpy('getRunHistory').and.returnValue(of([]))
    };

    await TestBed.configureTestingModule({
      imports: [RunHistoryPageComponent, RouterTestingModule],
      providers: [
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RunHistoryPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
