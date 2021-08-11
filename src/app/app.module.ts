import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { FileuploadComponent } from './fileupload/fileupload.component';
import { StoreModule } from '@ngrx/store';
import * as R from './@store/app-reducer';
import { EffectsModule } from '@ngrx/effects';
import { AppEffects } from './@services/app-effects';
import { FileUploadService } from './file-upload.service';
import { HttpClientModule } from '@angular/common/http';
import { ScanComponent } from './scan/scan.component';
import { EnrollComponent } from './enroll/enroll.component';

@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
    StoreModule.forFeature('app', R.reducer),
    StoreModule.forRoot({}),
    EffectsModule.forRoot([AppEffects]),
    EffectsModule.forFeature([AppEffects]),
  ],
  declarations: [
    AppComponent,
    FileuploadComponent,
    ScanComponent,
    EnrollComponent,
  ],
  providers: [FileUploadService],
  bootstrap: [AppComponent],
})
export class AppModule {}
