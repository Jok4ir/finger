import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import * as S from '../@store';

@Component({
  selector: 'app-fileupload',
  templateUrl: './fileupload.component.html',
  styleUrls: ['./fileupload.component.scss'],
})
export class FileuploadComponent implements OnInit {
  defaultBtn: HTMLElement = document.querySelector(
    '#default-btn'
  ) as HTMLElement;
  imageSrc: string = '';
  img: HTMLElement = document.querySelector('img') as HTMLElement;

  // Variable to store shortLink from api response
  shortLink: string = '';
  loading: boolean = false; // Flag variable
  file: File | null = null; // Variable to store file

  constructor(private _store: Store<any>) {}

  ngOnInit(): void {}

  defaultBtnActive() {
    let btn: HTMLElement = document.querySelector(
      '#default-btn'
    ) as HTMLElement;
    btn.click();
  }

  fileChanged(event: any) {
    let img2: HTMLElement = document.querySelector('img') as HTMLElement;
    const reader = new FileReader();
    this.file = event.target.files[0];

    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;
      reader.readAsDataURL(file);

      reader.onload = () => {
        this.imageSrc = reader.result as string;

        img2.setAttribute('src', this.imageSrc);
      };
    }
  }
  onUpload() {
    this.loading = !this.loading;
    console.log(this.file?.stream);
    // if (this.file != null) {
    //   this._store.dispatch(S.Actions.uploadFile({ value: this.file }));
    // }
    if (this.file != null) {
      this._store.dispatch(S.Actions.uploadFile({ file: this.file }));

      // console.log('WE UPLOAD');
      // var form_data2 = new FormData();
      // const fileToUpload = this.imageSrc;
      // form_data2.append('file', this.file);
      // console.log(form_data2);
      // fetch('http://localhost:5000/upload', {
      //   method: 'POST',
      //   body: form_data2,
      // }).then((resp) => {
      //   console.log('response');
      //   console.log(resp);
      // });
    }
  }
}
