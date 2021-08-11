import { Component } from '@angular/core';
import { select } from '@ngrx/store';
import { Store } from '@ngrx/store';

import * as S from './@store';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  dummy = this._store.pipe(select(S.dummy));
  action$ = this._store.select(S.action);
  constructor(private _store: Store<S.State>) {
    this._store.dispatch(S.Actions.init());
  }
  gotoscan() {
    this._store.dispatch(S.Actions.GoToAction({ page: 'scan' }));
  }
  gotoenroll() {
    this._store.dispatch(S.Actions.GoToAction({ page: 'enroll' }));
  }
}
