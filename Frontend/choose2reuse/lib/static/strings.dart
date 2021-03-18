// ignore: avoid_classes_with_only_static_members

class ReuseStrings {
  static String appName = 'Choose2Reuse';

  //button text
  static String scanContainerButtonText = 'Scan container QR code';
  static String scanLocationButtonText = 'Scan location QR code';
  static String loginButtonText = 'Log in';
  static String signUpButtonText = 'Sign Up';
  static String useCamera = 'Use Camera';
  static String submit = 'Submit';
  static String cancel = 'Cancel';

  //page titles
  static String homepageTitle = 'Dashboard';
  static String signUpPageTitle = 'Sign Up';

  //field text
  static String emailField = 'Email';
  static String passwordField = 'Password';
  static String confirmPasswordField = 'Confirm Password';
  static String firstNameField = 'First Name';
  static String middleNameField = 'Middle Name';
  static String lastNameField = 'Last Name';
  static String classYearField = 'Class Year';
  static String phoneNumberField = 'Phone Number';
  static String enterValidationCodeField = 'Enter code here';

  //textButton text
  static String rememberPassword = 'Remember me';
  static String goToSignUpPageText = 'Need an account? Sign up here!';
  static String goToValidationPageText =
      'Have a verification code? Enter it here!';
  static String requestNewCode = 'Request a new code';

  //label text/instructions
  static String scanLocationMessage =
      'Please scan the QR code at the drop-off location. Here is a sample QR code:';
  static String scanContainerMessage =
      'Please scan the QR code on the container.';
  static String scanBeforeTimer =
      'Please scan the QR code on the container before the timer runs out:';
  static String welcomeLabel = 'Welcome!';
  static String validationInstruction =
      'Thank you for signing up for the Choose 2 Reuse App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.';

  //error message
  static String timerOutErrorMessage = 'Timer has ran out.';
  static String invalidCodeErrorMessage = 'Please enter a valid code.';
}
