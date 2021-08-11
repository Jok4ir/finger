import { createFeatureSelector, createSelector } from '@ngrx/store';
import { State } from '.';

export const state = createFeatureSelector<State>('app');

export const dummy = createSelector(state, (s) => s.dummy);
export const enrollStep = createSelector(state, (s) => s.enrollStep);
export const step = createSelector(enrollStep, (s) => {
  if (s == 1) {
    return 'posez votre doigt';
  } else if (s == 2) {
    return 'enlevez votre doigt puis reposez-le pour une deuxieme fois';
  } else if (s == 3) {
    return 'Choisir une image maintenant';
  } else if (s == -1) {
    return "une erreur est survenue lors de l'enregistrement";
  }
  return 'pret a scanner';
});
export const user = createSelector(state, (s) => s.user);
export const fingerID = createSelector(user, (u) => u.fingerID);
export const name = createSelector(user, (u) => u.name);
export const filename = createSelector(user, (u) => u.img_filename);
export const first_name = createSelector(user, (u) => u.firstname);
export const email = createSelector(user, (u) => u.email);
export const action = createSelector(state, (s) => s.action);
