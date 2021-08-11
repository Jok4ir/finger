import { createAction, props } from '@ngrx/store';
import { User } from '../User';

export const Actions = {
  init: createAction('[APP] Init'),
  reset: createAction('[APP] Reset'),
  setdummy: createAction(
    '[APP] Action with value set',
    props<{ value: boolean }>()
  ),
  uploadFile: createAction('[APP] UPLOAD FILE', props<{ file: File }>()),
  UploadSuccess: createAction(
    '[APP] UPLOAD SUCCESS',
    props<{ imgFilename: string }>()
  ),
  beginEnroll: createAction('[APP] Begin Enroll'),
  EnrollStep1_Done: createAction(
    '[APP] Enroll 1 Done - remove hand',
    props<{ fingerID: number }>()
  ),
  Enroll_step2: createAction('[APP] Enroll Step 2'),
  EnrollStep2_Done: createAction(
    '[APP] Enroll 2 Done - remove hand - upload file',
    props<{ fingerID: number }>()
  ),
  EnrollError: createAction('[APP] ERROR WHILE ENROLLING'),
  ScanFinger: createAction('[APP] Scan Finger'),
  ScanFingerSuccess: createAction(
    '[APP] Scan Finger Success',
    props<{ user: User }>()
  ),
  ShowUploadPage: createAction('[APP] SHOW upload page'),
  SetUserName: createAction('[APP] Set user name', props<{ name: string }>()),
  SetUserFirstName: createAction(
    '[APP] Set user firstname',
    props<{ firstname: string }>()
  ),
  SetUserEmail: createAction(
    '[APP] Set user email',
    props<{ email: string }>()
  ),
  SetUserImgFilename: createAction(
    '[APP] Set user img filename',
    props<{ img_filename: string }>()
  ),
  SetUserFingerID: createAction(
    '[APP] Set user fingerprint ID',
    props<{ fingerID: number }>()
  ),
  EnrollAll: createAction('[APP] Enroll all', props<{ user: User }>()),
  EnrollSuccess: createAction('[APP] enrolling success'),
  EnrollFailed: createAction('[APP] enroll failed'),
  GoToAction: createAction('[APP] Go to Action', props<{ page: string }>()),
  ReturnToHome: createAction('[APP] return to home'),
};
