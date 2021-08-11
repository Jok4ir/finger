import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { EMPTY, never, Observable } from 'rxjs';
import {
  withLatestFrom,
  switchMap,
  map,
  mergeMap,
  exhaustMap,
  tap,
} from 'rxjs/operators';

import * as S from '../@store';
import { FileUploadService } from '../file-upload.service';

@Injectable()
export class AppEffects {
  init$ = createEffect(
    () =>
      this.actions$.pipe(
        ofType(S.Actions.init),
        withLatestFrom(this._store.pipe(select(S.state))),
        tap(([action, state]) => {
          if (state.dummy) {
            console.log('true');
          } else {
            console.log('false');
          }
        })
      ),
    { dispatch: false }
  );

  uploadFile$ = createEffect(() =>
    this.actions$.pipe(
      ofType(S.Actions.uploadFile),
      withLatestFrom(this._store.pipe(select(S.state))),
      switchMap(([action, state]) =>
        this._fileUploadService
          .upload$(action.file)
          .pipe(
            map((response) =>
              S.Actions.UploadSuccess({ imgFilename: response.data })
            )
          )
      )
    )
  );
  uploadsuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(S.Actions.UploadSuccess),
      withLatestFrom(this._store.pipe(select(S.state))),
      switchMap(([action, state]) =>
        this._fileUploadService
          .enrollAll$(state.user)
          .pipe(
            map((response) =>
              response.status
                ? S.Actions.EnrollSuccess()
                : S.Actions.EnrollFailed()
            )
          )
      )
    )
  );
  // enrollAll$ = createEffect(() =>
  //   this.actions$.pipe(
  //     ofType(S.Actions.EnrollAll),
  //     withLatestFrom(this._store.pipe(select(S.state))),
  //     switchMap(([action, state]) =>
  //       this._fileUploadService
  //         .enrollAll$(action.user)
  //         .pipe(
  //           map((response) =>
  //             response.status
  //               ? S.Actions.EnrollSuccess()
  //               : S.Actions.EnrollFailed()
  //           )
  //         )
  //     )
  //   )
  // );
  scanFinger$ = createEffect(() =>
    this.actions$.pipe(
      ofType(S.Actions.ScanFinger),
      withLatestFrom(this._store.pipe(select(S.state))),
      switchMap(([action, state]) =>
        this._fileUploadService
          .scan$()
          .pipe(
            map((response) => S.Actions.ScanFingerSuccess({ user: response }))
          )
      )
    )
  );
  beginEnroll$ = createEffect(() =>
    this.actions$.pipe(
      ofType(S.Actions.beginEnroll),
      withLatestFrom(this._store.pipe(select(S.state))),
      switchMap(([action, state]) =>
        this._fileUploadService
          .enroll1$()
          .pipe(
            map((response) =>
              response.status
                ? S.Actions.EnrollStep1_Done({ fingerID: response.fingerID })
                : S.Actions.EnrollError()
            )
          )
      )
    )
  );
  // enrollStep2$ = createEffect(() =>
  //   this.actions$.pipe(
  //     ofType(S.Actions.EnrollStep1_Done),
  //     withLatestFrom(this._store.pipe(select(S.state))),
  //     switchMap(([action, state]) =>
  //       this._fileUploadService
  //         .enroll2$()
  //         .pipe(map((response) => S.Actions.Enroll_step2()))
  //     )
  //   )
  // );
  enrollStep2$ = createEffect(() =>
    this.actions$.pipe(
      ofType(S.Actions.Enroll_step2),
      withLatestFrom(this._store.pipe(select(S.state))),
      switchMap(([action, state]) =>
        this._fileUploadService
          .enroll2$()
          .pipe(
            map((response) =>
              response.status
                ? S.Actions.EnrollStep2_Done({ fingerID: response.fingerID })
                : S.Actions.EnrollError()
            )
          )
      )
    )
  );
  //   showUploadPage$ = createEffect(() =>
  //   this.actions$.pipe(
  //     ofType(S.Actions.ShowUploadPage),
  //     withLatestFrom(this._store.pipe(select(S.state))),
  //     switchMap(([action, state]) =>
  //       this._fileUploadService
  //         .enroll2$()
  //         .pipe(map((response) => S.Actions.EnrollStep2_Done()))
  //     )
  //   )
  // );

  constructor(
    private actions$: Actions,
    private _store: Store<S.State>,
    private _fileUploadService: FileUploadService
  ) {}
}
