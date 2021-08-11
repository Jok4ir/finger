import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';

import * as S from '../@store';

@Component({
  selector: 'app-enroll',
  templateUrl: './enroll.component.html',
  styleUrls: ['./enroll.component.scss'],
})
export class EnrollComponent implements OnInit {
  enrollStep$ = this._store.select(S.enrollStep);
  step$ = this._store.select(S.step);

  constructor(private _store: Store<any>) {}

  ngOnInit(): void {}
  enrollClick() {
    this._store.dispatch(S.Actions.beginEnroll());
  }
  enrollStep2() {
    this._store.dispatch(S.Actions.Enroll_step2());
  }
  setUserName(event: any) {
    this._store.dispatch(S.Actions.SetUserName({ name: event.target.value }));
  }
  setUserFirstName(event: any) {
    this._store.dispatch(
      S.Actions.SetUserFirstName({ firstname: event.target.value })
    );
  }
  setUserEmail(event: any) {
    this._store.dispatch(S.Actions.SetUserEmail({ email: event.target.value }));
  }
  gotohome() {
    // this._store.dispatch(S.Actions.GoToAction({ page: 'home' }));
    this._store.dispatch(S.Actions.reset());
  }
}
