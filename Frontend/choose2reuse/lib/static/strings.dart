// ignore: avoid_classes_with_only_static_members

class ReuseStrings {
  static String appName = 'Choose2Reuse';

  //button text
  static String resetReturnButtonText = 'Start a new return';
  static String scanContainerButtonText = 'Scan container QR code';
  static String scanLocationButtonText = 'Scan location QR code';
  static String loginButtonText = 'Log in';
  static String signUpButtonText = 'Sign Up';
  static String viewAllButtonText = 'View All';
  static String useCamera = 'Use Camera';
  static String submit = 'Submit';
  static String cancel = 'Cancel';
  static String yes = 'Yes';
  static String save = 'Save';
  static String changePassword = 'Change Password';
  static String logOut = 'Log Out';

  //page titles
  static String homepageTitle = 'Dashboard';
  static String signUpPageTitle = 'Sign Up';
  static String containerListTitle = 'Container History';
  static String profilePageTitle = 'Profile';
  static String changePasswordPageTitle = 'Change Password';
  static String forgotPasswordPageTitle = 'Forgot Password';
  static String pointsPageTitle = 'My Points & Rewards';

  //field text
  static String emailField = 'Email';
  static String passwordField = 'Password';
  static String confirmPasswordField = 'Confirm Password';
  static String firstNameField = 'First Name';
  static String middleNameField = 'Middle Name (Optional)';
  static String lastNameField = 'Last Name';
  static String classYearField = 'Class Year (Optional)';
  static String phoneNumberField = 'Phone Number';
  static String enterValidationCodeField = 'Enter code here';
  static String currentPasswordField = 'Current Password';
  static String newPasswordField = 'New Password';
  static String confirmNewPasswordField = 'Confirm New Password';

  //textButton text
  static String rememberPassword = 'Remember me';
  static String goToSignUpPageText = 'Need an account? Sign up here!';
  static String goToValidationPageText =
      'Have a verification code? Enter it here!';
  static String requestNewCode = 'Request a new code';
  static String forgotPassword = 'Forgot Password';
  static String sendCode = 'Send Code';

  //label text/instructions
  static String scanLocationMessage =
      'Please scan the QR code at the drop-off location. Here is a sample QR code:';
  static String scanContainerMessage =
      'Please scan the QR code on the container.';
  static String scanBeforeTimer =
      'Please scan the QR code on the container before the timer runs out:';
  static String welcomeLabel = 'Welcome!';
  static String validationInstruction =
      'Thank you for signing up for the Choose2Reuse App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.';
  static String filterBy = 'Filter By';
  static String lostOrDamagedQuestion =
      'Please provide details to report this container as lost or damaged.';
  static String lostOrDamagedTitle = 'Report a Container';
  static String lostOrDamagedPrompt = 'Enter your reasoning here';
  static String noContainers = 'No containers found.';
  static String undoLostOrDamagedQuestion =
      'Are you sure you want to undo marking this container as damaged/lost?';
  static String myPoints = 'Points';

  //snackbar messages
  static String changePassSuccess = 'Password changed successfully';
  static String updateProfileSuccess = 'Information updated successfully';

  //error message
  static String timerOutErrorMessage = 'Timer has ran out.';
  static String invalidCodeErrorMessage = 'Please enter a valid code.';
  static String emptyEmailErrorMessage = 'Please enter an email address.';
  static String passMismatchErrorMessage = 'New password fields do not match.';
}
