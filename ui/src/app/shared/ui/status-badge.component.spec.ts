/**
 * status-badge.component.spec.ts intent header.
 *
 * This test validates the StatusBadgeComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StatusBadgeComponent } from './status-badge.component';

describe('StatusBadgeComponent', () => {
  let component: StatusBadgeComponent;
  let fixture: ComponentFixture<StatusBadgeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatusBadgeComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StatusBadgeComponent);
    component = fixture.componentInstance;
    component.text = 'test status';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should accept text input', () => {
    expect(component.text).toBe('test status');
  });

  it('should render text and tone class', () => {
    component.tone = 'succeeded';
    fixture.detectChanges();

    const element: HTMLElement = fixture.nativeElement;
    const badge = element.querySelector('.badge');
    expect(badge?.textContent).toContain('test status');
    expect(badge?.classList).toContain('succeeded');
  });
});
