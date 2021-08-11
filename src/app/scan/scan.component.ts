import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { environment } from 'src/environments/environment';
import * as S from '../@store';

@Component({
  selector: 'app-scan',
  templateUrl: './scan.component.html',
  styleUrls: ['./scan.component.scss'],
})
export class ScanComponent implements OnInit {
  fingerID$ = this._store.select(S.fingerID);
  name$ = this._store.select(S.name);
  first_name$ = this._store.select(S.first_name);
  email$ = this._store.select(S.email);
  imgfilename$ = this._store.select(S.filename);
  imgUrl = environment.imagesFolder;

  constructor(private _store: Store<any>) {}

  scanClick() {
    console.log('click');
    this._store.dispatch(S.Actions.ScanFinger());
  }
  gotohome() {
    // this._store.dispatch(S.Actions.GoToAction({ page: 'home' }));
    this._store.dispatch(S.Actions.reset());
  }

  ngOnInit(): void {}
}
