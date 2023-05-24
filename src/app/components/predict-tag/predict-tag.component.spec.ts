import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictTagComponent } from './predict-tag.component';

describe('PredictTagComponent', () => {
  let component: PredictTagComponent;
  let fixture: ComponentFixture<PredictTagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PredictTagComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictTagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
