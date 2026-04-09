/**
 * app-shell.component.spec.ts intent header.
 *
 * This test validates the AppShellComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { AppShellComponent } from './app-shell.component';
import { FrontendDataService } from '../../shared/services/frontend-data.service';

describe('AppShellComponent', () => {
  let component: AppShellComponent;
  let fixture: ComponentFixture<AppShellComponent>;

  beforeEach(async () => {
    const mockDataService = {
      getServiceHealth: jasmine.createSpy('getServiceHealth').and.returnValue(of({
        status: 'healthy',
        message: 'Mock service is healthy',
        checkedAtIso: new Date().toISOString(),
        mode: 'mock'
      }))
    };

    await TestBed.configureTestingModule({
      imports: [AppShellComponent, RouterTestingModule],
      providers: [
        { provide: FrontendDataService, useValue: mockDataService }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AppShellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should request service health during initialization', () => {
    expect(TestBed.inject(FrontendDataService).getServiceHealth).toHaveBeenCalled();
  });

  it('should render the health label', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('.status')?.textContent).toContain('healthy · MOCK · Mock service is healthy');
  });
});
