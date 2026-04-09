/**
 * page-header.component.spec.ts intent header.
 *
 * This test validates the PageHeaderComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PageHeaderComponent } from './page-header.component';

describe('PageHeaderComponent', () => {
  let component: PageHeaderComponent;
  let fixture: ComponentFixture<PageHeaderComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageHeaderComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PageHeaderComponent);
    component = fixture.componentInstance;
    component.title = 'Test Title';
    component.description = 'Test Description';
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should accept inputs', () => {
    expect(component.title).toBe('Test Title');
    expect(component.description).toBe('Test Description');
  });

  it('should render the title and description', () => {
    const element: HTMLElement = fixture.nativeElement;
    expect(element.querySelector('h2')?.textContent).toContain('Test Title');
    expect(element.querySelector('p')?.textContent).toContain('Test Description');
  });
});
