import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { defer, Observable } from 'rxjs';
import { AppService } from './app.service';
import { environment } from 'src/environments/environment';
import { User } from './User';
import { EnrollOutput } from './EnrollOutput';

const UPLOAD_URL = environment.baseApiUrl + '/upload';

@Injectable()
export class FileUploadService implements AppService {
  // API url

  constructor(private http: HttpClient) {}

  // Returns an observable
  upload$(file: File) {
    // Create form data
    const formData = new FormData();

    // const config = new HttpHeaders().set(
    //   'Content-Type',
    //   'application/x-www-form-urlencoded'
    // );

    // Store form name as "file" with file data
    formData.append('file', file);
    return defer(() =>
      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      }).then((resp) => {
        // console.log('response');
        return resp.json().then(function (data: EnrollOutput) {
          return data;
        });
      })
    );

    // Make http post request over api
    // with formData as req
    // return this.http.post(UPLOAD_URL, formData, { headers: config });
  }
  scan$() {
    return defer(() =>
      fetch('http://localhost:5000/scan', {
        method: 'POST',
      }).then((resp) => {
        return resp.json().then(function (data: User) {
          return data;
        });
        // console.log('response');
        // console.log(resp);
      })
    );
  }
  enroll1$() {
    return defer(() =>
      fetch('http://localhost:5000/enroll1', {
        method: 'POST',
      }).then((resp) => {
        return resp.json().then(function (data: EnrollOutput) {
          return data;
        });
        // console.log('response');
        console.log(resp);
      })
    );
  }
  enroll2$() {
    return defer(() =>
      fetch('http://localhost:5000/enroll2', {
        method: 'POST',
      }).then((resp) => {
        return resp.json().then(function (data: EnrollOutput) {
          console.log(data);
          return data;
        });
        // console.log('response');
        console.log(resp);
      })
    );
  }
  enrollAll$(user: User) {
    const formData = new FormData();
    formData.append('filename', user.img_filename);
    formData.append('email', user.email);
    formData.append('firstName', user.firstname);
    formData.append('name', user.name);
    formData.append('fingerprintID', user.fingerID.toString());
    console.log(formData);
    return defer(() =>
      fetch('http://localhost:5000/enroll', {
        method: 'POST',
        body: formData,
      }).then((resp) => {
        return resp.json().then(function (data: EnrollOutput) {
          return data;
        });
        // console.log('response');
        console.log(resp);
      })
    );
  }
}
