import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MixMatchService } from '../../services/mixmatch.service';
import { UserLoginModel } from '../../models';

@Component({
    selector: 'app-login',
    imports: [FormsModule],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {
  user_login: UserLoginModel = new UserLoginModel();
  
  constructor(private mixmatchService: MixMatchService) {}

  login(): void {
    this.mixmatchService.login(this.user_login).subscribe();
  }

}
