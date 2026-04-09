/**
 * run-detail-page.component.spec.ts intent header.
 *
 * This test validates the RunDetailPageComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { RunDetailPageComponent } from './run-detail-page.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('RunDetailPageComponent', () => {
  let component: RunDetailPageComponent;
  let fixture: ComponentFixture<RunDetailPageComponent>;

  beforeEach(async () => {
    const mockDataService = {
      getRunDetail: jasmine.createSpy('getRunDetail').and.returnValue(of(null))
    };

    await TestBed.configureTestingModule({
      imports: [RunDetailPageComponent, RouterTestingModule],
      providers: [
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RunDetailPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
