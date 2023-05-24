import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  public links: { name: string, url: string }[];

  constructor() {
    this.links = [
      { name: 'Home', url: '/' },
      { name: 'Predict', url: '/predict-tag' }
    ];
  }
}
