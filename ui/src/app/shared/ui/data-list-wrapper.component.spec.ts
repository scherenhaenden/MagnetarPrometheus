/**
 * data-list-wrapper.component.spec.ts intent header.
 *
 * This test validates the DataListWrapperComponent.
 */
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DataListWrapperComponent } from './data-list-wrapper.component';

describe('DataListWrapperComponent', () => {
  let component: DataListWrapperComponent;
  let fixture: ComponentFixture<DataListWrapperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DataListWrapperComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DataListWrapperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
