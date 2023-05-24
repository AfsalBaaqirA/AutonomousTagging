import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-predict-tag',
  templateUrl: './predict-tag.component.html',
  styleUrls: ['./predict-tag.component.css']
})
export class PredictTagComponent {
  public title: string;
  public post: string;
  public tags: string[];
  public tagsPredicted: boolean;

  constructor(private http: HttpClient) {
    this.title = '';
    this.post = '';
    this.tags = [];
    this.tagsPredicted = false;
  }

  public predictTags(): void {
    if (this.title === '') {
      return alert('Please enter a title.');
    }
    if (this.post === '') {
      return alert('Please enter a post.');
    }
    const data = {
      title: this.title,
      post: this.post
    };
    this.http.post('http://127.0.0.1:5000/api/predict-tags', data).subscribe((response: any) => {
      this.tags = response.message.tags;
      this.tagsPredicted = true;
      console.log(response);
    });
  }

  public clear(): void {
    this.title = '';
    this.post = '';
    this.tags = [];
    this.tagsPredicted = false;
  }
}
