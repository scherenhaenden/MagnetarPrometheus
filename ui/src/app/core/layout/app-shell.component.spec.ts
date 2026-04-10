/**
 * app-shell.component.spec.ts intent header.
 *
 * This test validates the AppShellComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { firstValueFrom, of, skip, throwError } from 'rxjs';
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
      providers: [{ provide: FrontendDataService, useValue: mockDataService }]
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

  it('should render primary navigation in top workflow bar', () => {
    const element: HTMLElement = fixture.nativeElement;
    const links = Array.from(element.querySelectorAll('.workflow-nav a')).map((item) => item.textContent?.trim());
    expect(links).toContain('Workflow Studio');
    expect(links).toContain('Run History');
  });

  it('should expose the healthy tone after the service health resolves', async () => {
    await expectAsync(firstValueFrom(component['healthTone$'].pipe(skip(1)))).toBeResolvedTo('healthy');
    await expectAsync(firstValueFrom(component['healthLabel$'].pipe(skip(1)))).toBeResolvedTo(
      'healthy · MOCK · Mock service is healthy'
    );
  });

  it('should fall back to offline health state when the service health request fails', async () => {
    TestBed.resetTestingModule();
    await TestBed.configureTestingModule({
      imports: [AppShellComponent, RouterTestingModule],
      providers: [
        {
          provide: FrontendDataService,
          useValue: {
            getServiceHealth: jasmine
              .createSpy('getServiceHealth')
              .and.returnValue(throwError(() => new Error('network down')))
          }
        }
      ]
    }).compileComponents();

    const offlineFixture = TestBed.createComponent(AppShellComponent);
    const offlineComponent = offlineFixture.componentInstance;
    offlineFixture.detectChanges();

    await expectAsync(firstValueFrom(offlineComponent['healthTone$'].pipe(skip(1)))).toBeResolvedTo('offline');
    await expectAsync(firstValueFrom(offlineComponent['healthLabel$'].pipe(skip(1)))).toBeResolvedTo(
      'offline · API · Service unreachable'
    );

    const element: HTMLElement = offlineFixture.nativeElement;
    const status = element.querySelector('.status');
    expect(status?.textContent).toContain('offline · API · Service unreachable');
    expect(status?.classList).toContain('offline');
  });
});
