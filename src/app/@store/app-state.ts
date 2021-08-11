import { User } from '../User';

export interface State {
  readonly dummy: boolean;
  /**
   * 0 - initial (do nothing)
   * 1 - scaning 1
   * 2 - scaning 1 DONE
   * 3 - scaning 2
   * 4 - scaning 2 DONE
   * -1 - ERROR WHILE ENROLL
   */
  readonly enrollStep: number;
  readonly user: User;
  readonly action: string;
}

export const InitialState: State = {
  dummy: true,
  enrollStep: 0,
  user: {
    name: '',
    firstname: '',
    email: '',
    img_filename: '',
    fingerID: -1,
  },
  action: 'home',
};
