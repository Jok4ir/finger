import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';
import { Action, createReducer, on } from '@ngrx/store';
import * as S from './';

export interface StateEntity extends EntityState<S.State> {
  state: S.State;
  logs: {
    type: string;
    message: string;
  };
}

export const AppAdapter: EntityAdapter<S.State> = createEntityAdapter<S.State>({
  sortComparer: false,
});

const appReducer = createReducer(
  S.InitialState,
  on(S.Actions.init, (state) => {
    // console.log('blabla');
    return { ...state, dummy: false };
  }),
  on(S.Actions.reset, (state) => S.InitialState),
  on(S.Actions.setdummy, (state, { value }) => ({ ...state, dummy: value })),
  on(S.Actions.ScanFingerSuccess, (state, action) => ({
    ...state,
    user: action.user,
  })),
  on(S.Actions.beginEnroll, (state) => ({ ...state, enrollStep: 1 })),
  on(S.Actions.EnrollStep1_Done, (state, action) => ({
    ...state,
    enrollStep: 2,
    user: { ...state.user, fingerID: action.fingerID },
  })),
  on(S.Actions.EnrollStep2_Done, (state, action) => ({
    ...state,
    enrollStep: 3,
    // user: { ...state.user, fingerID: action.fingerID },
  })),
  on(S.Actions.EnrollError, (state) => ({ ...state, enrollStep: -1 })),
  on(S.Actions.SetUserName, (state, action) => ({
    ...state,
    user: { ...state.user, name: action.name },
  })),
  on(S.Actions.SetUserFirstName, (state, action) => ({
    ...state,
    user: { ...state.user, firstname: action.firstname },
  })),
  on(S.Actions.SetUserEmail, (state, action) => ({
    ...state,
    user: { ...state.user, email: action.email },
  })),
  on(S.Actions.SetUserFingerID, (state, action) => ({
    ...state,
    user: { ...state.user, fingerID: action.fingerID },
  })),
  on(S.Actions.SetUserImgFilename, (state, action) => ({
    ...state,
    user: { ...state.user, img_filename: action.img_filename },
  })),
  on(S.Actions.UploadSuccess, (state, action) => ({
    ...state,
    user: { ...state.user, img_filename: action.imgFilename },
  })),
  on(S.Actions.GoToAction, (state, action) => ({
    ...state,
    action: action.page,
  }))
);

export function reducer(state: S.State, action: Action) {
  return appReducer(state, action);
}
